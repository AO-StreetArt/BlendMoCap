# -*- coding: utf-8 -*-
"""
Created on Mon May 29 03:54:30 2017

Motion Capture Addon

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

@author: alex barry
"""

bl_info = {
    "name": "BlendMoCap",
    "author": "Alex Barry",
    "version": (0, 0, 1),
    "blender": (2, 78, 0),
    "description": "Blender Add on to assist in the use of using BVH data",
    "category": "Object",
}

import bpy
import time

# TO-DO: Transform the mocap constraints to keyframes
def createMocapKeyframes(src, trg, keyframe_interval):
    print("Creating Motion Capture Keyframes on %s with target %s" % (src.name, trg.name))

# Select an object and switch to pose mode
def selectAndPose(src):
    # Deselect everything
    for ob in bpy.context.selected_objects:
        ob.select = False

    # Select the source armature
    src.select = True
    bpy.context.scene.objects.active = src

    # Set pose mode and select all the bones in the armature
    bpy.ops.object.mode_set(mode='POSE')

# Removes the mocap constraints
def removeMocapConstraints(src):
    print("Removing Motion Capture Constraints from %s" % (src.name))

    selectAndPose(src)
    bpy.ops.pose.select_all(action='SELECT')

    # iterate over the pose bones
    for bone in bpy.context.selected_pose_bones:
        for c in bone.constraints:
            if c.type == 'COPY_ROTATION' or c.type == 'COPY_LOCATION':
                bone.constraints.remove(c)

# Copy the roll values for all bones in one armature to another
# TO-DO: Only map to the target bones that were taken from the source
def copyBoneRolls(src, trg):
    # Setup
    rolls = {}

    print("Pulling Bone Roll from Source")

    # Pull the Roll values from the source armature
    bpy.context.scene.objects.active = src
    bpy.ops.object.mode_set(mode='EDIT')
    for eb in src.data.edit_bones:
        rolls[eb.name] = eb.roll
        bpy.ops.object.mode_set(mode='POSE')

    print("Writing Bone Roll to Target")

    # Place the Roll values in the target armature
    bpy.context.scene.objects.active = trg
    bpy.ops.object.mode_set(mode='EDIT')
    for eb in trg.data.edit_bones:
        oldRoll = eb.roll
        eb.roll = rolls[eb.name]
        print(eb.name, oldRoll, eb.roll)

# Setup Copy Rotation & Location Constraints
def addMocapConstraints(src, trg):
    print("Adding Location Constraints to %s with target %s" % (src.name, trg.name))

    # iterate over the pose bones
    for bone in bpy.context.selected_pose_bones:

        # Apply a Copy Rotation Constraint to each pose bone
        new_constraint = bone.constraints.new('COPY_LOCATION')

        # Set up the constraint target and set it to copy pose data
        new_constraint.target = bpy.data.objects[self.trg]
        new_constraint.subtarget = bone.name
        new_constraint.target_space = 'POSE'
        new_constraint.owner_space = 'POSE'

    # Turn off pose mode so that we can do basic operations
    bpy.ops.object.posemode_toggle()

    print("Adding Rotation Constraints to %s with target %s" % (self.constrained, self.target))

    selectAndPose(src)
    bpy.ops.pose.select_all(action='SELECT')

    # iterate over the pose bones
    for bone in bpy.context.selected_pose_bones:

        # Apply a Copy Rotation Constraint to each pose bone
        new_constraint = bone.constraints.new('COPY_ROTATION')

        # Set up the constraint target and set it to copy pose data
        new_constraint.target = bpy.data.objects[self.target]
        new_constraint.subtarget = bone.name
        new_constraint.target_space = 'POSE'
        new_constraint.owner_space = 'POSE'

class CopyBoneRotations(bpy.types.Operator):
    bl_idname = "object.copy_bone_roll"
    bl_label = "Copy Bone Roll"
    bl_options = {'REGISTER', 'UNDO'}

    # Called when operator is run
    def execute(self, context):

        # Find the source and target armatures
        trg = bpy.context.scene.objects.active
        src = None
        for ob in bpy.context.selected_objects:
            if ob.name != src.name:
                src = ob

        if src is None:
            print("No source selected")
        else:
            print("Copying Bone Rotation from %s to %s" % (src.name, trg.name))
            copyBoneRolls(src, trg)

        #Let's blender know the operator is finished
        return {'FINISHED'}

# Blender Operators
# Functions exposed via the Blender UI

class TransferMoCapData(bpy.types.Operator):
    bl_idname = "object.transfer_mocap_data"
    bl_label = "Transfer MoCap Data"
    bl_options = {'REGISTER', 'UNDO'}
    generate_constraints = bpy.props.BoolProperty(name="GenerateConstraints")
    generate_keyframes = bpy.props.BoolProperty(name="GenerateKeyframes")
    keyframe_interval = bpy.props.IntProperty(name="KeyFrameInterval", default="KeyFrameInterval")

    # Called when operator is run
    def execute(self, context):

        interv = self.keyframe_interval
        gen_kf = self.generate_keyframes
        gen_cn = self.generate_constraints

        # Find the source and target armatures
        trg = bpy.context.scene.objects.active
        src = None
        for ob in bpy.context.selected_objects:
            if ob.name != src.name:
                src = ob

        if src is None:
            print("no source selected")
        else:
            if (gen_cn):
                # Set up the Motion Capture Constraints
                addMocapConstraints(src, trg)
            if (gen_kf):
                # Transform the constraints to keyframes
                createMocapKeyframes(src, trg, interv)
                # Remove the Motion Capture Constraints
                removeMocapConstraints(src)

        # Let's blender know the operator is finished
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class CopyArmaturewithoutAnimation(bpy.types.Operator):
    bl_idname = "object.copy_armature_without_animation"
    bl_label = "Copy Armature without Animation"
    bl_options = {'REGISTER', 'UNDO'}

    # Called when operator is run
    def execute(self, context):

        # Duplicate the armature
        bpy.ops.object.duplicate_move()

        # Remove the keyframes from the armature
        bpy.ops.anim.keyframe_clear_v3d()

        # Let's blender know the operator is finished
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CopyBoneRotations)
    bpy.utils.register_class(CopyArmaturewithoutAnimation)
    bpy.utils.register_class(TransferMoCapData)

def unregister():
    bpy.utils.unregister_class(TransferMoCapData)
    bpy.utils.unregister_class(CopyArmaturewithoutAnimation)
    bpy.utils.unregister_class(CopyBoneRotations)

if __name__ == "__main__":
    register()
