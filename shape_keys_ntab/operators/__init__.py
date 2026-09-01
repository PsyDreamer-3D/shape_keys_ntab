# SPDX-License-Identifier: GPL-2.0-or-later

from .shape_key_ops import (
    OBJECT_OT_shapekey_add_ntab,
    OBJECT_OT_shapekey_clear_ntab,
    OBJECT_OT_shapekey_new_from_mix_ntab,
    OBJECT_OT_shapekey_remove_ntab,
)

classes = (
    OBJECT_OT_shapekey_add_ntab,
    OBJECT_OT_shapekey_remove_ntab,
    OBJECT_OT_shapekey_new_from_mix_ntab,
    OBJECT_OT_shapekey_clear_ntab,
)


def register():
    import bpy
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    import bpy
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
