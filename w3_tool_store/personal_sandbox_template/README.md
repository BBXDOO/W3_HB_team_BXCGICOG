# W3 Personal Sandbox — reusable template

**Owner:** BBX19  
**Location:** `w3_tool_store/personal_sandbox_template/`  
**Current editable source:** v53 (0.53), 5 Nov 2026; derived from the original v40 snapshot  
**Scope:** W3 internal reuse by a human, a module, or an AI agent. Personal use only at this stage.

## What to copy

Copy the entire `source/` directory to a new project workspace. Each copied sandbox becomes an independent project. Do not write a user's new project data into this template.

`source/` contains the editable React/TypeScript app, Android wrapper, bundled offline web assets, and the Android build workflow. The original v40 bundled assets came from `BBXDOO/W3-personal-sandbox-app` branch `refactor/v0.2`, commit `d3ec48dfb1edcd650cd5e27b8798780e1605f6fe`.

The original W3 systems are not dependencies of the sandbox runtime. The app saves project data on the user's device and supports JSON export/import. No personal project JSON, private key, Android signing key, or `node_modules` is included here.

## Copy and build

1. Copy `source/` to the receiving module's workspace. Rename the copied folder for that module. Keep this template intact.
2. In the copied source folder, run `npm ci`, `npm run lint`, then `sh android-app/sync-web-assets.sh` to rebuild the offline web bundle after edits.
3. For an Android test APK, open `source/android-app/` as an Android project and build `:app:assembleDebug` with JDK 17, Gradle 8.9 and Android SDK 35. Alternatively, copy **the contents** of `source/android-app/` to the root of a separate build repository; its `.github/workflows/build-apk.yml` builds a test APK on `refactor/v0.2`.
4. Before sharing any derived build, check its name, package ID, content, and signing key. A freshly built debug APK may require uninstalling the previous version; export JSON first if it holds data.

To run the browser development view: `npm run dev`. For guidance in Thai, see `source/docs/คู่มือใช้งานภาษาไทย.md` and `source/android-app/README-ANDROID-TH.txt`.

## Reuse boundary

- This is a reusable **starting copy**, not a shared live database. Changes in one copy do not modify the template or another copy.
- A module or agent can propose or prepare its own derived sandbox. It must stay within its assigned workspace and authority; importing the template grants no authority to alter W3 core systems.
- Owner-signed updates are distributed from the separate Android build repository. This reusable source does not contain a signing key; use the original package and owner signing configuration for installed-app updates.
- The W3 repository and the separate Android build repository are public. “Personal use” is the intended use, not a GitHub access restriction. Keep private data and signing keys outside both repositories.

**Source of this snapshot:** `BBXDOO/W3-personal-sandbox-app@d3ec48dfb1edcd650cd5e27b8798780e1605f6fe` for Android bundled assets and wrapper; editable source from the corresponding local W3 Personal Sandbox workspace.

## Current user guide and release checks

- [คู่มือภาษาไทย v53 ครบทุกเมนู](source/docs/คู่มือใช้งานภาษาไทย.md) — also bundled in the app.
- [ขั้นตรวจคู่มือก่อนอัปเดต](source/docs/RELEASE_CHECKLIST_TH.md)
- v52 adds a theme scoped to each board coordinate table.
- Run `npm run review:manual` only after reviewing changed menus; `npm run check:manual` rejects unreviewed source changes. The Android build checks its bundled manual before publishing.

- v53 adds seamless square grids and a project-local Lego image library with single-image/sheet import, repeat placement and JSON backup. Existing rounded/dot modes remain available.
