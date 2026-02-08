import storage.movie_storage_sql as storage
import storage.movie_api as api
from storage.website_generator import generate_website


def handle_list_movies():
    """Zeigt alle Filme aus der Datenbank an."""
    movies = storage.get_movies()
    if not movies:
        print("Keine Filme in der Datenbank.")
        return
    for title, data in movies.items():
        print(f"{title} ({data['year']}), Rating: {data['rating']}")


def handle_add_movie():
    """Sucht Film via API und speichert ihn in der DB."""
    title = input("Gib den Filmnamen ein: ").title()
    movie_data = api.fetch_movie_from_api(title)
    if movie_data:
        storage.add_movie_to_db(movie_data)
        print(f"Erfolg: {movie_data['title']} hinzugefügt.")
    else:
        print("Film nicht gefunden.")


def handle_delete_movie():
    """Löscht einen Film nach Benutzereingabe."""
    title = input("Film zum Löschen eingeben: ").title()
    storage.delete_movie(title)
    print("Falls vorhanden, wurde der Film gelöscht.")


def handle_update_movie():
    """Aktualisiert das Rating eines Films."""
    title = input("Filmtitel: ").title()
    try:
        rating = float(input("Neues Rating (0-10): "))
        storage.update_movie(title, rating)
        print("Rating aktualisiert.")
    except ValueError:
        print("Ungültige Eingabe für das Rating.")


def start_menu():
    """Hauptmenü-Schleife."""
    actions = {
        "1": handle_list_movies,
        "2": handle_add_movie,
        "3": handle_delete_movie,
        "4": handle_update_movie,
        "9": lambda: generate_website(storage.get_movies())
    }

    while True:
        print("\n--- Film Datenbank ---")
        print("0. Exit | 1. Liste | 2. Hinzufügen | 3. Löschen | 4. Update | 9. Webseite")
        choice = input("Wahl: ")

        if choice == "0":
            break
        if choice in actions:
            actions[choice]()
        else:
            print("Ungültige Wahl.")


if __name__ == "__main__":
    storage.init_db()
    start_menu()
