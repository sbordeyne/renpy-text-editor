pyinstaller --onefile --noconsole ^
            renpytexteditor.py
robocopy ./config ./dist/config
robocopy ./themes ./dist/themes
pause