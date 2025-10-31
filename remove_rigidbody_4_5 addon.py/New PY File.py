bl_info = {
    "name": "Remove Rigid Bodies & Constraints",
    "author": "Cyber King",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Rigid Tools",
    "description": "Removes Rigid Bodies and Constraints from selected objects with one click",
    "category": "Object",
}

import bpy

# ------------------------------
# المشغل (الزر الفعلي)
# ------------------------------
class OBJECT_OT_remove_rigid(bpy.types.Operator):
    """Removes Rigid Bodies and Constraints from selected objects"""
    bl_idname = "object.remove_rigid_data"
    bl_label = "Remove Rigid Bodies"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objs = context.selected_objects
        if not selected_objs:
            self.report({'WARNING'}, "⚠️ No objects selected.")
            return {'CANCELLED'}

        removed_count = 0
        constraint_count = 0

        for obj in selected_objs:
            # Remove Rigid Body
            if obj.rigid_body is not None:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.rigidbody.object_remove()
                removed_count += 1

            # Remove Constraint
            if obj.rigid_body_constraint is not None:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.rigidbody.constraint_remove()
                constraint_count += 1

        # Clear Rigid Body World if exists
        scene = context.scene
        if scene.rigidbody_world:
            try:
                scene.rigidbody_world.point_cache.clear()
                scene.rigidbody_world = None
            except:
                pass

        self.report({'INFO'}, f"✅ Removed {removed_count} Rigid Bodies and {constraint_count} Constraints.")
        return {'FINISHED'}

# ------------------------------
# اللوحة في الشريط الجانبي
# ------------------------------
class VIEW3D_PT_remove_rigid_panel(bpy.types.Panel):
    bl_label = "Rigid Tools"
    bl_idname = "VIEW3D_PT_remove_rigid_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Rigid Tools"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Remove Physics Data:")
        layout.operator("object.remove_rigid_data", icon='TRASH')


# ------------------------------
# التسجيل
# ------------------------------
classes = [OBJECT_OT_remove_rigid, VIEW3D_PT_remove_rigid_panel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
