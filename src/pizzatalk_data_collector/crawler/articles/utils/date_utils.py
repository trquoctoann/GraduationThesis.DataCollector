from datetime import datetime, timedelta

import pytz
from dateutil.relativedelta import relativedelta


def convert_datetext_to_datetime(time_str):
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")


def fotmob_convert_to_datetime(fotmob_raw_date):
    if not fotmob_raw_date:
        return None
    utc_dt = datetime.fromisoformat(fotmob_raw_date).replace(tzinfo=pytz.utc)
    local_dt = utc_dt.astimezone(pytz.timezone("Asia/Bangkok"))
    return local_dt.strftime("%Y-%m-%d %H:%M:%S")


def get_current_time():
    timezone = pytz.timezone("Asia/Bangkok")
    current_time_utc7 = datetime.now(timezone)
    return current_time_utc7


def convert_fotmob_datetext_to_datetime(time_str):
    timezone = pytz.timezone("Asia/Bangkok")
    current_time = datetime.now(timezone).replace(microsecond=0)

    if time_str == "yesterday":
        adjusted_time = current_time - timedelta(days=1)
    else:
        number, unit = time_str.split()[:2]
        if number == "last":
            number = 1
        else:
            number = int(number)

        if unit.startswith("minute"):
            adjusted_time = current_time - timedelta(minutes=number)
        elif unit.startswith("hour"):
            adjusted_time = current_time - timedelta(hours=number)
        elif unit.startswith("day"):
            adjusted_time = current_time - timedelta(days=number)
        elif unit.startswith("week"):
            adjusted_time = current_time - timedelta(weeks=number)
        elif unit.startswith("month"):
            adjusted_time = current_time - relativedelta(months=number)
        elif unit.startswith("year"):
            adjusted_time = current_time - relativedelta(years=number)

    format_adjusted_time = adjusted_time.strftime("%Y-%m-%d %H:%M:%S")
    return convert_datetext_to_datetime(format_adjusted_time)
