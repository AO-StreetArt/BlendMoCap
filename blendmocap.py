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

@author: AO Street Art
"""

bl_info = {
    "name": "blendmocap",
    "author": "AO Street Art",
    "version": (0, 0, 1),
    "blender": (2, 78, 0),
    "description": "Blender Add on to assist in the use of using BVH data",
    "category": "Object",
}

import bpy


# Base Functions


# Transform the mocap constraints to keyframes
def create_mocap_keyframes(src, trg, keyframe_interval):
    print("Creating Motion Capture Keyframes on %s with target %s" % (src.name, trg.name))

    select_and_pose(src)
    bpy.ops.pose.select_all(action='SELECT')

    start_frame_index = bpy.context.scene.frame_start
    end_frame_index = bpy.context.scene.frame_end

    bpy.ops.nla.bake(frame_start=start_frame_index, frame_end=end_frame_index, visual_keying=True,
                     clear_constraints=True, step=keyframe_interval,only_selected=True, bake_types={'POSE'})

# Select an object and switch to pose mode
def select_and_pose(src):
    # Deselect everything
    for ob in bpy.context.selected_objects:
        ob.select = False

    # Select the source armature
    src.select = True
    bpy.context.scene.objects.active = src

    # Set pose mode and select all the bones in the armature
    bpy.ops.object.mode_set(mode='POSE')


# Removes the mocap constraints
def remove_mocap_constraints(src):
    print("Removing Motion Capture Constraints from %s" % src.name)

    select_and_pose(src)
    bpy.ops.pose.select_all(action='SELECT')

    # iterate over the pose bones
    for bone in bpy.context.selected_pose_bones:
        for c in bone.constraints:
            if c.type == 'COPY_ROTATION' or c.type == 'COPY_LOCATION':
                bone.constraints.remove(c)


# Copy the roll values for all bones in one armature to another
def copy_bone_rolls(src, trg):
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
        old_roll = eb.roll
        if eb.name in rolls:
            eb.roll = rolls[eb.name]
        print(eb.name, old_roll, eb.roll)


# Setup Copy Rotation & Location Constraints
def add_mocap_constraints(src, trg):
    print("Adding Location Constraints to %s with target %s" % (src.name, trg.name))

    # iterate over the pose bones
    for bone in bpy.context.selected_pose_bones:

        # Apply a Copy Rotation Constraint to each pose bone
        new_constraint = bone.constraints.new('COPY_LOCATION')

        # Set up the constraint target and set it to copy pose data
        new_constraint.target = trg
        new_constraint.subtarget = bone.name
        new_constraint.target_space = 'POSE'
        new_constraint.owner_space = 'POSE'

    # Turn off pose mode so that we can do basic operations
    bpy.ops.object.posemode_toggle()

    print("Adding Rotation Constraints to %s with target %s" % (src, trg))

    select_and_pose(src)
    bpy.ops.pose.select_all(action='SELECT')

    # iterate over the pose bones
    for bone in bpy.context.selected_pose_bones:

        # Apply a Copy Rotation Constraint to each pose bone
        new_constraint = bone.constraints.new('COPY_ROTATION')

        # Set up the constraint target and set it to copy pose data
        new_constraint.target = trg
        new_constraint.subtarget = bone.name
        new_constraint.target_space = 'POSE'
        new_constraint.owner_space = 'POSE'


# Core Logic


# Copy the armature with no animation
def copy_armature_without_animation():
    # Duplicate the armature
    bpy.ops.object.duplicate_move()

    # Remove the keyframes from the armature
    bpy.ops.anim.keyframe_clear_v3d()


# Copy bone roll values from one armature to another
def copy_bone_rotations():
    # Find the source and target armatures
    trg = bpy.context.scene.objects.active
    src = None
    for ob in bpy.context.selected_objects:
        if ob.name != trg.name:
            src = ob

    if src is None:
        print("No source selected")
    else:
        print("Copying Bone Rotation from %s to %s" % (src.name, trg.name))
        copy_bone_rolls(src, trg)


# Actually transfer the motion capture data
def transfer_mocap_data(interv, gen_cn, gen_kf):
    # Find the source and target armatures
    trg = bpy.context.scene.objects.active
    src = None
    for ob in bpy.context.selected_objects:
        if ob.name != trg.name:
            src = ob

    if src is None:
        print("no source selected")
    else:
        if gen_cn or gen_kf:
            # Set up the Motion Capture Constraints
            add_mocap_constraints(trg, src)
        if gen_kf:
            # Transform the constraints to keyframes
            create_mocap_keyframes(trg, src, interv)
            # Remove the Motion Capture Constraints
            remove_mocap_constraints(trg)


# Blender Operators
# Functions exposed via the Blender UI


# Copy Bone Roll from one armature to another
class CopyBoneRotations(bpy.types.Operator):
    bl_idname = "object.copy_bone_roll"
    bl_label = "Copy Bone Roll"
    bl_options = {'REGISTER', 'UNDO'}

    # Called when operator is run
    def execute(self, context):

        copy_bone_rotations()

        # Let's blender know the operator is finished
        return {'FINISHED'}


# Actually transfer the mocap data from one rig to another
class TransferMoCapData(bpy.types.Operator):
    bl_idname = "object.transfer_mocap_data"
    bl_label = "Transfer MoCap Data"
    bl_options = {'REGISTER', 'UNDO'}
    generate_constraints = bpy.props.BoolProperty(name="GenerateConstraints")
    generate_keyframes = bpy.props.BoolProperty(name="GenerateKeyframes")
    keyframe_interval = bpy.props.IntProperty(name="KeyFrameInterval", default=1)

    # Called when operator is run
    def execute(self, context):

        transfer_mocap_data(self.keyframe_interval, self.generate_keyframes,
                            self.generate_constraints)

        # Let's blender know the operator is finished
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


# Copy the mocap armature without keeping the animations
class CopyArmaturewithoutAnimation(bpy.types.Operator):
    bl_idname = "object.copy_armature_without_animation"
    bl_label = "Copy Armature without Animation"
    bl_options = {'REGISTER', 'UNDO'}

    # Called when operator is run
    def execute(self, context):

        copy_armature_without_animation()

        # Let's blender know the operator is finished
        return {'FINISHED'}


# Register and UnRegister functions for the operators


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
