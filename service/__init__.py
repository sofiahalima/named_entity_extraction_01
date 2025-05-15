import azure
import azure.functions as func

from data_collection import setup_azure_blob, scrape_bbc_news, save_to_blob

app = func.FunctionApp()


@app.schedule(schedule="0 */30 * * * *", arg_name="mytimer", run_on_startup=True)
def bbc_scrape_timer(mytimer: func.TimerRequest):
    container = setup_azure_blob()
    news_data = scrape_bbc_news()
    if news_data:
        save_to_blob(container, news_data)
