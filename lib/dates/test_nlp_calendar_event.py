import unittest
from datetime import datetime
import pytz
from freezegun import freeze_time
import spacy

# Import the functions you want to test
from lib.dates.nlp_calendar_event import (
    parse_event_details,
    get_doc_entities,
    extract_date_time,
)


class TestNLPFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load spaCy model once for all tests
        cls.nlp = spacy.load("en_core_web_sm")

    def setUp(self):
        self.user_timezone = "America/New_York"
        self.frozen_date = datetime(
            2023, 6, 15, 10, 30, tzinfo=pytz.timezone(self.user_timezone)
        )

    @freeze_time("2023-06-15 10:30:00")
    def test_parse_event_details(self):
        input_text = "Schedule a meeting with John at Central Park next Tuesday at 3 PM"
        result = parse_event_details(input_text, self.user_timezone)

        self.assertEqual(result["person"], "John")
        self.assertEqual(result["place"], "Central Park")
        self.assertEqual(
            result["date_time"].strftime("%Y-%m-%d %H:%M:%S"), "2023-06-20 15:00:00"
        )
        self.assertIn("meeting", result["title"].lower())

    def test_get_doc_entities(self):
        input_text = "Apple is looking at buying U.K. startup for $1 billion"
        result = get_doc_entities(input_text)

        expected_entities = {"Apple": "ORG", "U.K.": "GPE", "$1 billion": "MONEY"}

        for entity in result:
            self.assertIn(entity["text"], expected_entities)
            self.assertEqual(entity["label"], expected_entities[entity["text"]])

    @freeze_time("2023-06-15 10:30:00")
    def test_extract_date_time(self):
        test_cases = [
            ("Schedule a meeting next Tuesday at 3 PM", "2023-06-20 15:00:00"),
            ("Let's have dinner tomorrow at 7 PM", "2023-06-16 19:00:00"),
            ("The report is due next month on the 15th", "2023-07-15 10:30:00"),
            ("Call Sarah this Friday at 11 AM", "2023-06-16 11:00:00"),
            ("The conference is scheduled for June 1st at 9 AM", "2024-06-01 09:00:00"),
            ("Set a reminder for 9am", "2023-06-16 09:00:00"),
            ("Meet me next Wednesday at 2:30pm", "2023-06-21 14:30:00"),
            ("The event is on the last day of next month", "2023-07-31 10:30:00"),
            ("Let's catch up this weekend", "2023-06-17 10:30:00"),
        ]

        for input_text, expected_output in test_cases:
            with self.subTest(input=input_text):
                result = extract_date_time(input_text, self.user_timezone)
                expected = datetime.strptime(
                    expected_output, "%Y-%m-%d %H:%M:%S"
                ).replace(tzinfo=pytz.timezone(self.user_timezone))
                self.assertEqual(result, expected)

    def test_complex_inputs(self):
        test_cases = [
            (
                "Schedule a video call with Sarah and Mike for next Monday at 2:30 PM at the virtual conference room",
                {
                    "person": "Sarah",  # Note: It might pick either Sarah or Mike
                    "place": "virtual conference room",
                    "date_time": datetime(
                        2023, 6, 19, 14, 30, tzinfo=pytz.timezone(self.user_timezone)
                    ),
                },
            ),
            (
                "Remind me to buy groceries from Walmart on 5th Avenue this Saturday morning",
                {
                    "place": "Walmart",  # or potentially "5th Avenue"
                    "date_time": datetime(
                        2023, 6, 17, 10, 30, tzinfo=pytz.timezone(self.user_timezone)
                    ),
                },
            ),
            (
                "Book a flight to New York for July 4th at 9 AM",
                {
                    "place": "New York",
                    "date_time": datetime(
                        2023, 7, 4, 9, 0, tzinfo=pytz.timezone(self.user_timezone)
                    ),
                },
            ),
        ]

        for input_text, expected in test_cases:
            with self.subTest(input=input_text):
                result = parse_event_details(input_text, self.user_timezone)
                for key, value in expected.items():
                    if isinstance(value, datetime):
                        self.assertEqual(
                            result[key].strftime("%Y-%m-%d %H:%M:%S"),
                            value.strftime("%Y-%m-%d %H:%M:%S"),
                        )
                    else:
                        self.assertEqual(result[key], value)

    @freeze_time("2023-06-15 10:30:00")
    def test_invalid_inputs(self):
        result = parse_event_details(
            "This input has no recognizable entities", self.user_timezone
        )
        self.assertEqual(result["person"], "No Person Found")
        self.assertEqual(result["place"], "No Place Found")
        self.assertIsInstance(
            result["date_time"], datetime
        )  # It should default to current time

        result = extract_date_time(
            "This is not a valid date string", self.user_timezone
        )
        self.assertEqual(
            result, self.frozen_date
        )  # It should return the current date/time


if __name__ == "__main__":
    unittest.main()
