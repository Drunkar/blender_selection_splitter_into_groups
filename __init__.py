import re
import bpy
from bpy.props import StringProperty

bl_info = {
    "name": "selection splitter into groups",
    "author": "Drunkar",
    "version": (0, 2),
    "blender": (2, 7, 8),
    "location": "3D View, Ctrl + Alt + S",
    "description": "Split select object into specific groups and print ids.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"
}


addon_keymaps = []


class SeectionSplitter(bpy.types.Operator):

    bl_idname = "3dview.selection_splitter_into_groups"
    bl_label = "selection splitter into groups"
    bl_description = "Split select object into specific groups and print ids."
    bl_options = {"REGISTER", "UNDO"}

    # main
    def execute(self, context):
        item_names = []
        items = []
        items_x = {}
        items_y = {}
        items_z = {}
        item_parents_x = {}
        item_parents_y = {}
        item_parents_z = {}
        for obj in bpy.context.selected_objects:
            matched = re.search(context.scene.selection_splitter_id_key, obj.name)
            if obj.select and matched:
                item_names.append(obj.name)
                items.append(matched.group(0))
                items_x['"' + str(matched.group(0)) + '"'] = obj.location[0]
                items_y['"' + str(matched.group(0)) + '"'] = obj.location[1]
                items_z['"' + str(matched.group(0)) + '"'] = obj.location[2]
        items.sort()
        items = ['"' + str(item) + '"' for item in items]
        x_asc = [k for k, v in sorted(items_x.items(), key=lambda x:x[1])]
        y_asc = [k for k, v in sorted(items_y.items(), key=lambda x:x[1])]
        z_asc = [k for k, v in sorted(items_z.items(), key=lambda x:x[1])]
        context.scene.selection_splitter_id_asc = ",".join(items)
        context.scene.selection_splitter_x_asc = ",".join(x_asc)
        context.scene.selection_splitter_y_asc = ",".join(y_asc)
        context.scene.selection_splitter_z_asc = ",".join(z_asc)
        items.reverse()
        x_asc.reverse()
        y_asc.reverse()
        z_asc.reverse()
        context.scene.selection_splitter_id_desc = ",".join(items)
        context.scene.selection_splitter_x_desc = ",".join(x_asc)
        context.scene.selection_splitter_y_desc = ",".join(y_asc)
        context.scene.selection_splitter_z_desc = ",".join(z_asc)

        # parent
        item_parents = [bpy.data.objects[i].parent for i in item_names if bpy.data.objects[i].parent]
        if len(list(set(item_parents))) > 0:
            item_parents = [i.name for i in item_parents]
            for i, obj in enumerate(item_parents):
                matched = re.search(context.scene.selection_splitter_id_key, item_names[i])
                if matched:
                    item_parents_x['"' + str(matched.group(0)) + '"'] = bpy.data.objects[obj].location[0]
                    item_parents_y['"' + str(matched.group(0)) + '"'] = bpy.data.objects[obj].location[1]
                    item_parents_z['"' + str(matched.group(0)) + '"'] = bpy.data.objects[obj].location[2]
            parent_x_asc = [k for k, v in sorted(item_parents_x.items(), key=lambda x:x[1])]
            parent_y_asc = [k for k, v in sorted(item_parents_y.items(), key=lambda x:x[1])]
            parent_z_asc = [k for k, v in sorted(item_parents_z.items(), key=lambda x:x[1])]
        else:
            item_parents = []
            parent_x_asc = []
            parent_y_asc = []
            parent_z_asc = []
        context.scene.selection_splitter_parent_id_asc = ",".join(item_parents)
        context.scene.selection_splitter_parent_x_asc = ",".join(parent_x_asc)
        context.scene.selection_splitter_parent_y_asc = ",".join(parent_y_asc)
        context.scene.selection_splitter_parent_z_asc = ",".join(parent_z_asc)
        item_parents.reverse()
        parent_x_asc.reverse()
        parent_y_asc.reverse()
        parent_z_asc.reverse()
        context.scene.selection_splitter_parent_id_desc = ",".join(item_parents)
        context.scene.selection_splitter_parent_x_desc = ",".join(parent_x_asc)
        context.scene.selection_splitter_parent_y_desc = ",".join(parent_y_asc)
        context.scene.selection_splitter_parent_z_desc = ",".join(parent_z_asc)

        return {"FINISHED"}

    def draw(self, context):
        col = self.layout.column(align=True)
        col.prop(context.scene, "selection_splitter_id_key")
        col.prop(context.scene, "selection_splitter_id_asc")
        col.prop(context.scene, "selection_splitter_x_asc")
        col.prop(context.scene, "selection_splitter_y_asc")
        col.prop(context.scene, "selection_splitter_z_asc")
        col.prop(context.scene, "selection_splitter_id_desc")
        col.prop(context.scene, "selection_splitter_x_desc")
        col.prop(context.scene, "selection_splitter_y_desc")
        col.prop(context.scene, "selection_splitter_z_desc")
        col.prop(context.scene, "selection_splitter_parent_id_asc")
        col.prop(context.scene, "selection_splitter_parent_x_asc")
        col.prop(context.scene, "selection_splitter_parent_y_asc")
        col.prop(context.scene, "selection_splitter_parent_z_asc")
        col.prop(context.scene, "selection_splitter_parent_id_desc")
        col.prop(context.scene, "selection_splitter_parent_x_desc")
        col.prop(context.scene, "selection_splitter_parent_y_desc")
        col.prop(context.scene, "selection_splitter_parent_z_desc")

    def invoke(self, context, event):
        if context.scene.selection_splitter_x_asc in vars():
            context.scene.selection_splitter_x_asc = None
            context.scene.selection_splitter_y_asc = None
            context.scene.selection_splitter_z_asc = None
        return context.window_manager.invoke_props_dialog(self)


