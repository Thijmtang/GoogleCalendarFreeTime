import datetime
from GoogleApiClient import GoogleApiClient
from GoogleCalendarUtils import GoogleCalendarUtils
from GoogleCalendarService import GoogleCalendarService


def main():
    googleApiClient = GoogleApiClient()
    googleCalendarService = GoogleCalendarService(googleApiClient)

    startDate = datetime.datetime.strptime('05-01-2024', '%d-%m-%Y')
    endDate = datetime.datetime.strptime('29-01-2024', '%d-%m-%Y')

    events = googleCalendarService.getMultipleCalendarEvents([
        'primary',
        'infusb8pcq01dq2a1ojpsi650m9b3jcq@import.calendar.google.com'
    ], startDate, endDate)

    minimumTime = datetime.time(8, 30)
    minimalIntervalBetween = 60

    # Process events
    days = GoogleCalendarUtils.getAvailabilityCalendarDays(
        start=startDate,
        end=endDate,
        minimumTime=minimumTime,
        minimalIntervalBetweenInMinutes=minimalIntervalBetween,
        events=events
    )

    for day, available in days.items():
        print(day, available)


if __name__ == "__main__":
    main()
