import json
from typing import List

import cloudscraper
import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
import azure
from azure.eventhub import EventHubProducerClient, EventData
from azure.storage.blob import BlobServiceClient

from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path="/Users/sofiahalima/PycharmProjects/EntityExtractionDemo/app/.env")



def fetch_news_from_api():
    sources = {
        "newsapi": "https://bbc-world-news-api.p.rapidapi.com/sport/cricket"
    }

    producer = EventHubProducerClient.from_connection_string(
        os.getenv("EVENT_HUB_CONN_STR"),
        eventhub_name="sports_news"
    )
    for source, url in sources.items():
        params = {"sportName": "cricket"}
        headers = {"X-RapidAPI-Host": "bbc-world-news-api.p.rapidapi.com"}
        response = requests.get(url, params=params, headers=headers)

        with producer:
            batch = producer.create_batch()
            for article in response.json()["articles"]:
                batch.add(EventData(json.dumps({
                    "id": f"{source}-{article['publishedAt']}-{hash(article['title'])}",
                    "sources": source,
                    "content": article["content"],
                    "metadata": article
                })))
            producer.send_batch(batch)


def setup_azure_blob():
    """Initialize Azure Blob Storage client"""
    blob_service_client = BlobServiceClient.from_connection_string(os.environ["AZURE_STORAGE_CONNECTION_STRING"])
    container_client = blob_service_client.get_container_client("bbc-news-json")
    try:
        container_client.create_container("bbc-news-json")
    except Exception:
        pass  # Container exists
    return container_client


def load_doc_from_storage() -> List[dict]:
    documents = []
    container_client = setup_azure_blob()

    for blob in container_client.list_blobs():
        blob_client = container_client.get_blob_client(blob.name)
        content = blob_client.download_blob().readall()
        document = json.loads(content)
        documents.append(document)
    return documents


def scrape_bbc_news():
    scraper = cloudscraper.create_scraper()
    try:
        response = scraper.get("https://www.bbc.com/news")
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []
        for article in soup.find_all("div", {"data-testid": "edinburgh-card"}):
            title = article.find("h3")
            if not title:
                continue

            articles.append({
                "title": title.text.strip(),
                "url": "https://www.bbc.com" + article.find("a")["href"],
                "summary": article.find("p").text.strip() if len(article.find("p").text.strip()) > 0 else None,
                "timestamp": datetime.utcnow().isoformat()
            })

        return articles
    except Exception as e:
        print(f"web scraping failed:{str(e)}")
        return []


def save_to_blob(container_name, data):
    blob_name = f"bbc_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    blob_client = container_name.get_blob_client(blob_name)

    try:
        blob_client.upload_blob(
            json.dumps(data, indent=2),
            overwrite=True,
            metadata={"source": "bbc.com",
                      "timestamp": datetime.utcnow().isoformat(),
                      "processed": False})
        print(f"successfully saved data to {blob_name}")
    except Exception as e:
        print(f"blob upload failed: {str(e)}")


if __name__ == "__main__":
    container = setup_azure_blob()
    new_articles = scrape_bbc_news()
    if new_articles:
        save_to_blob(container, new_articles)


def scrape_article_content(url):
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        return {
            "body": ' '.join(p.text for p in soup.select('article p')),
            "authors": [a.text for a in soup.select('[data-testid="byline-name"]')],
            "published_time": soup.find('time')['datetime'] if soup.find('time') else None
        }
    except Exception as e:
        print(f"Failed to scrape article: {str(e)}")
        return None


# Error Handling & Retries
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def scrape_with_retry(url):
    return cloudscraper.get(url)
