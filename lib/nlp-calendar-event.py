import spacy
import dateparser
from datetime import datetime

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


def get_doc_entities(input: str):
    doc = nlp(user_input)
    return [(ent.text, ent.label_) for ent in doc.ents]


def parse_event_details(user_input):
    entities = get_doc_entities(user_input)

    # Initialize default values
    title = None
    place = None
    person = None
    date_time = None

    # print("Entities:", [(ent.text, ent.label_) for ent in doc.ents])

    # Extract entities
    for ent in doc.ents:
        if ent.label_ == "GPE" or ent.label_ == "LOC":
            place = ent.text
        elif ent.label_ == "PERSON":
            person = ent.text
        elif ent.label_ == "DATE" or ent.label_ == "TIME":
            date_time = dateparser.parse(ent.text)

    # Extract possible title
    title_tokens = []
    for token in doc:
        if not token.ent_type_ and not token.is_stop:
            title_tokens.append(token.text)
    title = " ".join(title_tokens)

    return {
        "title": title if title else "No Title Found",
        "person": person if person else "No Person Found",
        "place": place if place else "No Place Found",
        "date_time": date_time if date_time else "No Date/Time Found",
    }


# Example usage
user_input = "Schedule a meeting with John at Central Park next Tuesday at 3 PM"
event_details = parse_event_details(user_input)

print("Event Details:")
print(f"Title: {event_details['title']}")
print(f"Person: {event_details['person']}")
print(f"Place: {event_details['place']}")
print(f"Date and Time: {event_details['date_time']}")

doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
