# Shape Keys (N-Panel)

Blender 5.1+ add-on. All source code lives in `shape_keys_ntab/`.

See the `blender-addon-scaffold` skill for project-wide development guidelines (hot-reload pattern, bpy.ops rules, structure conventions). If this repo ends up sitting alongside other add-on projects in one workspace, those conventions are also worth promoting to a physical `AGENTS.md` at the workspace root.

## Key design decisions

- Uses a hand-rolled UIList (`ui/panels.py::OBJECT_UL_shapekeys_ntab`) rather than borrowing Blender's built-in `MESH_UL_shape_keys`. That class lives in `bl_ui/properties_data_mesh.py`, a bundled startup script — not stable `bpy.types` API — and as of Blender 5.2 it's no longer registered under that name (`template_list` raised "List type MESH_UL_shape_keys not found" at runtime). Don't reuse other `bl_ui`-internal class names elsewhere in this add-on without checking they're still registered on the target Blender version first.
- `object.shape_key_move` and `object.shape_key_mirror` are called directly from `ui/panels.py` rather than reimplemented — both are documented exceptions to the no-`bpy.ops` rule (list reordering has no `bpy.data` equivalent; mirror depends on Blender's internal mesh-symmetry cache).
- Driver detection (`core/utils.py::find_value_driver`) reads `key.animation_data.drivers`, not the key block's own animation_data — drivers on shape key values are stored on the owning `Key` datablock.
- `properties/` is an intentional empty stub — this add-on has no Scene-level settings yet.

## Testing

Install via Blender Preferences → Get Extensions → Install from Disk, pointing at the built zip (or the `shape_keys_ntab/` folder for a dev install).

Manual smoke test:

1. Select a mesh with no shape keys → **Shape Keys** tab in the N-panel shows only an Add button.
2. Click Add twice → list shows "Basis" and "Key" rows; value slider appears for "Key".
3. Double-click "Key" in the list → rename inline.
4. Click **New Shape From Mix** → new key appears baked from current values.
5. Right-click the value slider → **Add Driver** → driver icon (⚡) appears next to the slider.
6. Specials menu (▾) → Move Up/Down reorders the list; Clear Values zeroes every slider.
