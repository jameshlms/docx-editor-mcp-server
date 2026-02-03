from collections.abc import Callable, Mapping
from datetime import datetime
from enum import Enum
from json import dumps


class DateFormat(Enum):
    MONTH_YEAR_ABBR = "mon_year_abbr"  # Jan 2020
    MONTH_YEAR_FULL = "month_year_full"  # January 2020
    YEAR = "year"  # 2020
    YMD_SLASH = "ymd_slash"  # 01/2020
    DMY_SLASH = "dmy_slash"  # 2020/01
    MDY_SLASH = "mdy_slash"  # 15/01/2020
    YM_SLASH = "ym_slash"  # 2020/01/15
    MY_SLASH = "my_slash"  # 01/15/2020
    YMD_SLASH_2 = "ymd_slash_2"  # 15/01/20
    DMY_SLASH_2 = "dmy_slash_2"  # 20/01/15
    MDY_SLASH_2 = "mdy_slash_2"  # 15/01/20
    YM_SLASH_2 = "ym_slash_2"  # 20/01/15
    MY_SLASH_2 = "my_slash_2"  # 01/15/20
    YMD_DASH = "ymd_dash"  # 01/2020
    DMY_DASH = "dmy_dash"  # 2020/01
    MDY_DASH = "mdy_dash"  # 15/01/2020
    YM_DASH = "ym_dash"  # 2020/01/15
    MY_DASH = "my_dash"  # 01/15/2020
    YMD_DASH_2 = "ymd_dash_2"  # 15/01/20
    DMY_DASH_2 = "dmy_dash_2"  # 20/01/15
    MDY_DASH_2 = "mdy_dash_2"  # 15/01/20
    YM_DASH_2 = "ym_dash_2"  # 20/01/15
    MY_DASH_2 = "my_dash_2"  # 01/15/20

    @classmethod
    def as_json(cls) -> str:
        return dumps({format: format.value for format in cls})


format_date: Mapping[DateFormat, Callable[[datetime], str]] = {
    DateFormat.MONTH_YEAR_ABBR: lambda dt: dt.strftime("%b %Y"),
    DateFormat.MONTH_YEAR_FULL: lambda dt: dt.strftime("%B %Y"),
    DateFormat.YEAR: lambda dt: dt.strftime("%Y"),
    DateFormat.YMD_SLASH: lambda dt: dt.strftime("%Y/%m/%d"),
    DateFormat.DMY_SLASH: lambda dt: dt.strftime("%d/%m/%Y"),
    DateFormat.MDY_SLASH: lambda dt: dt.strftime("%m/%d/%Y"),
    DateFormat.YM_SLASH: lambda dt: dt.strftime("%Y/%m"),
    DateFormat.MY_SLASH: lambda dt: dt.strftime("%m/%Y"),
    DateFormat.YMD_SLASH_2: lambda dt: dt.strftime("%y/%m/%d"),
    DateFormat.DMY_SLASH_2: lambda dt: dt.strftime("%d/%m/%y"),
    DateFormat.MDY_SLASH_2: lambda dt: dt.strftime("%m/%d/%y"),
    DateFormat.YM_SLASH_2: lambda dt: dt.strftime("%y/%m"),
    DateFormat.MY_SLASH_2: lambda dt: dt.strftime("%m/%y"),
    DateFormat.YMD_DASH: lambda dt: dt.strftime("%Y-%m-%d"),
    DateFormat.DMY_DASH: lambda dt: dt.strftime("%d-%m-%Y"),
    DateFormat.MDY_DASH: lambda dt: dt.strftime("%m-%d-%Y"),
    DateFormat.YM_DASH: lambda dt: dt.strftime("%Y-%m"),
    DateFormat.MY_DASH: lambda dt: dt.strftime("%m-%Y"),
    DateFormat.YMD_DASH_2: lambda dt: dt.strftime("%y-%m-%d"),
    DateFormat.DMY_DASH_2: lambda dt: dt.strftime("%d-%m-%y"),
    DateFormat.MDY_DASH_2: lambda dt: dt.strftime("%m-%d-%y"),
    DateFormat.YM_DASH_2: lambda dt: dt.strftime("%y-%m"),
    DateFormat.MY_DASH_2: lambda dt: dt.strftime("%m-%y"),
}


def stringify_date(dt: datetime | None, date_format: DateFormat) -> str | None:
    if dt is None:
        return None
    if not isinstance(date_format, DateFormat):
        raise ValueError(f"Invalid date format: {date_format}")
    if not isinstance(dt, datetime):
        raise ValueError(f"Invalid date value: {dt}")
    return format_date[date_format](dt)
