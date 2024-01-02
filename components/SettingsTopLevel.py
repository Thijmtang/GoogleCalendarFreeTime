import string

import customtkinter
from CTkMessagebox import CTkMessagebox

from components.BannedSummaryKeywordsController import BannedSummaryKeywordsController
from utils.ScreenUtils import ScreenUtils
from utils.SettingsUtils import SettingsUtils
from components.CalendarController import CalendarController


class SettingsTopLevel(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.winfo_toplevel()

        self.title("Settings")

        tabview = customtkinter.CTkTabview(self)
        tabview.pack(fill=customtkinter.BOTH, expand=1)

        tabview.add("Calendar's")  # add tab at the end
        tabview.add("Summary banned keywords")  # add tab at the end

        calendar = CalendarController(tabview.tab("Calendar's"))
        calendar.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=1)

        keywords = BannedSummaryKeywordsController(tabview.tab("Summary banned keywords"))
        keywords.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=1)



