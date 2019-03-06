pyinstaller --onefile --noconsole ^
            renpytexteditor.py
robocopy ./config ./dist/config
robocopy ./themes ./dist/themes
robocopy ./snippets ./dist/snippets
robocopy ./assets ./dist/assets
pause