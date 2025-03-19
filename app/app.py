from flask import Flask, jsonify, render_template
import json
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

scheduler = BackgroundScheduler()

def update_local_news():
    news = fetch_news()
    with open("data/news.json", "w", encoding="utf-8") as file:
        json.dump(news, file, ensure_ascii=False, indent=4)

def update_local_events():
    events = fetch_events()
    with open("data/events.json", "w", encoding="utf-8") as file:
        json.dump(events, file, ensure_ascii=False, indent=4)

scheduler.add_job(update_local_news, 'interval', minutes=30)
scheduler.add_job(update_local_events, 'interval', minutes=30)
scheduler.start()

def load_data(filename):
    filepath = os.path.join("data", filename)
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        return {"error": str(e)}

def fetch_news():
    url = f"https://gnews.io/api/v4/top-headlines?country=fr&token=b73d8af7701ab556d3067e7e3986d31c"
    try:
        response = requests.get(url)
        data = response.json()
        if "articles" in data:
            return [{"title": article["title"], "date": article["publishedAt"]} for article in data["articles"]]
        return {"error": "Aucune actualité"}
    except Exception as e:
        return {"error": str(e)}


def fetch_events():
    url = f"https://api.openagenda.com/v2/agendas/19009844/events?key=5d8f57d220ad4fe6bfbb367f534a4dba&lang=fr"
    try:
        response = requests.get(url)
        data = response.json()
        if "events" not in data or not isinstance(data["events"], list):
            return {"error": "Aucun événement trouvé ou format incorrect"}
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

        return events_list if events_list else {"error": "Aucun événement disponible"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur lors de la connexion à l'API: {str(e)}"}
    except json.decoder.JSONDecodeError:
        return {"error": "Réponse non JSON de l'API"}
    except Exception as e:
        return {"error": f"Erreur inattendue: {str(e)}"}

@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(fetch_events())

@app.route('/api/news', methods=['GET'])
def get_news():
    return jsonify(fetch_news())

@app.route('/')
def home():
    events = fetch_events()
    news = fetch_news()
    return render_template("index.html", events=events, news=news)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4123)
