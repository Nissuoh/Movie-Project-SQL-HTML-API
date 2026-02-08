import os


def generate_website(movies):
    """
    Erzeugt die index.html basierend auf den Filmdaten im Speicher.
    """
    try:
        # Pfade relativ zur Datei festlegen
        base_dir = os.path.dirname(__file__)
        template_path = os.path.join(base_dir, "..", "_static", "index_template.html")
        output_path = os.path.join(base_dir, "..", "index.html")

        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        movie_grid = ""
        for title, data in movies.items():
            movie_grid += f"""
            <li>
                <div class="movie">
                    <img class="movie-poster" src="{data['poster']}" alt="Poster">
                    <div class="movie-title">{title}</div>
                    <div class="movie-year">{data['year']}</div>
                </div>
            </li>
            """

        content = template.replace("__TEMPLATE_TITLE__", "My Movie App")
        content = content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Website wurde erfolgreich erstellt.")

    except FileNotFoundError:
        print("Fehler: Template-Datei nicht gefunden.")
    except Exception as e:
        print(f"Fehler bei der Website-Generierung: {e}")
