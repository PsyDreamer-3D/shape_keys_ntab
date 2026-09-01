# SPDX-License-Identifier: GPL-2.0-or-later

"""Shape key operators.

Every operator here mutates data via the bpy.data / RNA API directly
(obj.shape_key_add, obj.shape_key_remove, kb.value assignment, etc.),
never via bpy.ops. The two exceptions — reordering a shape key in the
list and topology-based mirroring — are called directly from
ui/panels.py, with a comment explaining why: neither has a
bpy.data-level equivalent.
"""

from bpy.types import Operator

from ..core.utils import SHAPE_KEY_OBJECT_TYPES, has_shape_keys


class OBJECT_OT_shapekey_add_ntab(Operator):
    """Add a new shape key to the active object"""
    bl_idname = "object.shapekey_add_ntab"
    bl_label = "Add Shape Key"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj is not None and obj.type in SHAPE_KEY_OBJECT_TYPES and obj.data is not None

    def execute(self, context):
        obj = context.object
        is_first = obj.data.shape_keys is None
        kb = obj.shape_key_add(name="Basis" if is_first else "Key", from_mix=False)
        obj.active_shape_key_index = len(obj.data.shape_keys.key_blocks) - 1
        self.report({'INFO'}, f"Added shape key '{kb.name}'")
        return {'FINISHED'}


class OBJECT_OT_shapekey_remove_ntab(Operator):
    """Remove the active shape key from the active object"""
    bl_idname = "object.shapekey_remove_ntab"
    bl_label = "Remove Shape Key"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return has_shape_keys(obj) and obj.active_shape_key is not None

    def execute(self, context):
        obj = context.object
        kb = obj.active_shape_key
        name = kb.name
        obj.shape_key_remove(kb)
        self.report({'INFO'}, f"Removed shape key '{name}'")
        return {'FINISHED'}


class OBJECT_OT_shapekey_new_from_mix_ntab(Operator):
    """Create a new shape key baked from the current mix of enabled shape keys"""
    bl_idname = "object.shapekey_new_from_mix_ntab"
    bl_label = "New Shape From Mix"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return has_shape_keys(context.object)

    def execute(self, context):
        obj = context.object
        kb = obj.shape_key_add(name="Mix", from_mix=True)
        obj.active_shape_key_index = len(obj.data.shape_keys.key_blocks) - 1
        self.report({'INFO'}, f"Added '{kb.name}' from mix")
        return {'FINISHED'}


class OBJECT_OT_shapekey_clear_ntab(Operator):
    """Reset every shape key value on the active object to 0"""
    bl_idname = "object.shapekey_clear_ntab"
    bl_label = "Clear Shape Key Values"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return has_shape_keys(context.object)

    def execute(self, context):
        key = context.object.data.shape_keys
        for kb in key.key_blocks:
            kb.value = 0.0
        self.report({'INFO'}, "Cleared shape key values")
        return {'FINISHED'}
