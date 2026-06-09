#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required. Install Python 3 and try again."
  exit 1
fi

if ! command -v osacompile >/dev/null 2>&1; then
  echo "osacompile is required to build the .app bundle."
  exit 1
fi

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt pyinstaller

rm -rf build dist
python3 -m PyInstaller --clean --onefile --console --name pokemon --add-data "sounds:sounds" pokemon.py

APP_NAME="PokemonBattleSim"
APP_DIR="dist/${APP_NAME}.app"
TMP_SCRIPT="$(mktemp /tmp/pokemon_app.XXXXXX.applescript)"

cat > "$TMP_SCRIPT" <<'EOF'
on run
  set appPath to POSIX path of (path to me)
  set appDir to POSIX path of (container of (path to me))
  set resourcesDir to appDir & "Contents/Resources"
  tell application "Terminal"
    activate
    do script "cd " & quoted form of resourcesDir & " && ./pokemon"
  end tell
end run
EOF

osacompile -o "$APP_DIR" "$TMP_SCRIPT"
rm -f "$TMP_SCRIPT"

cp dist/pokemon "$APP_DIR/Contents/Resources/pokemon"
chmod +x "$APP_DIR/Contents/Resources/pokemon"

rm -rf dist/dmg
mkdir -p dist/dmg
cp -R "$APP_DIR" dist/dmg/
cp README.md dist/dmg/

hdiutil create -srcfolder dist/dmg -volname "Pokemon Battle Sim" -fs HFS+ -format UDZO dist/${APP_NAME}.dmg

echo "Created dist/${APP_NAME}.app and dist/${APP_NAME}.dmg"
