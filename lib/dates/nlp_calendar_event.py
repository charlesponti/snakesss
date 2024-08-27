from shlex import join

from lib.clients.spacy import nlp
from lib.dates.test_hotdate import extract_date_time


def get_doc_entities(input: str):
    doc = nlp(input)
    return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]


def parse_event_details(user_input, user_timezone):
    entities = nlp(user_input)

    # Initialize default values
    title = None
    place = None
    person = None
    date_time = None

    # Extract entities
    for ent in entities.ents:
        if ent.label_ == "GPE" or ent.label_ == "LOC":
            place = ent.text
        elif ent.label_ == "PERSON":
            person = ent.text

    # Extract possible title
    title_tokens = []
    for token in entities:
        if not token.ent_type_ and not token.is_stop:
            title_tokens.append(token.text)
    title = " ".join(title_tokens)

    date_time = extract_date_time(
        join(
            [
                ent.text
                for ent in entities.ents
                if ent.label_ == "DATE" or ent.label_ == "TIME"
            ]
        ),
        user_timezone,
    )

    return {
        "title": title if title else "No Title Found",
        "person": person if person else "No Person Found",
        "place": place if place else "No Place Found",
        "date_time": date_time if date_time else "No Date/Time Found",
        # ent.label_: ent.text for ent in entities.ents if value is not None
    }
