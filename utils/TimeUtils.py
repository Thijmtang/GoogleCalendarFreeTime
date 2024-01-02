import datetime


class TimeUtils:
    @staticmethod
    def addMinutesToTime(time: datetime.time, minutes: int) -> datetime.time:
        current_datetime = datetime.datetime.combine(datetime.datetime.today(), time)

        # Add 30 minutes to the current time
        new_datetime = current_datetime + datetime.timedelta(minutes=minutes)

        # Extract the time from the new datetime object
        return new_datetime.time()