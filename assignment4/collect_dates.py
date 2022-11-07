import re
from typing import Tuple

## -- Task 3 (IN3110 optional, IN4110 required) -- ##
# create array with all names of months
month_names_short = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
    ]

day = r"((?:0?[1-9])|(?:[12][0-9])|(?:3[01]))"

def get_date_patterns() -> Tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day
    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """

    # Regex to capture days, months and years with numbers
    # year should accept a 4-digit number between at least 1000-2029
    year = r"([012][0-9]{3})"
    # month should accept month names or month numbers
    month = r"((?:(?:Jan)|(?:Feb)|(?:Mar)|(?:Apr)|(?:May)|(?:Jun)|(?:Jul)|(?:Aug)|(?:Sep)|(?:Oct)|(?:Nov)|(?:Dec))[a-z]{0,6})"
    # day should be a number, which may or may not be zero-padded
    day = r"((?:0?[1-9])|(?:[12][0-9])|(?:3[01]))"

    return year, month, day


def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09'.

    You don't need to use this function,
    but you may find it useful.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    # If already digit do nothing
    if s.isdigit():
        s = zero_pad(s)
        return s
    # Convert to number as string'
    else:
        i = 0
        while i < len(month_names_short):
            if len(s) > 3:
                s = s[0 : 3]
            if month_names_short[i] == s:
                j = i + 1
                j =zero_pad(str(j))
                return j
            i += 1


def zero_pad(n: str):
    """zero-pad a number string

    turns '2' into '02'

    You don't need to use this function,
    but you may find it useful.
    """
    if len(n) == 2:
        return n
    if len(n) == 1:
        return "0" + n


def find_dates(text: str, output: str = None) -> list:
    """Finds all dates in a text using reg ex

    arguments:
        text (string): A string containing html text from a website
    return:
        results (list): A list with all the dates found
    """
    year, month, day = get_date_patterns()

    # Date on format YYYY/MM/DD - ISO
    ISO = fr"\b{year}-((?:0[1-9])|(?:1[0-2]))-((?:0[1-9])|(?:[12][0-9])|(?:3[01]))\b"

    # Date on format DD/MM/YYYY
    DMY = fr"\b{day}? ?{month} {year}\b"

    # Date on format MM/DD/YYYY
    MDY = fr"\b{month} ?{day}?, {year}\b"

    # Date on format YYYY/MM/DD
    YMD = fr"\b{year} {month} {day}\b"

    # list with all supported formats
    formats = [ISO, DMY, MDY, YMD]
    dates = []

    # find all dates in any format in text
    for format in formats:
        if format == ISO:
            dates += [f"{day[0]}/{day[1]}/{day[2]}"
                for day in re.findall(ISO, text, flags=re.M)]
        if format == DMY:
            dates += [f"{day[2]}/{convert_month(day[1])}/{zero_pad(day[0])}"
                if len(day[0]) != 0 else f"{day[2]}/{convert_month(day[1])}"
                for day in re.findall(DMY, text, flags=re.M)]
        if format == MDY:
            dates += [f"{day[2]}/{convert_month(day[0])}/{zero_pad(day[1])}"
                if len(day[1]) != 0 else f"{day[2]}/{convert_month(day[0])}"
                for day in re.findall(MDY, text, flags=re.M)]
        if format == YMD:
            dates += [f"{day[0]}/{convert_month(day[1])}/{zero_pad(day[2])}"
                if len(day[2]) != 0 else f"{day[0]}/{convert_month(day[1])}"
                for day in re.findall(YMD, text, flags=re.M)]


    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        out = open(output, "w")

        for text in dates:
            out.write(text + '\n')
        out.close()

    return dates
