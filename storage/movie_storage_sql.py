import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Pfad-Logik nach Shovals Kritik
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")
db_path = os.path.join(data_dir, "movies.db")
DB_URL = f"sqlite:///{db_path}"

# Engine erstellen
engine = create_engine(DB_URL)


def init_db():
    """
    Initialisiert die Datenbank.
    FIX: Erstellt den 'data'-Ordner, falls er fehlt (behebt Shovals OperationalError).
    """
    try:
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

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
    except SQLAlchemyError as e:
        print(f"Datenbankfehler bei der Initialisierung: {e}")


def get_movies():
    """Ruft alle Filme ab und gibt sie als Dictionary zurück."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT title, year, rating, poster_url FROM movies"))
            rows = result.fetchall()
        return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in rows}
    except SQLAlchemyError as e:
        print(f"Fehler beim Abrufen: {e}")
        return {}


def add_movie_to_db(movie_data):
    """Speichert Filmdaten."""
    if not movie_data:
        return
    try:
        with engine.connect() as connection:
            connection.execute(text("""
                INSERT INTO movies (title, year, rating, poster_url) 
                VALUES (:t, :y, :r, :p)"""),
                               {"t": movie_data["title"], "y": movie_data["year"], "r": movie_data["rating"],
                                "p": movie_data["poster"]}
                               )
            connection.commit()
    except SQLAlchemyError as e:
        print(f"Fehler beim Hinzufügen: {e}")


def update_movie(title, rating):
    """Aktualisiert das Rating."""
    try:
        with engine.connect() as connection:
            connection.execute(text("UPDATE movies SET rating = :r WHERE title = :t"), {"r": rating, "t": title})
            connection.commit()
    except SQLAlchemyError as e:
        print(f"Fehler beim Update: {e}")


def delete_movie(title):
    """Löscht einen Film."""
    try:
        with engine.connect() as connection:
            connection.execute(text("DELETE FROM movies WHERE title = :t"), {"t": title})
            connection.commit()
    except SQLAlchemyError as e:
        print(f"Fehler beim Löschen: {e}")


def get_stats():
    """
    Berechnet Statistiken (Gefordert von Shoval).
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT AVG(rating), MAX(rating), MIN(rating) FROM movies")).fetchone()
            if not result or result[0] is None:
                return None

            # Besten Film für den Namen finden
            best = connection.execute(text("SELECT title FROM movies WHERE rating = :r"), {"r": result[1]}).fetchone()
            worst = connection.execute(text("SELECT title FROM movies WHERE rating = :r"), {"r": result[2]}).fetchone()

            return {
                "average": result[0],
                "best_movie": best[0] if best else "N/A",
                "best_rating": result[1],
                "worst_movie": worst[0] if worst else "N/A",
                "worst_rating": result[2]
            }
    except SQLAlchemyError as e:
        print(f"Fehler bei Stats: {e}")
        return None


def search_movies(query):
    """Sucht Filme (Gefordert von Shoval)."""
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT title, year, rating, poster_url FROM movies WHERE title LIKE :q"),
                {"q": f"%{query}%"}
            ).fetchall()
            return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in result}
    except SQLAlchemyError as e:
        print(f"Fehler bei Suche: {e}")
        return {}
