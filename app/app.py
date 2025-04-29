from flask import Flask, jsonify, render_template
import json
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import logging, os


logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
load_dotenv()
app = Flask(__name__)
scheduler = BackgroundScheduler()

def upload_to_blob(filename, data):
    try:
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = os.getenv("BLOB_CONTAINER", "json-data")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

        json_data = json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8")
        blob_client.upload_blob(json_data, overwrite=True)
        logging.info(f"{filename} uploaded to Azure Blob.")
    except Exception as e:
        logging.info(f"[ERROR upload_to_blob] {filename}: {str(e)}")

def load_data_from_blob(filename):
    blob_base_url = os.getenv("BLOB_STORAGE_URL", "")
    try:
        response = requests.get(f"{blob_base_url}/{filename}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return [{"title": f"Erreur lors du chargement de {filename} depuis Azure Blob", "date": str(e)}]

def fetch_news():
    url = "https://gnews.io/api/v4/top-headlines?country=fr&token=b73d8af7701ab556d3067e7e3986d31c"
    try:
        response = requests.get(url)
        data = response.json()
        if "articles" in data:
            return [{"title": article["title"], "date": article["publishedAt"]} for article in data["articles"]]
        return [{"title": "Aucune actualité", "date": ""}]
    except Exception as e:
        return [{"title": "Erreur de récupération des actualités", "date": str(e)}]

def fetch_events():
    url = "https://api.openagenda.com/v2/agendas/19009844/events?key=5d8f57d220ad4fe6bfbb367f534a4dba&lang=fr"
    try:
        response = requests.get(url)
        data = response.json()
        if "events" not in data or not isinstance(data["events"], list):
            return [{"title": "Aucun événement trouvé", "date": "", "location": "", "image": "", "link": ""}]
        events_list = []
        for event in data["events"]:
            title = event.get("title", {}).get("fr", "Titre non disponible")
            next_timing = event.get("nextTiming") or {}
            date = next_timing.get("begin", "Date inconnue")
            location = event.get("location") or {}
            location_name = location.get("name", "Lieu inconnu")
            location_city = location.get("city", "Ville inconnue")
            full_location = f"{location_name}, {location_city}"
            image_data = event.get("image") or {}
            image_url = f"{image_data.get('base', '')}{image_data.get('filename', '')}" if image_data else None
            link = f"https://openagenda.com/fr/angers-nantes-opera/events/{event.get('slug', '')}"
            events_list.append({
                "title": title,
                "date": date,
                "location": full_location,
                "image": image_url,
                "link": link
            })
        return events_list if events_list else [{"title": "Aucun événement disponible", "date": "", "location": "", "image": "", "link": ""}]
    except Exception as e:
        return [{"title": "Erreur de récupération des événements", "date": "", "location": "", "image": "", "link": str(e)}]

def update_news_blob():
    news = fetch_news()
    upload_to_blob("news.json", news)

def update_events_blob():
    events = fetch_events()
    upload_to_blob("events.json", events)

scheduler.add_job(update_news_blob, 'interval', minutes=90)
scheduler.add_job(update_events_blob, 'interval', minutes=90)
scheduler.start()

@app.route("/api/news")
def api_news():
    return jsonify(load_data_from_blob("news.json"))

@app.route("/api/events")
def api_events():
    return jsonify(load_data_from_blob("events.json"))

@app.route("/")
def home():
    events = fetch_events() #load_data_from_blob("events.json") problème de crédits Azure 
    news = fetch_news() #load_data_from_blob("news.json") problème de crédits Azure 
    return render_template("index.html", events=events, news=news)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4123)

application = app 