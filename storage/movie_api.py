import os
import requests
from dotenv import load_dotenv

# Lädt die Variablen aus der .env Datei
load_dotenv()
API_KEY = os.getenv("MOVIE_API_KEY")


def fetch_movie_from_api(title):
    """
    Ruft Filmdaten von der OMDb-API ab.

    :param title: Der Titel des Films.
    :return: Dictionary mit (title, year, rating, poster) oder None bei Fehlern.
    """
    if not API_KEY:
        print("Fehler: API_KEY nicht in der .env Datei gefunden.")
        return None

    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Prüft auf HTTP-Fehler
        data = response.json()

        if data.get("Response") == "True":
            return {
                "title": data.get("Title"),
                "year": int(data.get("Year")[:4]) if data.get("Year") else 0,
                "rating": float(data.get("imdbRating")) if data.get("imdbRating") != "N/A" else 0.0,
                "poster": data.get("Poster")
            }
        return None
    except Exception as e:
        print(f"API-Fehler: {e}")
        return None
