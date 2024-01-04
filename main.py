import datetime
import os
from GoogleApiClient import GoogleApiClient
from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry
from utils.GoogleCalendarUtils import GoogleCalendarUtils
from services.GoogleCalendarService import GoogleCalendarService
from utils.ScreenUtils import ScreenUtils
from utils.SettingsUtils import SettingsUtils
import customtkinter
from components.SettingsFrame import SettingsTopLevel
from components.ShowEventsTopLevel import ShowEventsTopLevel

def fetchCalendarDays(startDate: datetime, endDate: datetime):
    googleApiClient = GoogleApiClient()
    googleCalendarService = GoogleCalendarService(googleApiClient)

    calendars = SettingsUtils.getCalendars()

    if len(calendars) == 0:
        return

    events = googleCalendarService.getMultipleCalendarEvents(calendars, startDate, endDate)

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
    clearBody()

    startDate = calendarEntryStart.get_date()
    endDate = calendarEntryEnd.get_date()

    timeDifferenceInDays = (endDate - startDate).days

    # The amount of day that needs to be processed is way too big,
    if timeDifferenceInDays > 365:
        msg = CTkMessagebox(title="Are you sure?", message="The timeframe is very large, it is recommended to use the "
                                                           "excel export function",
                            option_2="Continue",
                            option_1="Cancel",
                            icon="info")

        if msg.get() == "Cancel":
            return

    if timeDifferenceInDays < 0:
        CTkMessagebox(title="Error", message="Can't choose a end date which is before the start date!",
                      icon="cancel", option_1="Ok")
        return

    # generate all days within time period
    days = fetchCalendarDays(startDate, endDate)

    if days is None:
        CTkMessagebox(title="No calendars available", message="Configure calendars within settings", icon="cancel")
        return

    availableDaysScroll = customtkinter.CTkScrollableFrame(body, width, height)
    availableDaysScroll.pack()

    # progressbar = customtkinter.CTkProgressBar(availableDaysScroll, orientation="horizontal", mode='indeterminate', progress_color='green')
    # progressbar.configure(mode="indeterminate_speed")
    progressbar = customtkinter.CTkProgressBar(availableDaysScroll, progress_color='green')
    progressbar.pack(side=customtkinter.TOP, fill=customtkinter.BOTH)
    progressbar.set(0)
    # progressbar.start()
    # progressbar.pack(side=customtkinter.TOP)
    tksleep(app, .1)

    i = 0
    totalCount = len(days)

    for day, dayObject in days.items():
        available = dayObject['available']
        events = dayObject['events']

        date = datetime.datetime.strptime(day, "%d-%m-%Y")

        calendarDayFrame = customtkinter.CTkFrame(master=availableDaysScroll, border_width=1)

        dateLabel = customtkinter.CTkLabel(master=calendarDayFrame, text=date.strftime('%d-%m-%Y %A'))
        dateLabel.pack(side=customtkinter.LEFT, padx=10)

        # Decide color and status of availability
        color = 'red'
        status = 'Not Available'
        if available:
            color = 'green'
            status = 'Available'

        availableLabel = customtkinter.CTkLabel(master=calendarDayFrame, fg_color=color, text=status, corner_radius=100)
        availableLabel.pack(side=customtkinter.LEFT)

        calendarDayFrame.pack(side=customtkinter.TOP, padx=20, pady=5, anchor='w', fill=customtkinter.BOTH,
                              expand=True)
        if date.weekday() == 6:
            divider = customtkinter.CTkLabel(master=availableDaysScroll, text="", )
            divider.pack(side=customtkinter.TOP, padx=5, pady=20, anchor='w')

        # if len(events) == 0:
        #     continue

        eventsAlert = customtkinter.CTkFrame(master=calendarDayFrame)
        eventsAlert.pack(padx=10, pady=10, side=customtkinter.RIGHT)

        eventCountLabel = customtkinter.CTkLabel(master=eventsAlert, text='Events: ' + str(len(events)),
                                                 font=('Helvetica', 16, 'bold'))
        eventCountLabel.pack(side=customtkinter.TOP, anchor='w', pady=10, padx=10)

        for event in events:
            dateTimeFormat = GoogleCalendarService.GOOGLE_DATETIME_FORMAT
            keyValue = 'dateTime'
            # All day event, fuck your freetime
            if 'dateTime' not in event['start']:
                dateTimeFormat = GoogleCalendarService.GOOGLE_DATE_FORMAT
                keyValue = 'date'

            eventStartDate = datetime.datetime.strptime(event['start'][keyValue], dateTimeFormat)
            eventEndDate = datetime.datetime.strptime(event['end'][keyValue], dateTimeFormat)

            eventText = event['summary'] + ' '
            eventText += eventStartDate.strftime("%d-%m-%Y %H:%M:%S")
            eventText += " - "
            eventText += eventEndDate.strftime("%d-%m-%Y %H:%M:%S")

            availableLabel = customtkinter.CTkLabel(master=eventsAlert, text=eventText)
            availableLabel.pack(side=customtkinter.TOP, anchor='w', padx=10)

        # buttonShowDay = customtkinter.CTkButton(master=calendarDayFrame)
        # buttonShowDay.pack(padx=10, pady=10, side=customtkinter.LEFT)

        if i % 15:
            # Sleep to show progressbar step increase
            tksleep(app, .001)
            pbValue = i / totalCount
            progressbar.set(pbValue)

        i += 1

    # Remove progressbar
    #     progressbar.destroy()
    availableDaysScroll.winfo_children()[0].destroy()


