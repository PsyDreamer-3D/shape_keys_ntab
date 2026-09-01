# SPDX-License-Identifier: GPL-2.0-or-later

"""Shape Keys panel, hosted in its own N-panel tab.

Uses a small hand-rolled UIList (OBJECT_UL_shapekeys_ntab below) rather
than borrowing Blender's built-in MESH_UL_shape_keys. That class lives
in bl_ui/properties_data_mesh.py — a bundled startup *script*, not
stable bpy.types API — and as of Blender 5.2 it's no longer registered
under that name (template_list raises "List type MESH_UL_shape_keys
not found"). Owning our own UIList means we don't break again the next
time Blender reshuffles its bl_ui internals.
"""

from bpy.types import Menu, Panel, UIList

from ..core.utils import SHAPE_KEY_OBJECT_TYPES, _TAB, find_value_driver


class OBJECT_UL_shapekeys_ntab(UIList):
    """Shape key row: editable name + a mute (eye) toggle."""

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        key_block = item
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(key_block, "name", text="", emboss=False, icon='SHAPEKEY_DATA')
            row.prop(
                key_block, "mute", text="", emboss=False,
                icon='HIDE_ON' if key_block.mute else 'HIDE_OFF',
            )
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon='SHAPEKEY_DATA')


class VIEW3D_MT_shape_keys_ntab_specials(Menu):
    bl_label = "Shape Key Specials"

    def draw(self, context):
        layout = self.layout
        # Reordering has no bpy.data-level equivalent — the key_blocks
        # collection exposes no move() method — so this is an
        # intentional bpy.ops exception, same as object.convert.
        layout.operator("object.shape_key_move", icon='TRIA_UP_BAR', text="Move to Top").type = 'TOP'
        layout.operator("object.shape_key_move", icon='TRIA_UP', text="Move Up").type = 'UP'
        layout.operator("object.shape_key_move", icon='TRIA_DOWN', text="Move Down").type = 'DOWN'
        layout.operator("object.shape_key_move", icon='TRIA_DOWN_BAR', text="Move to Bottom").type = 'BOTTOM'
        layout.separator()
        layout.operator("object.shapekey_clear_ntab", text="Clear Values", icon='X')


class VIEW3D_PT_shape_keys_ntab(Panel):
    bl_label = "Shape Keys"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = _TAB

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj is not None and obj.type in SHAPE_KEY_OBJECT_TYPES and obj.data is not None

    def draw(self, context):
        layout = self.layout
        obj = context.object
        key = obj.data.shape_keys

        row = layout.row()
        if key is None:
            row.operator("object.shapekey_add_ntab", icon='ADD')
            return

        row.template_list(
            "OBJECT_UL_shapekeys_ntab", "",
            key, "key_blocks",
            obj, "active_shape_key_index",
            rows=5,
        )

        col = row.column(align=True)
        col.operator("object.shapekey_add_ntab", icon='ADD', text="")
        col.operator("object.shapekey_remove_ntab", icon='REMOVE', text="")
        col.separator()
        col.menu("VIEW3D_MT_shape_keys_ntab_specials", icon='DOWNARROW_HLT', text="")

        kb = obj.active_shape_key
        index = obj.active_shape_key_index
        if kb is None:
            return

        col = layout.column()
        col.use_property_split = True

        if key.use_relative:
            if index > 0:
                driver = find_value_driver(kb)

                value_row = col.row(align=True)
                value_row.prop(kb, "value", slider=True)
                if driver is not None:
                    value_row.label(text="", icon='DRIVER')

                split = col.split(factor=0.5, align=True)
                split.prop(kb, "slider_min", text="Min")
                split.prop(kb, "slider_max", text="Max")

                col.prop_search(kb, "vertex_group", obj, "vertex_groups", text="Vertex Group")
                col.prop_search(kb, "relative_key", key, "key_blocks", text="Relative To")
        else:
            col.prop(key, "eval_time")

        layout.separator()
        row = layout.row(align=True)
        row.operator("object.shapekey_new_from_mix_ntab", icon='SHAPEKEY_DATA')
        # Topology-aware mirroring has no bpy.data-level equivalent — it
        # depends on Blender's internal mesh-symmetry cache — so this
        # calls the stock operator directly rather than reimplementing
        # symmetry detection by hand.
        row.operator("object.shape_key_mirror", text="Mirror", icon='ARROW_LEFTRIGHT')
