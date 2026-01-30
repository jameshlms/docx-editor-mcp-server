from collections.abc import Callable, Mapping
from datetime import datetime
from enum import Enum
from json import dumps


class DateFormat(Enum):
    MON_YEAR = "Mon Year"  # Jan 2020
    MONTH_YEAR = "Month Year"  # January 2020
    YYYY = "YYYY"  # 2020
    MM_YYYY = "MM/YYYY"  # 01/2020
    YYYY_MM = "YYYY/MM"  # 2020/01
    DD_MM_YYYY = "DD/MM/YYYY"  # 15/01/2020
    YYYY_MM_DD = "YYYY/MM/DD"  # 2020/01/15
    MM_DD_YYYY = "MM/DD/YYYY"  # 01/15/2020
    DD_MM_YY = "DD/MM/YY"  # 15/01/20
    YY_MM_DD = "YY/MM/DD"  # 20/01/15
    MM_DD_YY = "MM/DD/YY"  # 01/15/20

    @classmethod
    def as_json(cls) -> str:
        return dumps({format: format.value for format in cls})


format_date: Mapping[DateFormat, Callable[[datetime], str]] = {
    DateFormat.MON_YEAR: lambda dt: dt.strftime("%b %Y"),
    DateFormat.MONTH_YEAR: lambda dt: dt.strftime("%B %Y"),
    DateFormat.YYYY: lambda dt: dt.strftime("%Y"),
    DateFormat.MM_YYYY: lambda dt: dt.strftime("%m/%Y"),
    DateFormat.YYYY_MM: lambda dt: dt.strftime("%Y/%m"),
    DateFormat.DD_MM_YYYY: lambda dt: dt.strftime("%d/%m/%Y"),
    DateFormat.YYYY_MM_DD: lambda dt: dt.strftime("%Y/%m/%d"),
    DateFormat.MM_DD_YYYY: lambda dt: dt.strftime("%m/%d/%Y"),
    DateFormat.DD_MM_YY: lambda dt: dt.strftime("%d/%m/%y"),
    DateFormat.YY_MM_DD: lambda dt: dt.strftime("%y/%m/%d"),
    DateFormat.MM_DD_YY: lambda dt: dt.strftime("%m/%d/%y"),
}


def stringify_date(dt: datetime | None, date_format: DateFormat) -> str | None:
    if dt is None:
        return None
    if not isinstance(date_format, DateFormat):
        raise ValueError(f"Invalid date format: {date_format}")
    if not isinstance(dt, datetime):
        raise ValueError(f"Invalid date value: {dt}")
    return format_date[date_format](dt)