def exportExcel():
    global exportFile
    # startDate = calendarEntryStart.get_date()
    # endDate = calendarEntryEnd.get_date()
    #
    # days = fetchCalendarDays(startDate, endDate)
    #
    # if days is None:
    #     CTkMessagebox(title="No calendars available", message="Configure calendars within settings", icon="cancel")
    #     return
    #
    # minimumTime = datetime.time(7, 30)
    # minimalIntervalBetween = 120
    #
    # excelFileName = "overview-calendar.xlsx"
    #
    # if os.path.exists(excelFileName):
    #     subprocess.call("TASKKILL /F /IM excel.exe", shell=True)
    #
    # GoogleCalendarUtils.createExcel(excelFileName, days, minimumTime, minimalIntervalBetween)
    # # Launch xlss file with OS default application
    # os.startfile(excelFileName)


def showSettings():
    clearBody()

    settingToplevel = SettingsTopLevel(body, width, height)
    settingToplevel.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=True)

    # settingToplevel.geometry(ScreenUtils.getGeometry(width, height, screen_width, screen_height))

    # tksleep(app, .1)

    # settingToplevel.focus()


def tksleep(self, time: float) -> None:
    """
    Emulating `time.sleep(seconds)`
    Created by TheLizzard, inspired by Thingamabobs
    """
    self.after(int(time * 1000), self.quit)
    self.mainloop()


def showEvents(events: list):
    if events is None:
        return
    boeie = ShowEventsTopLevel()
    # boeie.geometry(
    #     '%dx%d+%d+%d' % (width + 1, height + 1, x, y))

    tksleep(app, .1)

    boeie.focus()


def logOut():
    if os.path.exists("token.json"):
        os.remove("token.json")
        SettingsUtils.reset()



def clearBody():
    for widget in body.winfo_children():
        widget.destroy()


customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')

app = customtkinter.CTk()

width = 1280  # Width
height = 720  # Height
screen_width = app.winfo_screenwidth()  # Width of the screen
screen_height = app.winfo_screenheight()  # Height of the screen

app.geometry(ScreenUtils.getGeometry(width, height, screen_width, screen_height))
app.maxsize(width, height)
app.minsize(width, height)

app.title('Free time check')

navbar = customtkinter.CTkFrame(master=app, width=width, height=height)
navbar.pack(side=customtkinter.TOP)

labelStart = customtkinter.CTkLabel(master=navbar, text='Start date:')
labelStart.pack(padx=20, side=customtkinter.LEFT)

calendarEntryStart = DateEntry(navbar, width=30, bg="darkblue", fg="white", selectmode='day', date_pattern="dd-mm-y", )
calendarEntryStart.pack(padx=20, pady=20, side=customtkinter.LEFT)

labelEnd = customtkinter.CTkLabel(master=navbar, text='End date:')
labelEnd.pack(padx=20, side=customtkinter.LEFT)

calendarEntryEnd = DateEntry(navbar, width=30, bg="darkblue", fg="white", selectmode='day', date_pattern="dd-mm-y", )
calendarEntryEnd.set_date(datetime.date.today() + datetime.timedelta(days=7))
calendarEntryEnd.pack(padx=20, side=customtkinter.LEFT)

body = customtkinter.CTkFrame(master=app, width=width, height=height, )

body.pack(side=customtkinter.TOP, pady=10, expand=True, fill="both", )
dates = []

# Navbar function buttons wrapper
buttonFrame = customtkinter.CTkFrame(master=navbar)
buttonFrame.pack(padx=20, side=customtkinter.RIGHT)

button = customtkinter.CTkButton(master=buttonFrame, text="Check free time", command=submit)
button.pack(padx=5, side=customtkinter.LEFT)

excelButton = customtkinter.CTkButton(master=buttonFrame, text="Export to xls.format", command=exportExcel)
excelButton.pack(padx=5, side=customtkinter.LEFT)

settingButton = customtkinter.CTkButton(master=buttonFrame, text="Settings", command=showSettings)
settingButton.pack(padx=5, side=customtkinter.LEFT)

logOutButton = customtkinter.CTkButton(master=buttonFrame, text="Log out", command=logOut)
logOutButton.pack(padx=5, side=customtkinter.LEFT)

app.mainloop()
