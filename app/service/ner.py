import spacy
import os
import env
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

USE_BERT_NER = os.getenv("USE_BERT_NER", "true").lower() == "true"
project_root = os.environ.get("PROJECT_ROOT")

if USE_BERT_NER:
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")


    def extract_entities(text):
        result = nlp(text)
        return [{
            "text": r["word"],
            "label": r["entity_group"],
            "start": r["start"],
            "end": r["end"],
            "score": r["score"]
        } for r in result]
else:
    model_dir = f"{project_root}/app/model/output/model-best'"
    nlp = spacy.load(model_dir)


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
