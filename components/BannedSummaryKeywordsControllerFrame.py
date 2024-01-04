from functools import partial

import customtkinter
from CTkMessagebox import CTkMessagebox

from utils.ScreenUtils import ScreenUtils
from utils.SettingsUtils import SettingsUtils


class BannedSummaryKeywordsController(customtkinter.CTkFrame):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)


        keywordScroll = customtkinter.CTkScrollableFrame(master=self)
        keywordScroll.pack(side=customtkinter.BOTTOM, fill=customtkinter.BOTH, expand=1)

        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight()  # Height of the screen

        def addNewKeyword():
            keywords = SettingsUtils.getSummaryBannedKeywords()

            dialog = customtkinter.CTkInputDialog(title="Add new keyword", text="")

            dialog.geometry(
                ScreenUtils.getGeometry(720, dialog.winfo_height(), screen_width, screen_height))
            text = dialog.get_input()  # waits for input

            if text is None or text == "":
                return

            keywords.append(text)
            SettingsUtils.setSummaryBannedKeywords(keywords)

            renderKeywords()

        labelKeywordsSummary = customtkinter.CTkLabel(master=self,
                                                      text="Keywords when found in the summary of events, will be counted as full day events, marking availability as false")
        labelKeywordsSummary.pack(side=customtkinter.TOP, pady=10, anchor='w')

        newKeywordButton = customtkinter.CTkButton(master=self, text="Add Keyword",
                                                    command=addNewKeyword, )
        newKeywordButton.pack(side=customtkinter.TOP, pady=10, anchor='w')

        def confirmDelete(keyword):
            keywords = SettingsUtils.getSummaryBannedKeywords()

            msg = CTkMessagebox(title="Are you sure?",
                                message="You are about to delete '" + keyword + "'",
                                option_2="Yes",
                                option_1="Cancel",
                                icon="info")

            if msg.get() != "Yes":
                return

            keywords.remove(keyword)
            SettingsUtils.setSummaryBannedKeywords(keywords)

            renderKeywords()

        def renderKeywords():
            keywords = SettingsUtils.getSummaryBannedKeywords()

            for widget in keywordScroll.winfo_children():
                widget.destroy()

            for keyword in keywords:
                keywordFrame = customtkinter.CTkFrame(master=keywordScroll, border_width=1)
                keywordLabel = customtkinter.CTkLabel(master=keywordFrame, text=keyword
                                                      , corner_radius=100)

                button = customtkinter.CTkButton(master=keywordFrame, text="Delete",
                                                 command=partial(confirmDelete, keyword))

                button.pack(side=customtkinter.LEFT, padx=20, pady=20)
                keywordLabel.pack(side=customtkinter.LEFT, padx=20, pady=20)
                keywordFrame.pack(side=customtkinter.TOP, padx=20, pady=20, anchor='w')

        renderKeywords()