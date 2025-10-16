

# Language dictionaries
_translations = {
    "English": {
        "custom_files": "Custom Files",
        "setting": "Settings",
        "language": "Language",
        "name": "Name:",
        "vatsim_id": "Vatsim ID:",
        "hint": "Hint",
        "vatsim_password": "Vatsim password:",
        "rating": "Rating:",
        "hoppie_code": "Hoppie code:",
        "afv_path": "Audio tool Path:",
        "browse": "Browse",
        "save": "Save",
        "missing_data_title": "Missing data",
        "missing_data": "At least name, Vatsim ID, Vatsim password, and rating must be set.",
        "update_available": "Update available",
        "installer_upgrade_available": "A newer version of the installer is available.",
        "installer_version": "A newer version of the installer is available.",
        "error_title": "Error",
        "error installercheck": "No internet connection, or online version not found.",
        "fresh_install": "Fresh install",
        "Choose_a_profile": "Choose a profile",
        "start": "Start",
        "sectorfile_version": (
"""ATTENTION!

Due to navdata provider changes, you have to manually download the sectorfile! 

When you press OK, your web browser will open the AeroNav GNG page. Please log in with your Navigraph and VATSIM accounts, download the sectorfile package and extract its contents in the folder that will open as well."""),
        "download": "Download",
        "language_changed_after_reload": "Language is changed after a restart",
        "quit": "Quit Installer",
        "euroscope_not_found": "Euroscope not found!",
        "could_not_find_euroscope": "Euroscope could not be found. You can check the path here:",
        "download_euroscope": "Download Euroscope",
        "euroscope_path": "Euroscope Path:",
        "ok": "Okay!",
        "file_is_not_euroscope": "File is not Euroscope. Please select the Euroscope.exe file.",
        "euroscope_upgrade_available": "A Euroscope upgrade is available.",
        "sectorfile": "Sectorfile",
        "name_not_set": "Your name is not configured!",
        "vatsim_id_not_set": "Your VATSIM ID is not configured!",
        "rating_not_set": "Your rating is not set!",
        "error": "Error!",
        "import_sectorfile": "Import sectorfile",
        "press_ok_to_continue_import_or_cancel_to_abort": "When you are done extracting the Sectorfile, click on okay to continue the import.",
        "could_not_find_valid_sectorfile_in_directory": "No valid sectorfile in import folder!",
        "please_select_a_profile": "Please select a profile.",
        "no_profiles_found": "No profiles found. Did you import a sectorfile?",
        "choose_a_profile": "Select Profile",
        "error": "Error!",
        "sectorfile_update_available": "A sectorfile update is available!",
        "about": "About",
        "about_message": """Sectorfile Installer

Built by the team at VACC-Austria.

For further information visit:""",
    },    
    "Deutsch": {
        "custom_files": "Benutzerdefinierte Dateien ",
        "setting": "Einstellungen",
        "language": "Sprache",
        "name": "Name:",
        "vatsim_id": "Vatsim ID:",
        "hint": "Hinweis",
        "vatsim_password": "Vatsim Passwort:",
        "rating": "Bewertung:",
        "hoppie_code": "Hoppie-Code:",
        "afv_path": "Audio Tool Pfad:",
        "browse": "Durchsuchen",
        "save": "Speichern",
        "missing_data_title": "Fehlende Daten",
        "missing_data": "Mindestens Name, Vatsim ID, Vatsim Passwort und Bewertung müssen festgelegt werden.",
        "update_available": "Update verfügbar",
        "installer_upgrade_available": "Eine neuere Version des Installers ist verfügbar.",
        "error_title": "Fehler",
        "error installercheck": "Keine Internetverbindung oder Online-Version nicht gefunden.",
        "fresh_install": "Neuinstallation",
        "Choose_a_profile": "Profil auswählen",
        "start": "Starten",
        "sectorfile_version": (
"""ACHTUNG!

Aufgrund von Änderungen beim Navdata-Anbieter musst du die Sektor-Datei manuell herunterladen. 

Wenn du auf OK klickst, öffnet dein Webbrowser die AeroNav GNG-Seite. Bitte melde dich mit deinem Navigraph- und deinem VATSIM-Konto an, lade das Sektorpaket herunter und entpacke es in den ebenfalls geöffneten Ordner."""),
        "download": "Herunterladen",
        "language_changed_after_reload": "Sprache wird nach Neustart geändert",
        "quit": "Installer beenden",
        "euroscope_not_found": "Euroscope nicht gefunden!",
        "could_not_find_euroscope": "Euroscope wurde nicht gefunden. Bitte überprüfe den Pfad:",
        "download_euroscope": "Euroscope Herunterladen",
        "euroscope_path": "Euroscope Pfad:",
        "ok": "OK!",
        "file_is_not_euroscope": "Diese Datei ist nicht Euroscope. Bitte wähle eine Euroscope.exe Datei aus.",
        "euroscope_upgrade_available": "Ein Update für Euroscope ist verfügbar.",
        "sectorfile": "Sectorfile",
        "name_not_set": "Dein Name ist nicht konfiguriert!",
        "vatsim_id_not_set": "Deine VATSIM ID ist nicht konfiguriert!",
        "rating_not_set": "Dein Rating ist nicht konfiguriert!",
        "error": "Fehler!",
        "import_sectorfile": "Sectorfile importieren",
        "press_ok_to_continue_import_or_cancel_to_abort": "Klicke auf OK um den Import fortzusetzen.",
        "could_not_find_valid_sectorfile_in_directory": "Kein gültiges Sectorfile in Import Ordner!",
        "please_select_a_profile": "Bitte wähle ein Profile aus.",
        "no_profiles_found": "Keine Profile gefunden. Hast du ein Sectorfile importiert?",
        "choose_a_profile": "Profil auswählen",
        "error": "Fehler!",
        "sectorfile_update_available": "Ein Sectorfile Update ist verfügbar!",
        "about": "Über ...",
        "about_message": """Sectorfile Installer

Erstellt vom Team der VACC-Austria.

Weitere Informationen auf:"""
     }
}

_selected_language: str | None = None

def select_language(lang: str):
    global _selected_language, _translations

    if lang not in _translations:
        _selected_language = "English"
    _selected_language = lang

def get_languages() -> list[str]:
    global _translations
    return list(sorted(_translations.keys()))

def translate(key: str) -> str:
    global _selected_language, _translations
    if _selected_language is None:
        raise ValueError("no language selected yet")
    return _translations[_selected_language].get(key, key)