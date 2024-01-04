import ast
import json
import os
import string
from typing import Any, Dict


class SettingsUtils:
    Settings = None
    FILEPATH = 'settings.json'
    @staticmethod
    def getCalendars() -> list:
        return SettingsUtils.__getValue("calendars")

    @staticmethod
    def setCalendars(calendars: list) -> None:
        SettingsUtils.getSettings()["calendars"] = calendars

        SettingsUtils.__updateSettings()

    @staticmethod
    def setSummaryBannedKeywords(keywords: list) -> None:
        SettingsUtils.getSettings()["summaryKeywords"] = keywords

        SettingsUtils.__updateSettings()

    @staticmethod
    def getSummaryBannedKeywords() -> dict[Any, Any]:
        return SettingsUtils.__getValue("summaryKeywords")

    @staticmethod
    def getStartDate() -> string:
        return SettingsUtils.__getValue("startDate")

    @staticmethod
    def getEndDate() -> string:
        return SettingsUtils.__getValue("endDate")

    @staticmethod
    def getSettings() -> dict[str, Any]:
        # Already loaded the file during runtime, no need to redo
        if SettingsUtils.Settings is not None:
            return SettingsUtils.Settings

        if not os.path.exists('./'+SettingsUtils.FILEPATH):
            SettingsUtils.reset()
            # raise Exception('No settings.json file found!')

        settings = open('./settings.json', 'r').read()
        # if len(settings) == 0:
        #     raise Exception('settings.json is not configured properly')


        try:
            SettingsUtils.Settings = ast.literal_eval(settings)
            return SettingsUtils.Settings
        except:
            SettingsUtils.reset()
            return SettingsUtils.getSettings()

    @staticmethod
    def __getValue(key: string) -> list:
        settings = SettingsUtils.getSettings()
        if key not in settings:
            return []

        return settings[key]

    @staticmethod
    def __updateSettings() -> None:
        oldSettings = SettingsUtils.getSettings()
        SettingsUtils.Settings = None

        # Writing to sample.json
        with open('settings.json', 'w') as outfile:
            json.dump(oldSettings, outfile)

        outfile.close()

        SettingsUtils.getSettings()

    @staticmethod
    def reset():
        with open('settings.json', 'w') as json_file:
            json.dump({}, json_file)