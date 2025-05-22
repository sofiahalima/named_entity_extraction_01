from datetime import datetime

from app.service.data_collection_utility import load_doc_from_storage
from app.service.db import persist_data_with_entities
from app.service.ner import extract_entities

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path="/Users/sofiahalima/PycharmProjects/EntityExtractionDemo/app/.env")


def run_pipeline():
    docs_array = load_doc_from_storage()
    for docs in docs_array:
        for doc in docs:  # assuming 'documents' is a list of dicts
            entities = extract_entities(doc["content"])
            print(entities)
            persist_data_with_entities(doc,entities)


if __name__ == "__main__":
    load_dotenv(dotenv_path="/Users/sofiahalima/PycharmProjects/EntityExtractionDemo/app/.env")
    run_pipeline()
