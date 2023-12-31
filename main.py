import datetime
import locale
import os
import subprocess

from GoogleApiClient import GoogleApiClient
from Utils.GoogleCalendarUtils import GoogleCalendarUtils
from Services.GoogleCalendarService import GoogleCalendarService
import xlsxwriter

from Utils.SettingsUtils import SettingsUtils
from Utils.TimeUtils import TimeUtils


def main():
    locale.setlocale(locale.LC_ALL, "nl_NL")

    googleApiClient = GoogleApiClient()
    googleCalendarService = GoogleCalendarService(googleApiClient)

    startDate = datetime.datetime.strptime(SettingsUtils.getStartDate(), '%d-%m-%Y')
    endDate = datetime.datetime.strptime(SettingsUtils.getEndDate(), '%d-%m-%Y')

    events = googleCalendarService.getMultipleCalendarEvents(SettingsUtils.getCalendars(), startDate, endDate)

    minimumTime = datetime.time(7, 30)
    minimalIntervalBetween = 120

    # Process events
    days = GoogleCalendarUtils.getAvailabilityCalendarDays(
        start=startDate,
        end=endDate,
        minimumTime=minimumTime,
        minimalIntervalBetweenInMinutes=minimalIntervalBetween,
        events=events
    )
    print(days)

    excelFileName = "overview-calendar.xlsx"

    GoogleCalendarUtils.createExcel(excelFileName, days, minimumTime, minimalIntervalBetween)

    os.system("start EXCEL.EXE " + excelFileName)


if __name__ == "__main__":
    main()
