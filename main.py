import random as rand
from storage.movie_storage_sql import *
# ODER (besser für deine Struktur):
import storage.movie_storage_sql as storage


def main():
    """Initialisiert die DB und startet das Programm."""
    storage.init_db()
    start_here()


def start_here():
    """Hauptmenü mit allen 10 Optionen (0-9)."""
    while True:
        print("\n" + "*" * 10, " My Movies Database ", "*" * 10, end="\n\n")
        print("Menu:")
        print("0. Exit | 1. List | 2. Add | 3. Delete | 4. Update")
        print("5. Stats | 6. Random | 7. Search | 8. Sorted | 9. Generate Website")

        answer = input("\nEnter choice (0-9): ")
        print()

        if answer == "0":
            print("Goodbye!")
            break
        elif answer == "1":
            list_movies()
        elif answer == "2":
            add_movie()
        elif answer == "3":
            delete_movie()
        elif answer == "4":
            update_movie()
        elif answer == "5":
            stats()
        elif answer == "6":
            random_movie()
        elif answer == "7":
            search_movie()
        elif answer == "8":
            movies_sorted_by_rating()
        elif answer == "9":
            generate_website()
        else:
            print("Invalid choice")

        input("\nPress enter to continue")


def list_movies():
    movies = storage.get_movies()
    for title, data in movies.items():
        print(f"{title} ({data['year']}), rating: {data['rating']}")


def add_movie():
    name = input("Enter movie name: ").title()
    storage.add_movie(name)


def delete_movie():
    name = input("Enter movie to delete: ").title()
    storage.delete_movie(name)


def update_movie():
    name = input("Enter movie name: ").title()
    try:
        new_rating = float(input("Enter new rating: "))
        storage.update_movie(name, new_rating)
        print("Updated!")
    except:
        print("Invalid input.")


def stats():
    movies = storage.get_movies()
    if not movies: return
    ratings = [m["rating"] for m in movies.values()]
    print(f"Average: {sum(ratings) / len(ratings):.2f} | Best: {max(ratings)}")


def random_movie():
    movies = storage.get_movies()
    if movies:
        t = rand.choice(list(movies.keys()))
        print(f"Random Pick: {t} ({movies[t]['year']})")


def search_movie():
    query = input("Search: ").title()
    for t, d in storage.get_movies().items():
        if query in t: print(f"Found: {t}")


def movies_sorted_by_rating():
    movies = storage.get_movies()
    sorted_list = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    for t, d in sorted_list:
        print(f"{d['rating']} - {t}")


def generate_website():
    """Erzeugt die index.html aus dem Template."""
    movies = storage.get_movies()
    try:
        # Template aus _static lesen
        with open("_static/index_template.html", "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print("Error: Template not found in _static/")
        return

    # HTML für die Film-Liste bauen
    movie_grid = ""
    for title, data in movies.items():
        movie_grid += "<li>"
        movie_grid += '<div class="movie">'
        # WICHTIG: Stelle sicher, dass 'poster' in movie_storage_sql.py korrekt zurückgegeben wird
        movie_grid += f'<img class="movie-poster" src="{data["poster"]}" alt="Poster">'
        movie_grid += f'<div class="movie-title">{title}</div>'
        movie_grid += f'<div class="movie-year">{data["year"]}</div>'
        movie_grid += "</div>"
        movie_grid += "</li>\n"

    # Platzhalter ersetzen
    content = template.replace("__TEMPLATE_TITLE__", "My Movie App")
    content = content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    # index.html im Hauptordner speichern
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("Website was generated successfully.")


if __name__ == "__main__":
    main()
