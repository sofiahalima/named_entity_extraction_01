import time
from app.service.ner import extract_entities
import os

sample_text = ("Jeff Bezos and Elon Musk are founders of Amazon and SpaceX. They met in Washington, D.C. to discuss AI "
               "policy with the United Nations.")


def benchmark_model(use_bert):
    os.environ["USE_BERT_NER"] = str(use_bert).lower()
    start = time.time()
    ents = extract_entities(sample_text)
    duration = time.time() - start
    return len(ents), duration


def test_benchmark_models():
    bert_ents, bert_time = benchmark_model(True)
    spacy_ents, spacy_time = benchmark_model(False)

    print(f"BERT: {bert_ents} entities in {bert_time:.3f}s")
    print(f"spaCy: {spacy_ents} entities in {spacy_time:.3f}s")
