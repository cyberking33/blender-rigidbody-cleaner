bl_info = {
    "name": "Rigid Tools - Remove Rigid Bodies & Constraints",
    "author": "Cyber King (Cyber Vision Studio™)",
    "version": (1, 2),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Rigid Tools",
    "description": "Easily remove Rigid Bodies or Constraints from selected objects",
    "category": "Object",
}

import bpy

# -------------------------------------------------
# 🔹 OPERATORS
# -------------------------------------------------
class OBJECT_OT_remove_rigid(bpy.types.Operator):
    """Remove Rigid Bodies from selected objects"""
    bl_idname = "object.remove_only_rigid"
    bl_label = "Remove Rigid Bodies Only"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objs = context.selected_objects
        if not selected_objs:
            self.report({'WARNING'}, "⚠️ No objects selected.")
            return {'CANCELLED'}

        removed_count = 0
        for obj in selected_objs:
            if obj.rigid_body is not None:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.rigidbody.object_remove()
                removed_count += 1

        if removed_count == 0:
            self.report({'INFO'}, "No Rigid Bodies found.")
        else:
            self.report({'INFO'}, f"✅ Removed {removed_count} Rigid Bodies.")
        return {'FINISHED'}


class OBJECT_OT_remove_constraints(bpy.types.Operator):
    """Remove Rigid Body Constraints from selected objects"""
    bl_idname = "object.remove_only_constraints"
    bl_label = "Remove Constraints Only"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objs = context.selected_objects
        if not selected_objs:
            self.report({'WARNING'}, "⚠️ No objects selected.")
            return {'CANCELLED'}

        removed_count = 0
        for obj in selected_objs:
            if obj.rigid_body_constraint is not None:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.rigidbody.constraint_remove()
                removed_count += 1

        if removed_count == 0:
            self.report({'INFO'}, "No Constraints found.")
        else:
            self.report({'INFO'}, f"✅ Removed {removed_count} Constraints.")
        return {'FINISHED'}


class OBJECT_OT_remove_all_rigid_data(bpy.types.Operator):
    """Remove both Rigid Bodies and Constraints"""
    bl_idname = "object.remove_all_rigid_data"
    bl_label = "Remove All Physics Data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objs = context.selected_objects
        if not selected_objs:
            self.report({'WARNING'}, "⚠️ No objects selected.")
            return {'CANCELLED'}

        rigid_count = 0
        constraint_count = 0

        for obj in selected_objs:
            if obj.rigid_body is not None:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.rigidbody.object_remove()
                rigid_count += 1

            if obj.rigid_body_constraint is not None:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.rigidbody.constraint_remove()
                constraint_count += 1

        # Clear rigid body world
        scene = context.scene
        if scene.rigidbody_world:
            try:
                scene.rigidbody_world.point_cache.clear()
                scene.rigidbody_world = None
            except:
                pass

        if rigid_count == 0 and constraint_count == 0:
            self.report({'INFO'}, "No Rigid Bodies or Constraints found.")
        else:
            self.report({'INFO'}, f"✅ Removed {rigid_count} Rigid Bodies and {constraint_count} Constraints.")
        return {'FINISHED'}


# -------------------------------------------------
# 🔹 PANEL (Sidebar UI)
# -------------------------------------------------
class VIEW3D_PT_rigid_tools(bpy.types.Panel):
    bl_label = "Rigid Tools"
    bl_idname = "VIEW3D_PT_rigid_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Rigid Tools"

    def draw(self, context):
        layout = self.layout
        selected_count = len(context.selected_objects)

        # Studio name at top
        box = layout.box()
        box.label(text="🔥 Cyber Vision Studio™", icon='FUND')

        # Selected objects info
        box = layout.box()
        box.label(text=f"🧩 Selected Objects: {selected_count}")

        # Buttons
        layout.label(text="Remove Physics Data:")
        layout.operator("object.remove_only_rigid", icon='PHYSICS')
        layout.operator("object.remove_only_constraints", icon='CONSTRAINT')
        layout.operator("object.remove_all_rigid_data", icon='TRASH')


# -------------------------------------------------
# 🔹 REGISTRATION
# -------------------------------------------------
classes = [
    OBJECT_OT_remove_rigid,
    OBJECT_OT_remove_constraints,
    OBJECT_OT_remove_all_rigid_data,
    VIEW3D_PT_rigid_tools
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
