pyinstaller --onefile --noconsole ^
            renpytexteditor.py
robocopy ./config ./dist/config
robocopy ./themes ./dist/themes
robocopy ./snippets ./dist/snippets
robocopy ./assets ./dist/assets
robocopy ./locale ./dist/locale
robocopy ./docs ./dist/docs
pause