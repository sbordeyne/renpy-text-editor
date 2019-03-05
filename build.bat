pyinstaller --onefile --noconsole ^
            renpytexteditor.py
robocopy ./config ./dist/config
robocopy ./themes ./dist/themes
robocopy ./snippets ./dist/snippets
robocopy ./assets/favicon.ico ./dist/assets/favicon.ico
robocopy ./assets/favicon.xbm ./dist/assets/favicon.xbm
pause