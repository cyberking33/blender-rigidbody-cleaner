import bpy

# Ensure we are in Object Mode
if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

# Get selected objects
selected_objs = bpy.context.selected_objects

if not selected_objs:
    print("⚠️ No objects selected.")
else:
    removed_count = 0
    constraint_count = 0

    for obj in selected_objs:
        # Remove Rigid Body (if it exists)
        if obj.rigid_body is not None:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.rigidbody.object_remove()
            removed_count += 1

        # Remove Rigid Body Constraint (if it exists)
        if obj.rigid_body_constraint is not None:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.rigidbody.constraint_remove()
            constraint_count += 1

    # Check if Rigid Body World exists and clear it if not used
    scene = bpy.context.scene
    if scene.rigidbody_world:
        try:
            scene.rigidbody_world.point_cache.clear()
            scene.rigidbody_world = None
        except:
            pass

    print(f"✅ Removed {removed_count} Rigid Bodies and {constraint_count} Constraints from selected objects.")
