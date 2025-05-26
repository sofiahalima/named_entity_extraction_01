import spacy
import os
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

USE_BERT_NER = os.getenv("USE_BERT_NER", "true").lower() == "true"

if USE_BERT_NER:
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")


    def extract_entities(text):
        doc = nlp(text)
        return [{
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char
        } for ent in doc.ents]
else:

    nlp = spacy.load('/Users/sofiahalima/PycharmProjects/EntityExtractionDemo/app/model/output/model-best')


    def extract_entities(text):
        doc = nlp(text)
        return [
            {
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            } for ent in doc.ents
        ]
