import customtkinter

from utils.SettingsUtils import SettingsUtils


class ShowEventsTopLevel(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.winfo_toplevel()

        self.title("Events")


        calendarScroll = customtkinter.CTkScrollableFrame(master=self)
        calendarScroll.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=1)

        calendars = SettingsUtils.getCalendars()
        for calendar in calendars:

            calendarFrame = customtkinter.CTkFrame(master=calendarScroll,)
            calendarLabel = customtkinter.CTkLabel(master=calendarScroll, text=calendar
                                                   , corner_radius=100)
            calendarLabel.pack(side=customtkinter.TOP)
