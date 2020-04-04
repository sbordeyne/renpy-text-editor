pyinstaller --onefile --noconsole renpytexteditor.py
cp -rf ./config ./dist/config
cp -rf ./themes ./dist/themes
cp -rf ./snippets ./dist/snippets
cp -rf ./assets ./dist/assets
cp -rf ./locale ./dist/locale
cp -rf ./docs ./dist/docs
