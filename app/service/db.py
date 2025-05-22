from datetime import datetime
from typing import List

from azure.cosmos import CosmosClient, PartitionKey
import os
from dotenv import load_dotenv
import os

load_dotenv()

client = CosmosClient(os.getenv("COSMOS_DB_URL"), credential=os.getenv("COSMOS_DB_KEY"))
database = client.create_database_if_not_exists(id="nerDB")  # Requires ID
container = database.create_container_if_not_exists(
    id="ner-doc",
    partition_key="/id"
)


def persist_data_with_entities(doc: dict, entities: List[dict]):
    enriched_doc = {
        **doc,
        "entities": entities,
        "processed_at": datetime.utcnow().isoformat()
    }
    container.upsert_item(enriched_doc)


def get_document_by_id(doc_id):
    return container.read_item(item=doc_id, partition_key=doc_id)
