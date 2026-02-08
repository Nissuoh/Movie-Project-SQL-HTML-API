import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# 1. Absoluter Pfad: Stellt sicher, dass movies.db im 'data'-Ordner gefunden wird
# Egal von wo das Programm gestartet wird.
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, "..", "data", "movies.db")
DB_URL = f"sqlite:///{db_path}"

# Engine erstellen
engine = create_engine(DB_URL)


def init_db():
    """
    Initialisiert die Datenbank und erstellt die Tabelle 'movies',
    falls diese noch nicht existiert.
    """
    try:
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
    """
    Ruft alle Filme aus der Datenbank ab.

    :return: Ein Dictionary, bei dem der Titel der Key ist und
             Details (year, rating, poster) die Werte sind.
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT title, year, rating, poster_url FROM movies"))
            rows = result.fetchall()
        # Umwandlung in das vom Frontend erwartete Dictionary-Format
        return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in rows}
    except SQLAlchemyError as e:
        print(f"Fehler beim Abrufen der Filme: {e}")
        return {}


def add_movie_to_db(movie_data):
    """
    Speichert ein Dictionary mit Filmdaten in der Datenbank.

    :param movie_data: Dictionary mit 'title', 'year', 'rating' und 'poster'.
    """
    if not movie_data:
        return

    try:
        with engine.connect() as connection:
            connection.execute(text("""
                INSERT INTO movies (title, year, rating, poster_url) 
                VALUES (:t, :y, :r, :p)"""),
                               {
                                   "t": movie_data["title"],
                                   "y": movie_data["year"],
                                   "r": movie_data["rating"],
                                   "p": movie_data["poster"]
                               })
            connection.commit()
    except SQLAlchemyError as e:
        # Fängt z.B. UniqueConstraint-Fehler ab, wenn der Film schon existiert
        print(f"Fehler beim Hinzufügen des Films '{movie_data.get('title')}': {e}")


def delete_movie(title):
    """
    Entfernt einen Film basierend auf seinem Titel aus der Datenbank.

    :param title: Der exakte Titel des zu löschenden Films.
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("DELETE FROM movies WHERE title = :t"), {"t": title})
            connection.commit()
            if result.rowcount > 0:
                print(f"Film '{title}' wurde gelöscht.")
            else:
                print(f"Film '{title}' wurde in der Datenbank nicht gefunden.")
    except SQLAlchemyError as e:
        print(f"Fehler beim Löschen des Films: {e}")


def update_movie(title, rating):
    """
    Aktualisiert das Rating eines Films in der Datenbank.

    :param title: Der Titel des Films.
    :param rating: Die neue Bewertung (float).
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("UPDATE movies SET rating = :r WHERE title = :t"),
                                        {"r": rating, "t": title})
            connection.commit()
            if result.rowcount > 0:
                print(f"Rating für '{title}' auf {rating} aktualisiert.")
            else:
                print(f"Film '{title}' konnte nicht aktualisiert werden (nicht gefunden).")
    except SQLAlchemyError as e:
        print(f"Fehler beim Update des Films: {e}")
