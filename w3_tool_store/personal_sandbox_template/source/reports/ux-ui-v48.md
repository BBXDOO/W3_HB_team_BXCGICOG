# Personal Sandbox v48 — UX/UI

2026-10-29. Requested by BBX19; publish directly through the existing in-app updater, without a PR.

- Shared charcoal surfaces, inset fields, raised cards and buttons, orange primary action and restrained purple/blue navigation accents.
- Source-level removal of literal forest panel colors across editor pages and dialogs; all selected palettes use shared surface variables.
- Device-width viewport, responsive header, labelled Thai navigation, readable input sizing, offline Noto Sans Thai (OFL).
- Preview now starts beside navigation, keeping all destinations reachable. Drawer, preview resizing, project data and runtime rules remain functional.
- Update button is now a React control calling the existing AndroidBridge.checkUpdate method; the fragile post-render DOM injection is removed from the APK.
- Source and APK bundled web assets are rebuilt from the same output. Release repository: BBXDOO/W3-personal-sandbox-app, branch refactor/v0.2, versionCode 48.

## Validation

- npm run lint and npm run build passed.
- Chromium touchscreen simulation at 412 × 915: all 11 editor destinations open; no uncaught page errors or document horizontal overflow.
- Existing forest project migrates to instrument default; description preserved. Added and renamed an item, autosaved, reloaded and reopened with data intact.
- Dark and light palette switching verified; update bridge invoked exactly once per click.
- Inspected mobile Home/Item, light theme dialog, and desktop 1280 × 900 screenshots. This is browser validation; physical-device APK installation remains to be performed by the owner through the update button.
