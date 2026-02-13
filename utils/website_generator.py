import os


def generate_website(movies):
    """
    Erzeugt die index.html basierend auf den Filmdaten.

    Verbesserungen nach Kritik:
    - Robustere Pfadverwaltung.
    - Detaillierte Fehlerbehandlung für I/O Operationen.
    - Docstrings für bessere Wartbarkeit.
    """
    try:
        # Pfade sauber definieren
        base_dir = os.path.dirname(os.path.dirname(__file__))  # Geht eine Ebene hoch aus /utils
        template_path = os.path.join(base_dir, "_static", "index_template.html")
        output_path = os.path.join(base_dir, "index.html")

        # Prüfen, ob das Template existiert, bevor wir es öffnen
        if not os.path.exists(template_path):
            print(f"Fehler: Die Vorlage wurde unter {template_path} nicht gefunden.")
            return

        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        movie_grid = ""

        # Falls movies eine Liste von Objekten ist (SQLAlchemy) oder ein Dictionary
        # Hier angepasst auf ein Dictionary/Objekt-Mix für maximale Kompatibilität
        for title, data in movies.items():
            poster = data.get('poster', 'https://via.placeholder.com/150')
            year = data.get('year', 'N/A')

            movie_grid += f"""
            <li>
                <div class="movie">
                    <img class="movie-poster" src="{poster}" alt="Poster von {title}">
                    <div class="movie-title">{title}</div>
                    <div class="movie-year">{year}</div>
                </div>
            </li>
            """

        # Platzhalter ersetzen
        content = template.replace("__TEMPLATE_TITLE__", "My Movie App")
        content = content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

        # Datei schreiben
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Website wurde erfolgreich unter {output_path} erstellt.")

    except PermissionError:
        print("Fehler: Keine Berechtigung zum Schreiben der index.html.")
    except Exception as e:
        print(f"Unerwarteter Fehler bei der Website-Generierung: {e}")
