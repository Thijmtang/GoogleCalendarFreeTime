import customtkinter
from CTkMessagebox import CTkMessagebox

from utils.ScreenUtils import ScreenUtils
from utils.SettingsUtils import SettingsUtils


class CalendarController(customtkinter.CTkFrame):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)

        # calendarsFrame = customtkinter.CTkFrame(master=self)
        # calendarsFrame.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=1)

        calendarScroll = customtkinter.CTkScrollableFrame(master=self)
        calendarScroll.pack(side=customtkinter.BOTTOM, fill=customtkinter.BOTH, expand=1)

        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight()  # Height of the screen

        def addNewCalendar():
            calendars = SettingsUtils.getCalendars()

            dialog = customtkinter.CTkInputDialog(text="Enter a Google calendar id", title="Add new calendar id")

            dialog.geometry(
                ScreenUtils.getGeometry(dialog.winfo_width(), dialog.winfo_height(), screen_width, screen_height))
            text = dialog.get_input()  # waits for input

            if text is None or text == "":
                return

            calendars.append(text)
            SettingsUtils.setCalendars(calendars)

            renderCalendars()

        labelCalendarSummary = customtkinter.CTkLabel(master=self,
                                                      text="This software needs calendar id's to be able to fetch events from google calendar ")
        labelCalendarSummary.pack(side=customtkinter.TOP, pady=10, anchor='w')

        newCalendarButton = customtkinter.CTkButton(master=self, text="Add calendar",
                                                    command=addNewCalendar, )
        newCalendarButton.pack(side=customtkinter.TOP, pady=10, anchor='w')

        def confirmDelete(calendar):
            calendars = SettingsUtils.getCalendars()

            msg = CTkMessagebox(title="Are you sure?",
                                message="You are about to delete '" + calendar + "'",
                                option_2="Yes",
                                option_1="Cancel",
                                icon="info")

            if msg.get() == "Cancel":
                return

            calendars.remove(calendar)
            SettingsUtils.setCalendars(calendars)
            renderCalendars()

        def renderCalendars():
            calendars = SettingsUtils.getCalendars()

            for widget in calendarScroll.winfo_children():
                widget.destroy()

            for calendar in calendars:
                calendarDayFrame = customtkinter.CTkFrame(master=calendarScroll, border_width=1)
                calendarLabel = customtkinter.CTkLabel(master=calendarDayFrame, text=calendar
                                                       , corner_radius=100)

                button = customtkinter.CTkButton(master=calendarDayFrame, text="Delete",
                                                 command=lambda: confirmDelete(calendar))

                button.pack(side=customtkinter.LEFT, padx=20, pady=20)
                calendarLabel.pack(side=customtkinter.LEFT, padx=20, pady=20)
                calendarDayFrame.pack(side=customtkinter.TOP, padx=20, pady=20, anchor='w')

        renderCalendars()