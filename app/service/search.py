from fastapi import APIRouter, Query
from azure.cosmos import CosmosClient
import os

router = APIRouter()

client = CosmosClient(os.getenv("COSMOS_DB_URL"), credential=os.getenv("COSMOS_DB_KEY"))
db = client.get_database_client("ner_pipeline")
container = db.get_container_client("documents")

@router.get("/search")
def search_entities(
    label: str = Query(None, description="Entity label to search for"),
    start_date: str = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(None, description="End date in YYYY-MM-DD format"),
    keyword: str = Query(None, description="Keyword to search in title or content")
):
    where_clauses = []
    if label:
        where_clauses.append("EXISTS (SELECT VALUE e FROM e IN c.entities WHERE e.label = @label)")
    if start_date and end_date:
        where_clauses.append("c.date BETWEEN @start AND @end")
    elif start_date:
        where_clauses.append("c.date >= @start")
    elif end_date:
        where_clauses.append("c.date <= @end")
    if keyword:
        where_clauses.append("(CONTAINS(c.title, @keyword) OR CONTAINS(c.content, @keyword))")

    where_clause = " AND ".join(where_clauses)
    query = f"SELECT c.id, c.title, c.date, c.url, ARRAY_LENGTH(c.entities) AS entity_count FROM c"
    if where_clause:
        query += f" WHERE {where_clause}"

    params = []
    if label:
        params.append({"name": "@label", "value": label})
    if start_date:
        params.append({"name": "@start", "value": start_date})
    if end_date:
        params.append({"name": "@end", "value": end_date})
    if keyword:
        params.append({"name": "@keyword", "value": keyword})

    items = list(container.query_items(
        query=query,
        parameters=params,
        enable_cross_partition_query=True
    ))

    return {"results": items}
