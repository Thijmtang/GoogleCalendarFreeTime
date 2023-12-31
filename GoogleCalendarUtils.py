import datetime

from GoogleCalendarService import GoogleCalendarService


class GoogleCalendarUtils:
    @staticmethod
    def getEventFromDate(events, start: datetime, end: datetime):
        """Filter events based on start date and end date, to reduce number of API calls"""

        if events is None:
            return

        result = []
        for event in events:
            dateTimeFormat = GoogleCalendarService.GOOGLE_DATETIME_FORMAT
            keyValue = 'dateTime'

            # All day event, fuck your freetime
            if 'dateTime' not in event['start']:
                dateTimeFormat = GoogleCalendarService.GOOGLE_DATE_FORMAT
                keyValue = 'date'

            eventStartDate = datetime.datetime.strptime(event['start'][keyValue], dateTimeFormat)
            eventEndDate = datetime.datetime.strptime(event['end'][keyValue], dateTimeFormat)

            if eventStartDate.date() < start.date() and eventEndDate.date() <= start.date():
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
    ):
        """Filter events based on the availability of the user"""

        availableDays = {}
        currenIterationDate = start

        while currenIterationDate < end:
            # Convert date into string to be able to use as a key
            dateStringFormat = currenIterationDate.strftime("%d-%m-%Y")

            availableDays[dateStringFormat] = True

            # Filter out the events which are not within given time frame
            currentDateEvents = GoogleCalendarUtils.getEventFromDate(events,
                                                                     datetime.datetime.combine(currenIterationDate,
                                                                                               datetime.time.min),
                                                                     datetime.datetime.combine(currenIterationDate,
                                                                                               datetime.time.max))
            # No events found
            if currentDateEvents is None:
                continue

            for event in currentDateEvents:
                # Python is disgusting

                # Incorrect format response
                if 'start' not in event or 'end' not in event or dateStringFormat not in availableDays:
                    return

                # All day event, fuck your freetime
                if 'dateTime' not in event['start']:
                    # print(event['start']['date'])
                    availableDays[dateStringFormat] = False
                    continue

                # Not a all day event
                eventStartDate = datetime.datetime.strptime(event['start']['dateTime'],
                                                            GoogleCalendarService.GOOGLE_DATETIME_FORMAT)
                eventEndDate = datetime.datetime.strptime(event['end']['dateTime'],
                                                          GoogleCalendarService.GOOGLE_DATETIME_FORMAT)

                # Initialise the supposed start time u would be available
                desired_datetime = datetime.datetime.combine(eventStartDate,
                                                             datetime.time(minimumTime.hour, minimumTime.minute))

                # Calculate the difference
                time_difference = datetime.datetime.astimezone(eventStartDate).replace(tzinfo=None) - desired_datetime

                # Extract the difference in minutes
                minutes_difference = time_difference.total_seconds() / 60
                print(minutes_difference)

                # fuck off
                # Not enough time in between
                if minutes_difference <= 0 or minutes_difference < minimalIntervalBetweenInMinutes:
                    availableDays[dateStringFormat] = False

            currenIterationDate = currenIterationDate + datetime.timedelta(days=1)

        return availableDays
