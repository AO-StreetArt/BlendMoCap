# -*- coding: utf-8 -*-
"""
Created on Mon May 29 03:54:30 2017

Motion Capture Addon

@author: alex
"""

bl_info = {
    "name": "AOMotionCapture", 
    "author": "Alex Barry",
    "version": (0, 0, 1),
    "blender": (2, 78, 0),
    "description": "Blender Add on to assist in the use of using BVH data",
    "category": "Object",
}

import bpy

class CopyBoneRotations(bpy.types.Operator):
    bl_idname = "object.copy_bone_roll"
    bl_label = "Copy Bone Roll"
    bl_options = {'REGISTER', 'UNDO'}
    source = bpy.props.StringProperty(name="SourceObject", default="SourceObject")
    destination = bpy.props.StringProperty(name="DestinationObject", default="DestinationObject")
    
    def execute(self, context):
        
        # Called by blender when the addon is run
        rolls = {}        
        
        # Get the source and target armatures
        src = bpy.context.scene.objects[self.source]
        trg = bpy.context.scene.objects[self.destination]

        # Pull the Roll values from the source armature        
        bpy.context.scene.objects.active = src
        bpy.ops.object.mode_set(mode='EDIT')
        for eb in src.data.edit_bones:
            rolls[eb.name] = eb.roll
            bpy.ops.object.mode_set(mode='POSE')
        
        # Place the Roll values in the target armature
        bpy.context.scene.objects.active = trg
        bpy.ops.object.mode_set(mode='EDIT')
        for eb in trg.data.edit_bones:
            oldRoll = eb.roll
            eb.roll = rolls[eb.name]
            print(eb.name, oldRoll, eb.roll)
        
        #Let's blender know the operator is finished
        return {'FINISHED'}
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
def copy_bone_rot_menu_func(self, context):
    self.layout.operator(CopyBoneRotations.bl_idname) 
        
def register():
    bpy.utils.register_class(CopyBoneRotations)
    bpy.types.VIEW3D_MT_object.append(copy_bone_rot_menu_func)
    
def unregister():
    bpy.types.VIEW3D_MT_object.remove(copy_bone_rot_menu_func)
    bpy.utils.unregister_class(CopyBoneRotations)
    
if __name__ == "__main__":
    register()