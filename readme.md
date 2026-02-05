# 🎬 Movie Project: SQL + HTML + API

Dieses Projekt ist eine interaktive Filmdatenbank-Anwendung. Es kombiniert eine Terminal-Steuerung (CLI) mit einer automatisierten Datenerfassung über eine API, einer dauerhaften Speicherung in SQL und einer grafischen Ausgabe als Webseite.

## 🚀 Features

- **API-Anbindung:** Filme werden über die OMDb API gesucht. Das Programm lädt automatisch Titel, Erscheinungsjahr, IMDB-Rating und das Filmposter.
- **SQL-Datenbank:** Alle Daten werden mit SQLAlchemy in einer SQLite-Datenbank (`movies.db`) gespeichert.
- **Web-Generator:** Auf Knopfdruck wird eine `index.html` erstellt, die alle Filme in einem schicken Grid-Layout mit Postern anzeigt.
- **Benutzerfreundliches Menü:** Suchen, Sortieren, Löschen und Statistiken direkt im Terminal.

## 🛠️ Technologien

- **Python 3**
- **SQLAlchemy:** Für die Verwaltung der SQL-Datenbank.
- **Requests:** Für die Kommunikation mit der OMDb API.
- **HTML/CSS:** Für die Darstellung der generierten Website.

## 📋 Installation & Nutzung

1. **Repository klonen:**
   Lade die Dateien auf deinen PC herunter.

2. **Bibliotheken installieren:**
   Stelle sicher, dass du die benötigten Module installiert hast:
   ```bash
   pip install sqlalchemy requests