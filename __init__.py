# bl_info
bl_info = {
    "name": "Quick Chain",
    "description": "quick create physics chain",
    "author": "Masato Suemura",
    "version": (1, 0, 0),
    "blender": (2, 82, 0),
    "support": "TESTING",
    "category": "Mesh",
    "location": "View3D > Sidebar > View Tab",
    "warning": "",
    "wiki_url": "",
    "tracker_url": ""
}

import bpy
import os.path


class QCA_PT_tools(bpy.types.Panel):
    bl_label = "Quick Chain"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "QuickChain"

    # properties
    bpy.types.Scene.chain_count = bpy.props.IntProperty(name = "", default=30)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        col = layout.column(align=True)

        col.label(text="import chain")
        col.prop(scene, "chain_count", text="")
        col.operator("qcr.import", text="Create")

class QCA_OT_ImportOperator(bpy.types.Operator):
    bl_idname = "qcr.import"
    bl_label = "apply lut"
    bl_options = {"REGISTER", "UNDO"}

    def setting_simulation(self, context):
        bpy.context.view_layer.objects.active = bpy.data.objects[0]
        bpy.ops.object.mode_set(mode = 'OBJECT')
        Chain_Base = bpy.data.objects["Chain_Base"]
        bpy.context.view_layer.objects.active = Chain_Base
        Chain_Base.modifiers["Array"].count = context.scene["chain_count"]
        # モディファイア適用 -> 個別に分割 -> 原点をオブジェクトの中心に
        for mod in Chain_Base.modifiers:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')

    def link_chain(self, context):
        Chain_Base = bpy.data.objects["Chain_Base"]
        # コレクションを新規作成
        new_collection = bpy.data.collections.new('Chain')
        # シーンにコレクションをリンク
        bpy.context.scene.collection.children.link(new_collection)
        ###コレクションにオブジェクトをリンク
        new_collection.objects.link(Chain_Base)
        #もとのコレクションとのリンク削除
        bpy.context.scene.collection.objects.unlink(Chain_Base)

    def execute(self, context):
        current_dir = os.path.dirname(__file__)
        fp = current_dir + "\\chain_base.blend\\Object\\"
        bpy.ops.wm.append(filename="Chain_Base", directory=fp)
        self.link_chain(context)
        self.setting_simulation(context)

        return {"FINISHED"}


def register():
    for cls in classes:
        print("Register : " + str(cls))
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

classes = [
    QCA_PT_tools,
    QCA_OT_ImportOperator
]

if __name__ == '__main__':
    register()
