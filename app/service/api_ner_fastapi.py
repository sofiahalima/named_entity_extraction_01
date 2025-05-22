from fastapi import FastAPI, HTTPException
from azure.cosmos import exceptions
from db import container

app = FastAPI()


@app.get("/entities")
def get_entities(id: str):
    try:
        response = container.read_item(item=id, partition_key=id)
        return {
            "id": response["id"],
            "title": response["title"],
            "content": response["content"],
            "entities": response.get("entities", [])
        }
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")
