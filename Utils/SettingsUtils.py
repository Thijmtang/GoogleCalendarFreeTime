import ast
import os
import string


class SettingsUtils:
    Settings = None

    @staticmethod
    def getCalendars() -> list:
        return SettingsUtils.__getValue("calendars")

    @staticmethod
    def getCalendars() -> list:
        return SettingsUtils.__getValue("calendars")

    @staticmethod
    def getSummaryBannedKeywords() -> list:
        return SettingsUtils.__getValue("summaryKeywords")

    @staticmethod
    def getStartDate() -> string:
        return SettingsUtils.__getValue("startDate")

    @staticmethod
    def getEndDate() -> string:
        return SettingsUtils.__getValue("endDate")
    @staticmethod
    def getSettings() -> list:
        # Already loaded the file during runtime, no need to redo
        if SettingsUtils.Settings is not None:
            return SettingsUtils.Settings

        if not os.path.exists('./settings.json'):
            raise Exception('No settings.json file found!')

        settings = open('./settings.json', 'r').read()
        if len(settings) == 0:
            raise Exception('settings.json is not configured properly')

        SettingsUtils.Settings = ast.literal_eval(settings)

        return SettingsUtils.Settings

    # Waarom werkt private zo PYTHON?????  🤢
    @staticmethod
    def __getValue(key: string) -> list:
        settings = SettingsUtils.getSettings()
        if settings[key] is None:
            raise Exception(key + " is not defined within settings.json!")

        return settings[key]