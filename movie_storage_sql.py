import requests
from sqlalchemy import create_engine, text

API_KEY = "8eea84d2"
DB_URL = "sqlite:///movies.db"
engine = create_engine(DB_URL)

def init_db():
    """Erstellt die Tabelle mit Poster-URL Spalte."""
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER,
                rating REAL,
                poster_url TEXT
            )
        """))
        connection.commit()

def get_movies():
    """Gibt alle Filme für das Menü und die Website zurück."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster_url FROM movies"))
        rows = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in rows}

def add_movie(title):
    """Holt Filmdaten inklusive Poster von OMDb."""
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get("Response") == "True":
            m_title = data.get("Title")
            m_year = int(data.get("Year")[:4]) if data.get("Year") else 0
            m_rating = float(data.get("imdbRating")) if data.get("imdbRating") != "N/A" else 0.0
            m_poster = data.get("Poster")
            with engine.connect() as connection:
                connection.execute(text("""
                    INSERT INTO movies (title, year, rating, poster_url) 
                    VALUES (:t, :y, :r, :p)"""),
                    {"t": m_title, "y": m_year, "r": m_rating, "p": m_poster})
                connection.commit()
                print(f"Movie '{m_title}' added!")
        else:
            print("Movie not found!")
    except Exception as e:
        print(f"Error: {e}")

def delete_movie(title):
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM movies WHERE title = :t"), {"t": title})
        connection.commit()

def update_movie(title, rating):
    with engine.connect() as connection:
        connection.execute(text("UPDATE movies SET rating = :r WHERE title = :t"), {"r": rating, "t": title})
        connection.commit()