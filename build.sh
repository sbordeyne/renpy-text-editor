pyinstaller --onefile --noconsole ^
            renpytexteditor.py
cp ./config ./dist/config
cp ./themes ./dist/themes
pause