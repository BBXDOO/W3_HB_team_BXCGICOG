#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
npm run build
rm -rf android-app/app/src/main/assets/www
mkdir -p android-app/app/src/main/assets/www
cp -R dist/. android-app/app/src/main/assets/www/
cp android-app/compact.css android-app/app/src/main/assets/www/compact.css
python3 - <<'PY'
from pathlib import Path
path = Path('android-app/app/src/main/assets/www/index.html')
html = path.read_text()
html = html.replace('width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover', 'width=640, viewport-fit=cover')
html = html.replace('</head>', '  <link rel="stylesheet" href="./compact.css">\n</head>')
path.write_text(html)
PY
echo "Android web assets updated."