def menu_func(self, context):
    self.layout.operator(SeectionSplitter.bl_idname)


def register_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        # register shortcut in 3d view
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        # key
        kmi = km.keymap_items.new(
            idname=SeectionSplitter.bl_idname,
            type="S",
            value="PRESS",
            shift=False,
            ctrl=True,
            alt=True)
        # register to shortcut key list
        addon_keymaps.append((km, kmi))


def unregister_shortcut():
    for km, kmi in addon_keymaps:
        # unregister shortcut key
        km.keymap_items.remove(kmi)
    # clear shortcut key list
    addon_keymaps.clear()


def register():
    unregister_shortcut()
    bpy.utils.register_module(__name__)
    bpy.types.Scene.selection_splitter_id_key = bpy.props.StringProperty(
        name="id key (regular expression)",
        description="select object only whichmatches to this expression.",
        default="")
    bpy.types.Scene.selection_splitter_id_asc = bpy.props.StringProperty(
        name="id asc",
        description="id in group",
        default="for output only")
    bpy.types.Scene.selection_splitter_x_asc = bpy.props.StringProperty(
        name="x asc",
        description="id in group",
        default="for output only")
    bpy.types.Scene.selection_splitter_y_asc = bpy.props.StringProperty(
        name="y asc",
        description="id in group",
        default="for output only")
    bpy.types.Scene.selection_splitter_z_asc = bpy.props.StringProperty(
        name="z asc",
        description="id in group",
        default="for output only")
    bpy.types.Scene.selection_splitter_id_desc = bpy.props.StringProperty(
        name="id desc",
        description="id in group",
        default="for output only")
    bpy.types.Scene.selection_splitter_x_desc = bpy.props.StringProperty(
        name="x desc",
        description="id in group",
        default="for output only")
    bpy.types.Scene.selection_splitter_y_desc = bpy.props.StringProperty(
        name="y desc",
        description="id in group",
        default="for output only")
    bpy.types.Scene.selection_splitter_z_desc = bpy.props.StringProperty(
        name="z asc",
        description="id in group",
        default="for output only")
    bpy.types.Scene.selection_splitter_parent_id_asc = bpy.props.StringProperty(
        name="parent id asc",
        description="parent id in group",
        default="for output only")
    bpy.types.Scene.selection_splitter_parent_x_asc = bpy.props.StringProperty(
        name="parent x asc",
        description="parent id in group",
        default="for output only")
    bpy.types.Scene.selection_splitter_parent_y_asc = bpy.props.StringProperty(
        name="parent y asc",
        description="parent id in group",
        default="for output only")
    bpy.types.Scene.selection_splitter_parent_z_asc = bpy.props.StringProperty(
        name="parent z asc",
        description="parent id in group",
        default="for output only")
    bpy.types.Scene.selection_splitter_parent_id_desc = bpy.props.StringProperty(
        name="parent id desc",
        description="parent id in group",
        default="for output only")
    bpy.types.Scene.selection_splitter_parent_x_desc = bpy.props.StringProperty(
        name="parent x desc",
        description="parent id in group",
        default="for output only")
    bpy.types.Scene.selection_splitter_parent_y_desc = bpy.props.StringProperty(
        name="parent y desc",
        description="parent id in group",
        default="for output only")
    bpy.types.Scene.selection_splitter_parent_z_desc = bpy.props.StringProperty(
        name="parent z desc",
        description="parent id in group",
        default="for output only")
    register_shortcut()


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.selection_splitter_id_key
    del bpy.types.Scene.selection_splitter_id_asc
    del bpy.types.Scene.selection_splitter_x_asc
    del bpy.types.Scene.selection_splitter_y_asc
    del bpy.types.Scene.selection_splitter_z_asc


if __name__ == "__main__":
    register()
