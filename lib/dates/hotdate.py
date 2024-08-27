import re
import pytz
from datetime import datetime, time
from dateutil.relativedelta import relativedelta

from lib.clients.spacy import nlp


def parse_relative_date(date_str, base_date):
    date_str = date_str.lower()

    # Dictionary for day of week mapping
    days = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    # Handle "next" expressions
    if "next" in date_str:
        if "month" in date_str:
            next_month = base_date + relativedelta(months=1)
            day_match = re.search(r"(\d+)(?:st|nd|rd|th)?", date_str)
            if day_match:
                day = int(day_match.group(1))
                return next_month.replace(
                    day=min(day, (next_month + relativedelta(months=1, days=-1)).day)
                )
            return next_month
        elif any(day in date_str for day in days):
            for day, offset in days.items():
                if day in date_str:
                    return base_date + relativedelta(
                        days=(offset - base_date.weekday() + 7) % 7
                    )
        elif "week" in date_str:
            return base_date + relativedelta(weeks=1)

    # Handle "this" expressions
    elif "this" in date_str:
        if any(day in date_str for day in days):
            for day, offset in days.items():
                if day in date_str:
                    days_ahead = offset - base_date.weekday()
                    if days_ahead <= 0:
                        days_ahead += 7
                    return base_date + relativedelta(days=days_ahead)

    # Handle "tomorrow" and "today"
    elif "tomorrow" in date_str:
        return base_date + relativedelta(days=1)
    elif "today" in date_str:
        return base_date

    # Handle month names
    months = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]
    for i, month in enumerate(months):
        if month in date_str:
            day_match = re.search(r"(\d+)(?:st|nd|rd|th)?", date_str)
            if day_match:
                day = int(day_match.group(1))
                date = base_date.replace(month=i + 1, day=min(day, 31))
                return date if date > base_date else date.replace(year=date.year + 1)

    # If no match found, return None
    return None


def parse_time(time_str):
    time_str = time_str.lower()
    match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", time_str)
    if match:
        hour, minute, period = match.groups()
        hour = int(hour)
        minute = int(minute) if minute else 0
        if period == "pm" and hour != 12:
            hour += 12
        elif period == "am" and hour == 12:
            hour = 0
        return time(hour, minute)
    return None


def extract_date_time(text, user_timezone):
    doc = nlp(text)

    date_entity = None
    time_entity = None

    for ent in doc.ents:
        if ent.label_ == "DATE" and not date_entity:
            date_entity = ent.text
        elif ent.label_ == "TIME" and not time_entity:
            time_entity = ent.text

    user_tz = pytz.timezone(user_timezone)
    now = datetime.now(user_tz)

    parsed_date = (
        parse_relative_date(date_entity, now.date()) if date_entity else now.date()
    )
    parsed_time = parse_time(time_entity) if time_entity else now.time()

    if parsed_date and parsed_time:
        dt = datetime.combine(parsed_date, parsed_time)
        dt = user_tz.localize(dt)

        # If the resulting datetime is in the past and doesn't contain "last", move it to the future
        if dt < now and "last" not in text.lower():
            if "next" not in text.lower():
                dt += relativedelta(days=1)
            else:
                dt += relativedelta(weeks=1)

        return dt

    return None
