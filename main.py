import datetime
import os

from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry
from GoogleApiClient import GoogleApiClient
from Utils.GoogleCalendarUtils import GoogleCalendarUtils
from Services.GoogleCalendarService import GoogleCalendarService
from Utils.SettingsUtils import SettingsUtils
import customtkinter

# locale.setlocale(locale.LC_ALL, "nl_NL")

customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')

app = customtkinter.CTk()

width = 1280  # Width
height = 720  # Height

screen_width = app.winfo_screenwidth()  # Width of the screen
screen_height = app.winfo_screenheight()  # Height of the screen

# Calculate Starting X and Y coordinates for Window
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)

app.geometry(
    '%dx%d+%d+%d' % (width, height, x, y))
app.title('Free time check')

navbar = customtkinter.CTkFrame(master=app, width=width, height=height)
navbar.pack(side=customtkinter.TOP)
# Use CTkLabel instead of tkinter Label
labelStart = customtkinter.CTkLabel(master=navbar, text='Start date:')
labelStart.pack(padx=20, side=customtkinter.LEFT)

calendarEntryStart = DateEntry(navbar, width=30, bg="darkblue", fg="white", selectmode='day', )
calendarEntryStart.pack(padx=20, pady=20, side=customtkinter.LEFT)

labelEnd = customtkinter.CTkLabel(master=navbar, text='End date:')
labelEnd.pack(padx=20, side=customtkinter.LEFT)

calendarEntryEnd = DateEntry(navbar, width=30, bg="darkblue", fg="white", selectmode='day')
calendarEntryEnd.pack(padx=20, side=customtkinter.LEFT)

body = customtkinter.CTkScrollableFrame(master=app, width=width, height=height, )

body.pack(side=customtkinter.TOP, pady=10)

dates = []


def fetchCalendarDays(startDate: datetime, endDate: datetime):
    googleApiClient = GoogleApiClient()
    googleCalendarService = GoogleCalendarService(googleApiClient)

    events = googleCalendarService.getMultipleCalendarEvents(SettingsUtils.getCalendars(), startDate, endDate)

    minimumTime = datetime.time(7, 30)
    minimalIntervalBetween = 120

    # Process events
    return GoogleCalendarUtils.getAvailabilityCalendarDays(
        start=startDate,
        end=endDate,
        minimumTime=minimumTime,
        minimalIntervalBetweenInMinutes=minimalIntervalBetween,
        events=events
    )


def submit():
    startDate = calendarEntryStart.get_date()
    endDate = calendarEntryEnd.get_date()

    timeDifferenceInDays = (endDate - startDate).days

    # The amount of day that needs to be processed is way too big,
    if timeDifferenceInDays > 365:
        CTkMessagebox(title="Warning", message="The timeframe too is large, please use the excel export function",
                      icon="warning")
        return

    # generate all days within time period
    days = fetchCalendarDays(startDate, endDate)

    for widget in body.winfo_children():
        widget.destroy()

    progressbar = customtkinter.CTkProgressBar(body, orientation="horizontal")
    progressbar.configure(mode="indeterminate")
    progressbar.start()
    progressbar.pack(side=customtkinter.BOTTOM)

    tksleep(app, 1)

    for day, available in days.items():
        progressbar.step()

        date = datetime.datetime.strptime(day, "%d-%m-%Y")

        frame = customtkinter.CTkFrame(master=body)

        dateLabel = customtkinter.CTkLabel(master=frame, text=date.strftime('%d-%m-%Y %A'))
        dateLabel.pack(side=customtkinter.LEFT)

        color = 'red'
        availableText = 'Not Available'
        if available:
            color = 'green'
            availableText = 'Available'

        availableLabel = customtkinter.CTkLabel(master=frame, fg_color=color, text=availableText, corner_radius=100)
        availableLabel.pack(side=customtkinter.LEFT, padx=20)

        frame.pack(side=customtkinter.TOP, padx=5, pady=5, anchor='w')
        if date.weekday() == 6:
            divider = customtkinter.CTkLabel(master=body, text="", )
            divider.pack(side=customtkinter.TOP, padx=5, pady=5, anchor='w')

    # Remove progressbar
    body.winfo_children()[0].destroy()


def exportExcel():
    startDate = calendarEntryStart.get_date()
    endDate = calendarEntryEnd.get_date()

    for widget in body.winfo_children():
        widget.destroy()

    progressbar = customtkinter.CTkProgressBar(body, orientation="horizontal")
    progressbar.configure(mode="indeterminate")
    progressbar.start()
    progressbar.pack(side=customtkinter.BOTTOM)

    tksleep(app, 1)

    days = fetchCalendarDays(startDate, endDate)
    minimumTime = datetime.time(7, 30)
    minimalIntervalBetween = 120

    excelFileName = "overview-calendar.xlsx"

    GoogleCalendarUtils.createExcel(excelFileName, days, minimumTime, minimalIntervalBetween)

    os.system("start EXCEL.EXE " + excelFileName)

    # Remove progressbar
    body.winfo_children()[0].destroy()


def tksleep(self, time: float) -> None:
    """
    Emulating `time.sleep(seconds)`
    Created by TheLizzard, inspired by Thingamabobs
    """
    self.after(int(time * 1000), self.quit)
    self.mainloop()


buttonFrame = customtkinter.CTkFrame(master=navbar)
buttonFrame.pack(padx=20, side=customtkinter.RIGHT)

excelButton = customtkinter.CTkButton(master=buttonFrame, text="Export into Excel", command=exportExcel)

excelButton.pack(padx=5, side=customtkinter.LEFT)

button = customtkinter.CTkButton(master=buttonFrame, text="Check free time", command=submit)
button.pack(padx=5, side=customtkinter.LEFT)

settingButton = customtkinter.CTkButton(master=buttonFrame, text="Settings", command=exportExcel)
settingButton.pack(padx=5, side=customtkinter.LEFT)

app.mainloop(

)
