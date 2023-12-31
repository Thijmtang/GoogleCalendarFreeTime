import datetime
import os
import subprocess
from typing import Any
import xlsxwriter
from Services.GoogleCalendarService import GoogleCalendarService
from Utils.SettingsUtils import SettingsUtils
from Utils.TimeUtils import TimeUtils


class GoogleCalendarUtils:
    @staticmethod
    def getEventFromDate(events, start: datetime, end: datetime) -> list:
        """Filter events based on start date and end date, to reduce number of API calls"""

        result = []

        if events is None:
            return result

        for event in events:
            dateTimeFormat = GoogleCalendarService.GOOGLE_DATETIME_FORMAT
            keyValue = 'dateTime'

            # All day event, fuck your freetime
            if 'dateTime' not in event['start']:
                dateTimeFormat = GoogleCalendarService.GOOGLE_DATE_FORMAT
                keyValue = 'date'

            eventStartDate = datetime.datetime.strptime(event['start'][keyValue], dateTimeFormat)
            eventEndDate = datetime.datetime.strptime(event['end'][keyValue], dateTimeFormat)

            if eventStartDate.date() < start.date() and eventEndDate.date() < start.date():
                continue

            if eventStartDate.date() > end.date() and eventEndDate.date() > start.date():
                continue

            result.append(event)

        return result

    @staticmethod
    def getAvailabilityCalendarDays(
            start: datetime,
            end: datetime,
            minimumTime: datetime.time,
            minimalIntervalBetweenInMinutes: int,
            events: list
    ) -> dict[Any, bool]:
        """Filter events based on the availability of the user"""

        availableDays = {}
        currenIterationDate = start

        while end >= currenIterationDate:
            # Convert date into string to be able to use as a key
            dateStringFormat = currenIterationDate.strftime("%d-%m-%Y")

            availableDays[dateStringFormat] = True

            # Filter out the events which are not within given time frame
            currentDateEvents = GoogleCalendarUtils.getEventFromDate(events,
                                                                     datetime.datetime.combine(currenIterationDate,
                                                                                               datetime.time.min),
                                                                     datetime.datetime.combine(currenIterationDate,
                                                                                               datetime.time.max))

            currenIterationDate = currenIterationDate + datetime.timedelta(days=1)

            # No events found
            if currentDateEvents is None:
                continue

            for event in currentDateEvents:
                # Python is disgusting
                # Incorrect format response
                if 'start' not in event or 'end' not in event or dateStringFormat not in availableDays:
                    continue

                # Already determined that not available
                if not availableDays[dateStringFormat]:
                    break

                # All day event
                if 'dateTime' not in event['start']:
                    availableDays[dateStringFormat] = False
                    continue

                bannedKeywords = SettingsUtils.getSummaryBannedKeywords()

                for bannedKeyword in bannedKeywords:

                    if event['summary'] is None:
                        break

                    # A banned keyword found in summary
                    if event['summary'].find(bannedKeyword) != -1:
                        availableDays[dateStringFormat] = False
                        break

                # Not a all day event
                eventStartDate = datetime.datetime.strptime(event['start']['dateTime'],
                                                            GoogleCalendarService.GOOGLE_DATETIME_FORMAT)

                # Initialise the supposed start time u would be available
                desired_datetime = datetime.datetime.combine(eventStartDate,
                                                             datetime.time(minimumTime.hour, minimumTime.minute))

                # Calculate the difference
                time_difference = datetime.datetime.astimezone(eventStartDate).replace(tzinfo=None) - desired_datetime

                # Extract the difference in minutes
                minutes_difference = time_difference.total_seconds() / 60

                # Not enough time in between
                if minutes_difference <= minimalIntervalBetweenInMinutes:
                    availableDays[dateStringFormat] = False

        return availableDays

    @staticmethod
    def createExcel(excelFileName, days: dict[Any, bool], minimumTime, minimalIntervalBetween):
        if os.path.exists(excelFileName):
            subprocess.call("TASKKILL /F /IM excel.exe", shell=True)

        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(excelFileName)
        worksheet = workbook.add_worksheet('Overview')

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({"bold": True})

        i = 1

        for day, available in days.items():
            color = 'red'
            if available:
                color = 'green'

            cell_format = workbook.add_format({'bold': True, 'bg_color': color, 'font_color': 'white'})

            date = datetime.datetime.strptime(day, "%d-%m-%Y")

            worksheet.write("A" + str(i), date.strftime('%d-%m-%Y %A', ), cell_format)
            worksheet.write("B" + str(i), available)

            # sunday
            if date.weekday() == 6:
                i += 1

            i += 1

        worksheet.write("A" + str(i), "Minimum tijd", bold)
        worksheet.write("B" + str(i), "Minimale interval", bold)
        worksheet.write("C" + str(i), "Eindelijke start tijd", bold)

        i += 1
        worksheet.write("A" + str(i), minimumTime.strftime('%H:%M'))
        worksheet.write("B" + str(i), minimalIntervalBetween)

        minimumTime = TimeUtils.addMinutesToTime(minimumTime, minimalIntervalBetween)

        worksheet.write("C" + str(i), minimumTime.strftime('%H:%M'))

        # Autosize columns
        worksheet.set_column("A:C", 20)

        workbook.close()