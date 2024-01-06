import datetime
import string
from typing import Any

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import GoogleApiClient


class GoogleCalendarService:
    GOOGLE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
    GOOGLE_DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, googleApiClient: GoogleApiClient):
        self.googleApiClient = googleApiClient
        self.service = build('calendar', 'v3', credentials=googleApiClient.credentials)

    # https://www.googleapis.com/calendar/v3/calendars/calendarId/events/eventId
    def getEvents(self, calendarId: string, startDate: datetime, endDate: datetime):
        # Round start hours minutes seconds down to 00:00:00
        start_datetime = datetime.datetime.combine(startDate, datetime.time.min)
        # Round the hours minutes seconds the maximal possible value
        end_datetime = datetime.datetime.combine(endDate, datetime.time.max)

        try:
            # fetch
            events_result = (
                self.service.events()
                .list(
                    calendarId=calendarId,
                    timeMin=start_datetime.isoformat() + 'Z',
                    timeMax=end_datetime.isoformat() + 'Z',
                    singleEvents=True,
                    showDeleted=False,
                    orderBy="startTime",
                ).execute()
            )

            events = events_result.get("items", [])

            return events

        except HttpError as error:
            print(error)

    def getMultipleCalendarEvents(self, calendars: list, startDate: datetime.date, endDate: datetime):
        events = []

        for calendar in calendars:
            try:
                events = events + self.getEvents(
                    calendar,
                    startDate, endDate)
            except:
                # Invalid calendar id
                continue

        return events

    def getCalendars(self):
        page_token = None
        while True:
            calendars = []
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                calendars.append(calendar_list_entry)
            if not page_token:
                return calendars



    def getCalendar(self, calendarId: str):
        calendar = self.service.calendars().get(calendarId=calendarId).execute()
        return calendar
