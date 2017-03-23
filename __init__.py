import bpy
from bpy.props import StringProperty

bl_info = {
    "name": "selection splitter into groups",
    "author": "Drunkar",
    "version": (0, 1),
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
        items = []
        items_x = {}
        items_y = {}
        items_z = {}
        for obj in bpy.data.objects.items():
            if bpy.data.objects[obj[0]].select:
                name = bpy.data.objects[obj[0]].name
                items.append(name)
                items_x['"' + str(name) + '"'] = bpy.data.objects[obj[0]].location[0]
                items_y['"' + str(name) + '"'] = bpy.data.objects[obj[0]].location[1]
                items_z['"' + str(name) + '"'] = bpy.data.objects[obj[0]].location[2]
        items.sort()
        items = ['"' + str(item) + '"' for item in items]
        x_asc = [k for k, v in sorted(items_x.items(), key=lambda x:x[1])]
        y_asc = [k for k, v in sorted(items_y.items(), key=lambda x:x[1])]
        z_asc = [k for k, v in sorted(items_z.items(), key=lambda x:x[1])]
        context.scene.selection_splitter_id_asc = ",".join(items)
        context.scene.selection_splitter_x_asc = ",".join(x_asc)
        context.scene.selection_splitter_y_asc = ",".join(y_asc)
        context.scene.selection_splitter_z_asc = ",".join(z_asc)
        return {"FINISHED"}

    def draw(self, context):
        col = self.layout.column(align=True)
        col.prop(context.scene, "selection_splitter_id_asc")
        col.prop(context.scene, "selection_splitter_x_asc")
        col.prop(context.scene, "selection_splitter_y_asc")
        col.prop(context.scene, "selection_splitter_z_asc")


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
    bpy.types.Scene.selection_splitter_id_asc = bpy.props.StringProperty(
        name="id asc",
        description="id in group",
        default="default")
    bpy.types.Scene.selection_splitter_x_asc = bpy.props.StringProperty(
        name="x asc",
        description="id in group",
        default="default")
    bpy.types.Scene.selection_splitter_y_asc = bpy.props.StringProperty(
        name="y asc",
        description="id in group",
        default="default")
    bpy.types.Scene.selection_splitter_z_asc = bpy.props.StringProperty(
        name="z asc",
        description="id in group",
        default="default")
    register_shortcut()


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.selection_splitter_id_asc
    del bpy.types.Scene.selection_splitter_x_asc
    del bpy.types.Scene.selection_splitter_y_asc
    del bpy.types.Scene.selection_splitter_z_asc


if __name__ == "__main__":
    register()
