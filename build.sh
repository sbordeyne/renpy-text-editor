pyinstaller --onefile --noconsole ^
            renpytexteditor.py
cp ./config ./dist/config
cp ./themes ./dist/themes
cp ./snippets ./dist/snippets
cp ./assets ./dist/assets