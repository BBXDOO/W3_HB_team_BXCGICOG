# W3 Personal Sandbox — working copy

This is a separate working copy of the W3.IDP Studio source supplied by BBX19. The original ZIP and the GitHub source are unchanged.

## Current checkpoint (2026-10-13)

- Independent working copy; original export and GitHub repository have not been changed.
- Home creates separate clean projects in Library, BG–Bookcraft, or Concept mind map mode. Playtest uses a configurable per-project reader menu, visual style, and touch-selectable board.
- Board and Location records remain distinct. Rules are editable reference text. Events are separate executable records.
- The Events editor exposes trigger, condition, priority, cooldown, spatial anchor, process steps, and outcome fields. Playtest runs **explicit OnInteract** events with supported numeric HP/MP/EN checks, a Self message, and numeric HP/MP/EN changes. Unsupported steps stop without applying a partial outcome. This does not implement all event types, movement, combat, or an interpreter for Rules text.
- Runtime vitals and interaction log belong to project-local progress, separate from authored project data. Save Progress is explicit. JSON export now bundles authored data and the latest saved progress; unsaved Playtest changes are not included. Import accepts both the new backup envelope and legacy project-only JSON and asks before replacing an existing project ID.
- Writes report storage failure and offer project JSON export. Browser localStorage still needs a durable database/backup migration for primary long-term use.
- Removed remote font/noise/icon references and disabled direct in-browser Gemini calls and API key embedding. The AI button now explains its offline state. A same-origin service worker caches the production shell after first online load; device offline behavior has not been verified yet.
- The earlier in-app source ZIP link pointed to a nonexistent file and has been replaced with project JSON export and honest install guidance. Source bundle is delivered separately.
- Rules editor now supports nested blocks with readable numbered hierarchy and preserves legacy flat blocks. A condition label is not an executable rule.
- Playtest now has local dice (d4/d6/d8/d10/d12/d20/d100), per-character board positions separate from cell selection, and explicit progress saving for position, dice history, and event log. A Thai guide is available from the editor top bar and `docs/คู่มือใช้งานภาษาไทย.md`.
- Cards and modules have separate project-local registries and 2 or 3 reference slots. Legacy card text remains readable. Playtest can trace assembled modules in slot order and A/B/C order. It recognizes only PASS and DISPLAY: literal text; unrecognized logic yields UNKNOWN and missing references or empty DISPLAY yield ERROR. This read-only trace does not execute effects or determine Grade/Access compatibility.
- Rules can evaluate declared condition blocks against a manually supplied JSON context, using arbitrary project-owned input keys and safe scalar comparisons. Prose remains prose. Command references are stored but not executed; no state changes or automatic integration with board, cards, or events yet.
- Playtest can explicitly evaluate Rules against a snapshot of selected project, board, cell, location, character, story and last selected item/card/event data. It shows the exact snapshot and trace. This is read-only and not an automatic trigger or command executor.
- Common Play is a project-local command registry with stable IDs, labels, descriptions, and required input paths. Rule references resolve against this registry; missing IDs yield ERROR, known but unimplemented commands yield UNKNOWN. Registry definitions are saved in project backups; no generic prose execution or mutation is implied.
- `npm run lint` and `npm run build` passed on 2026-10-13.

## Run

```bash
npm ci
npm run dev
```

## Still to do

- Test layout, touch controls, saving, and offline reopening on the target Android device.
- Migrate primary data beyond browser localStorage. The combined JSON backup can now restore progress, but localStorage reliability and Android storage behavior still need device testing.
- Add and test a local Android package. No APK exists at this checkpoint.
- Define card/module compatibility, 2–3 slot composition, and swaps through project-scoped rules before implementing their execution. Expand other event/rule behavior only against explicit definitions; add optional external connectors as opt-in later.
- Apply remaining theme/content changes with the owner's feedback.

`npm run lint` checks TypeScript; `npm run build` creates `dist/`. Neither verifies Android installation.
