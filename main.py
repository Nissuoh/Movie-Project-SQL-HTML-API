import storage.movie_storage_sql as storage
import api.movie_api as api
from utils.website_generator import generate_website


def display_menu():
    """Zeigt das Hauptmenü an (Erweitert um Stats & Suche nach Shovals Kritik)."""
    print("\n--- Film Datenbank ---")
    print("0. Exit")
    print("1. Liste anzeigen")
    print("2. Film hinzufügen (API)")
    print("3. Film löschen")
    print("4. Bewertung aktualisieren")
    print("5. Statistiken anzeigen")
    print("6. Film suchen")
    print("7. Filme sortieren")
    print("9. Webseite generieren")


def handle_update_movie():
    """Aktualisiert das Rating mit Validierung zwischen 0 und 10."""
    title = input("Filmtitel für das Update: ").title()
    try:
        rating = float(input("Neues Rating (0.0 - 10.0): "))
        # Shoval Kritik Punkt 2: Validierung des Bereichs
        if 0 <= rating <= 10:
            storage.update_movie(title, rating)
            print(f"Update für '{title}' auf {rating} erfolgreich.")
        else:
            print("Fehler: Das Rating muss zwischen 0 und 10 liegen!")
    except ValueError:
        print("Ungültige Eingabe: Bitte eine Zahl eingeben.")


def handle_stats():
    """Zeigt Statistiken an (Gefordert von Shoval)."""
    stats = storage.get_stats()
    if stats:
        print("\n--- Statistiken ---")
        print(f"Durchschnitt: {stats['average']:.2f}")
        print(f"Bester Film: {stats['best_movie']} ({stats['best_rating']})")
    else:
        print("Keine Daten für Statistiken verfügbar.")


def main():
    """Hauptschleife des Programms."""
    # Shoval Kritik: Sicherstellen, dass DB & Ordner existieren
    storage.init_db()

    while True:
        display_menu()
        choice = input("\nWahl: ").strip()

        if choice == "0":
            print("Programm beendet.")
            break
        elif choice == "1":
            movies = storage.get_movies()
            for title, data in movies.items():
                print(f"{title} ({data['year']}): {data['rating']}")
        elif choice == "2":
            title = input("Filmname: ").title()
            movie_data = api.fetch_movie_from_api(title)
            if movie_data:
                storage.add_movie_to_db(movie_data)
                print(f"Hinzugefügt: {movie_data['title']}")
        elif choice == "3":
            title = input("Titel zum Löschen: ").title()
            storage.delete_movie(title)
        elif choice == "4":
            handle_update_movie()
        elif choice == "5":
            handle_stats()
        elif choice == "6":
            query = input("Suchbegriff: ")
            results = storage.search_movies(query)
            for t, d in results.items():
                print(f"Gefunden: {t} ({d['year']})")
        elif choice == "7":
            # Optionales Feature: Sortierung
            sorted_movies = storage.get_sorted_movies()
            for t, d in sorted_movies:
                print(f"{t}: {d['rating']}")
        elif choice == "9":
            generate_website(storage.get_movies())
        else:
            print("Ungültige Wahl, bitte erneut versuchen.")


if __name__ == "__main__":
    main()
