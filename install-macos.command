#!/bin/bash
# Install Garmin Map Combiner into ~/Applications as a double-clickable .app
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)"
APP="$HOME/Applications/Garmin Map Combiner.app"
MACOS="$APP/Contents/MacOS"
RES="$APP/Contents/Resources"

mkdir -p "$MACOS" "$RES" "$HOME/Applications"
cp "$SRC/garmin_map_combiner.py" "$RES/garmin_map_combiner.py"

cat > "$MACOS/Garmin Map Combiner" << 'LAUNCH'
#!/bin/bash
DIR="$(cd "$(dirname "$0")/../Resources" && pwd)"
export PATH="/opt/homebrew/opt/openjdk/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

PY=""
for c in \
  /opt/homebrew/Cellar/python@3.13/*/bin/python3.13 \
  /opt/homebrew/opt/python@3.13/bin/python3.13 \
  /opt/homebrew/bin/python3.13 \
  /opt/homebrew/bin/python3 \
  /usr/bin/python3
do
  if [ -x "$c" ]; then PY="$c"; break; fi
done

if [ -z "$PY" ]; then
  osascript -e 'display dialog "Python 3 was not found.\n\nInstall with:\nbrew install python@3.13 python-tk@3.13" buttons {"OK"} default button 1'
  exit 1
fi

exec "$PY" "$DIR/garmin_map_combiner.py"
LAUNCH
chmod +x "$MACOS/Garmin Map Combiner"

cat > "$APP/Contents/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>Garmin Map Combiner</string>
  <key>CFBundleDisplayName</key><string>Garmin Map Combiner</string>
  <key>CFBundleIdentifier</key><string>dev.wilsonsamiano.garmin-map-combiner</string>
  <key>CFBundleVersion</key><string>1.0.0</string>
  <key>CFBundleShortVersionString</key><string>1.0.0</string>
  <key>CFBundleExecutable</key><string>Garmin Map Combiner</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>LSMinimumSystemVersion</key><string>13.0</string>
  <key>NSHighResolutionCapable</key><true/>
</dict>
</plist>
PLIST

xattr -dr com.apple.quarantine "$APP" 2>/dev/null || true

osascript -e 'display dialog "Garmin Map Combiner was installed in Applications.\n\nYou still need Java and mkgmap.jar (see the README on GitHub).\n\nOpen it now?" buttons {"Later", "Open"} default button "Open"' >/tmp/gmc-install.txt 2>/dev/null || true
if grep -q Open /tmp/gmc-install.txt 2>/dev/null; then
  open "$APP"
fi

echo "Installed: $APP"
