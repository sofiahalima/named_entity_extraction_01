import spacy
import os

nlp = spacy.load('/Users/sofiahalima/PycharmProjects/EntityExtractionDemo/app/model/output/model-best')


def extract_entities(text):
    doc = nlp(text)
    return [{
        "text": ent.text,
        "label": ent.label_,
        "start": ent.start_char,
        "end": ent.end_char
    } for ent in doc.ents]
