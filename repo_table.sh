#!/data/data/com.termux/files/usr/bin/bash

OUT="repo-structure.html"

{
  echo '<!doctype html><html><head><meta charset="utf-8">'
  echo '<title>Repository Structure</title>'
  echo '<style>
  body{font-family:Arial,sans-serif;padding:24px}
  table{border-collapse:collapse;width:100%}
  th,td{border:1px solid #ccc;padding:6px 10px;text-align:left}
  th{background:#f2f2f2}
  code{white-space:pre}
  </style></head><body>'
  echo '<h1>Repository Structure</h1>'
  echo '<table>'
  echo '<tr><th>#</th><th>Path</th><th>Type</th><th>Size</th></tr>'

  i=0
  find . \
    -path './.git' -prune -o \
    -path './node_modules' -prune -o \
    -print | sort | while read -r p; do
      i=$((i+1))
      type="file"
      [ -d "$p" ] && type="dir"
      size=$(du -sh "$p" 2>/dev/null | cut -f1)
      safe=$(printf '%s' "$p" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
      echo "<tr><td>$i</td><td><code>$safe</code></td><td>$type</td><td>$size</td></tr>"
    done

  echo '</table></body></html>'
} > "$OUT"

echo "Created: $OUT"
