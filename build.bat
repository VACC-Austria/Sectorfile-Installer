pyinstaller --onefile ^
            --windowed ^
            --add-data vacc-austria:vacc ^
            --icon vacc-austria/icon.ico ^
            Session-Launcher.py
