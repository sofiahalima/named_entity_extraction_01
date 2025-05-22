from fastapi import FastAPI, HTTPException
from app.service.db import container
from azure.cosmos import exceptions

from app.service.db import get_document_by_id

# schedule_app = func.FunctionApp()

app = FastAPI()


# @schedule_app.schedule(schedule="0 */30 * * * *", arg_name="mytimer", run_on_startup=True)
# def bbc_scrape_timer(mytimer: func.TimerRequest):
#     container = setup_azure_blob()
#     news_data = scrape_bbc_news()
#     if news_data:
#         save_to_blob(container, news_data)


@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}


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
