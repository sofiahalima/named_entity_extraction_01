import pytest
from app.service.ner import extract_entities
import os

TEST_TEXT = "Elon Musk met with the World Health Organization in Geneva."


def test_extract_entities(use_bert):
    os.environ["USE_BERT_NER"] = str(use_bert).lower()
    entities = extract_entities(TEST_TEXT)

    assert isinstance(entities, list)
    assert any(ent["label"] in ["ORG", "GPE", "PER", "person"] for ent in entities)
    print(f"Model: {'BERT' if use_bert else 'spaCy'} — Entities: {entities}")
