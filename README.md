# Shape Keys (N-Panel)

Puts Blender's Shape Keys panel in the 3D Viewport sidebar (N-panel), under its own **Shape Keys** tab, so switching active shape keys or scrubbing a value doesn't require leaving the viewport for Properties.

## Requirements

- Blender 5.1.0 or later

## Installation

1. In Blender, open **Edit → Preferences → Get Extensions**.
2. Click the dropdown → **Install from Disk** and select the built `shape_keys_ntab` zip (or point it at the `shape_keys_ntab/` folder for a dev install).
3. Enable **Shape Keys (N-Panel)** in the extensions list.
4. Open the 3D Viewport, press `N`, and look for the **Shape Keys** tab.

## Usage

- **Add / Remove** — the +/- buttons next to the list.
- **Specials menu (▾)** — Move to Top/Up/Down/Bottom, Clear Values.
- **Value slider** — shown for the active (non-Basis) key, with a min/max range below it. A small driver icon (⚡) appears next to the slider when the value is driven.
- **Vertex Group** / **Relative To** — same fields as the Properties editor's Shape Keys panel.
- **New Shape From Mix** — bakes the current mix of enabled shape keys into a new key.
- **Mirror** — topology-aware mirror of the active shape key.

Works on Mesh, Curve, Surface, and Lattice objects — anything that can own shape keys.

## How it works

The list uses a small add-on-owned UIList (`OBJECT_UL_shapekeys_ntab`) rather than Blender's built-in `MESH_UL_shape_keys` — that class lives in a bundled `bl_ui` startup *script*, not stable `bpy.types` API, and as of Blender 5.2 it's no longer registered under that name. Owning the row layout means double-click-to-rename and the mute toggle keep working regardless of future `bl_ui` reshuffles. All list/value mutation goes through the `Object`/`Key` RNA API directly (`obj.shape_key_add`, `obj.shape_key_remove`, `kb.value = ...`), never `bpy.ops`.

Two intentional exceptions call Blender's built-in operators directly, since neither has a `bpy.data`-level equivalent:

- `object.shape_key_move` — reordering; the `key_blocks` collection exposes no `move()` method.
- `object.shape_key_mirror` — topology-aware mirroring depends on Blender's internal mesh-symmetry cache.

Driver detection reads `key.animation_data.drivers` and matches on `kb.path_from_id("value")` — drivers on shape key values live on the `Key` datablock's `animation_data`, not on the key block itself.

## Out of scope

- No Scene-level settings/preferences yet — `properties/` is an intentional empty stub (see `CLAUDE.md`).
- No custom drag-reorder in the list; reordering goes through the specials menu.
