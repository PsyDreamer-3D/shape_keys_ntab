# SPDX-License-Identifier: GPL-2.0-or-later

from .panels import (
    OBJECT_UL_shapekeys_ntab,
    VIEW3D_MT_shape_keys_ntab_specials,
    VIEW3D_PT_shape_keys_ntab,
)

classes = (
    OBJECT_UL_shapekeys_ntab,
    VIEW3D_MT_shape_keys_ntab_specials,
    VIEW3D_PT_shape_keys_ntab,
)


def register():
    import bpy
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    import bpy
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
