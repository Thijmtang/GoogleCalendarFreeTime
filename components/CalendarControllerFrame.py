import json
from functools import partial

import customtkinter
from CTkMessagebox import CTkMessagebox

from GoogleApiClient import GoogleApiClient
from services.GoogleCalendarService import GoogleCalendarService
from utils.ScreenUtils import ScreenUtils
from utils.SettingsUtils import SettingsUtils


class CalendarController(customtkinter.CTkFrame):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)

        googleApiclient = GoogleApiClient()
        calendarService = GoogleCalendarService(googleApiclient)

        calendarScroll = customtkinter.CTkScrollableFrame(master=self)
        calendarScroll.pack(side=customtkinter.BOTTOM, fill=customtkinter.BOTH, expand=1)

        labelCalendarSummary = customtkinter.CTkLabel(master=self,
                                                      text="Available calendars, events will show for the enabled calendar's")
        labelCalendarSummary.pack(side=customtkinter.TOP, pady=10, anchor='w')

        def renderCalendars():
            # Fetch up-to-date calendar  list from Google
            calendars = calendarService.getCalendars()

            calendarsJson = SettingsUtils.getCalendars()

            for widget in calendarScroll.winfo_children():
                widget.destroy()

            for calendar in calendars:
                calendarDayFrame = customtkinter.CTkFrame(master=calendarScroll, border_width=1)

                calendarDayFrame.pack(side=customtkinter.TOP, padx=20, pady=20, anchor='w', fill=customtkinter.BOTH,
                                      expand=True)

                checkbox = customtkinter.CTkCheckBox(calendarDayFrame, text=calendar['summary'], offvalue="false",
                                                     onvalue="true",
                                                     command=partial(toggleCalendar, calendar['id'], ))

                checkbox.pack(side=customtkinter.LEFT, padx=20, pady=20, fill=customtkinter.BOTH, expand=True, )

                if calendar['id'] in calendarsJson:
                    checkbox.select()

            SettingsUtils.setCalendars(list(calendarsJson))

        def toggleCalendar(calendarId: str):
            calendarsJson = SettingsUtils.getCalendars()

            if calendarId in calendarsJson:
                calendarsJson.remove(calendarId)
            else:
                calendarsJson.append(calendarId)

            SettingsUtils.setCalendars(calendarsJson)

        renderCalendars()
