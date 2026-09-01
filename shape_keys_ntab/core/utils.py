# SPDX-License-Identifier: GPL-2.0-or-later

import bpy

# N-panel tab name shared by every Panel in ui/panels.py.
_TAB = "Shape Keys"

# Object types that can own a Key datablock (shape keys).
SHAPE_KEY_OBJECT_TYPES = {'MESH', 'CURVE', 'SURFACE', 'LATTICE'}


def has_shape_keys(obj) -> bool:
    """True if *obj* is a shape-key-capable type that already has a Key datablock."""
    return (
        obj is not None
        and obj.type in SHAPE_KEY_OBJECT_TYPES
        and obj.data is not None
        and getattr(obj.data, "shape_keys", None) is not None
    )


def find_value_driver(kb):
    """Return the FCurve driving a shape key's value, or None.

    Drivers on shape key values live on the *Key* datablock's
    animation_data.drivers, independently of any Action — they are not
    reachable through the key block itself.
    """
    key = kb.id_data
    anim_data = key.animation_data
    if not anim_data:
        return None
    data_path = kb.path_from_id("value")
    for fcurve in anim_data.drivers:
        if fcurve.data_path == data_path:
            return fcurve
    return None


def _write_report(context, text_name: str, lines: list[str]) -> None:
    """Write *lines* to a bpy.data.texts block and focus any open Text Editor on it.

    Use this instead of print() for anything a person needs to read — on
    Linux the Blender system console isn't reachable from the UI. Not
    called anywhere in this add-on yet (nothing here produces multi-line
    diagnostic output), but kept available per house convention for
    whichever operator needs it first.
    """
    if text_name in bpy.data.texts:
        tb = bpy.data.texts[text_name]
        tb.clear()
    else:
        tb = bpy.data.texts.new(text_name)
    tb.write("\n".join(lines))
    for area in context.screen.areas:
        if area.type == 'TEXT_EDITOR':
            area.spaces.active.text = tb
            break
