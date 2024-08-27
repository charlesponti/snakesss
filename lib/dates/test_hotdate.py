import unittest
from freezegun import freeze_time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from lib.dates.hotdate import extract_date_time


class TestDateExtraction(unittest.TestCase):
    def setUp(self):
        self.user_timezone = "America/New_York"
        self.frozen_date = datetime(
            2023, 6, 15, 10, 30
        )  # Thursday, June 15, 2023, 10:30 AM

    def assert_datetime(self, result, expected_date, expected_time):
        self.assertEqual(result.date(), expected_date)
        self.assertEqual(result.time(), expected_time)

    @freeze_time("2023-06-15 10:30:00")
    def test_next_day(self):
        result = extract_date_time(
            "Schedule a meeting tomorrow at 2 PM", self.user_timezone
        )
        expected = self.frozen_date + relativedelta(days=1, hour=14, minute=0)
        self.assert_datetime(result, expected.date(), expected.time())

    @freeze_time("2023-06-15 10:30:00")
    def test_next_tuesday(self):
        result = extract_date_time(
            "Schedule a meeting next Tuesday at 3 PM", self.user_timezone
        )
        expected = self.frozen_date + relativedelta(days=5, hour=15, minute=0)
        self.assert_datetime(result, expected.date(), expected.time())

    @freeze_time("2023-06-15 10:30:00")
    def test_next_month(self):
        result = extract_date_time(
            "The report is due next month on the 15th", self.user_timezone
        )
        expected = self.frozen_date + relativedelta(months=1, hour=10, minute=30)
        self.assert_datetime(result, expected.date(), expected.time())

    @freeze_time("2023-06-15 10:30:00")
    def test_this_friday(self):
        result = extract_date_time(
            "Call Sarah this Friday at 11 AM", self.user_timezone
        )
        expected = self.frozen_date + relativedelta(days=1, hour=11, minute=0)
        self.assert_datetime(result, expected.date(), expected.time())

    @freeze_time("2023-06-15 10:30:00")
    def test_specific_date(self):
        result = extract_date_time(
            "The conference is scheduled for June 1st at 9 AM", self.user_timezone
        )
        expected = datetime(
            2024, 6, 1, 9, 0
        )  # Note: This should be next year as June 1st has passed
        self.assert_datetime(result, expected.date(), expected.time())

    @freeze_time("2023-06-15 10:30:00")
    def test_time_only(self):
        result = extract_date_time("Set a reminder for 9am", self.user_timezone)
        expected = self.frozen_date.replace(hour=9, minute=0)
        self.assert_datetime(result, expected.date(), expected.time())

    @freeze_time("2023-06-15 10:30:00")
    def test_next_wednesday(self):
        result = extract_date_time(
            "Meet me next Wednesday at 2:30pm", self.user_timezone
        )
        expected = self.frozen_date + relativedelta(days=6, hour=14, minute=30)
        self.assert_datetime(result, expected.date(), expected.time())

    @freeze_time("2023-06-15 10:30:00")
    def test_last_day_next_month(self):
        result = extract_date_time(
            "The event is on the last day of next month", self.user_timezone
        )
        expected = (self.frozen_date + relativedelta(months=1)).replace(
            day=31, hour=10, minute=30
        )
        self.assert_datetime(result, expected.date(), expected.time())

    @freeze_time("2023-06-15 10:30:00")
    def test_this_weekend(self):
        result = extract_date_time("Let's catch up this weekend", self.user_timezone)
        expected = self.frozen_date + relativedelta(
            days=2
        )  # Assuming weekend starts on Saturday
        self.assert_datetime(result, expected.date(), self.frozen_date.time())

    @freeze_time("2023-06-15 10:30:00")
    def test_next_year(self):
        result = extract_date_time(
            "The annual meeting is scheduled for next year on March 15th",
            self.user_timezone,
        )
        expected = datetime(2024, 3, 15, 10, 30)
        self.assert_datetime(result, expected.date(), expected.time())

    @freeze_time("2023-06-15 10:30:00")
    def test_day_after_tomorrow(self):
        result = extract_date_time(
            "Let's meet the day after tomorrow at noon", self.user_timezone
        )
        expected = self.frozen_date + relativedelta(days=2, hour=12, minute=0)
        self.assert_datetime(result, expected.date(), expected.time())

    @freeze_time("2023-06-15 10:30:00")
    def test_next_week(self):
        result = extract_date_time(
            "The presentation is scheduled for next week", self.user_timezone
        )
        expected = self.frozen_date + relativedelta(weeks=1)
        self.assert_datetime(result, expected.date(), self.frozen_date.time())

    @freeze_time("2023-06-15 10:30:00")
    def test_end_of_month(self):
        result = extract_date_time(
            "Submit the report by the end of this month", self.user_timezone
        )
        expected = self.frozen_date.replace(
            day=30, hour=23, minute=59
        )  # June has 30 days
        self.assert_datetime(result, expected.date(), expected.time())

    @freeze_time("2023-06-15 10:30:00")
    def test_invalid_input(self):
        result = extract_date_time(
            "This text contains no date or time information", self.user_timezone
        )
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
