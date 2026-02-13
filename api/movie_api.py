import os
import requests
from dotenv import load_dotenv

# Lädt die Variablen aus der .env Datei
load_dotenv()
API_KEY = os.getenv("MOVIE_API_KEY")


def fetch_movie_from_api(title):
    """
    Ruft Filmdaten von der OMDb-API ab.

    Diese Funktion kapselt die API-Logik und verhindert Abstürze bei
    Verbindungsproblemen (Shoval Kritik Punkt 2).
    """
    if not API_KEY:
        print("Fehler: API_KEY nicht in der .env Datei gefunden.")
        return None

    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "True":
            # Extraktion der Daten
            raw_rating = data.get("imdbRating")

            # Validierung des Ratings (Shoval Kritik Punkt 2)
            # Wir stellen sicher, dass das Rating eine Zahl zwischen 0 und 10 ist
            try:
                rating = float(raw_rating) if raw_rating != "N/A" else 0.0
                if not (0 <= rating <= 10):
                    rating = 0.0
            except ValueError:
                rating = 0.0

            return {
                "title": data.get("Title"),
                "year": int(data.get("Year")[:4]) if data.get("Year") else 0,
                "rating": rating,
                "poster": data.get("Poster")
            }

        print(f"Film '{title}' wurde in der API nicht gefunden.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Netzwerkfehler bei der API-Anfrage: {e}")
        return None
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return None
