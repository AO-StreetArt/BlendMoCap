# BlendMoCap Design

BlendMoCap is a Blender add on designed to allow bvh data to be transferred to complex, realistic characters.  Due to the natural difficulties of working with such models, the add-on needs to be kept extremely simple and open to manual intervention.

The add-on will support the following workflows:

* Transferring bvh motions to an armature with the same core structure, with the addition of face and finger controls

The add-on will NOT support the following workflows:

* Transferring bvh motions to custom bone controls (ie. Rigify)
* Transferring bvh motions to rigs not matching the motion capture armature structure.

## Workflow Design

Users will follow the below steps in order to transfer motion capture data:

* Import BVH Data
* Select BVH Armature and 'Copy Armature without BVH Data'
* Scale & Edit the new armature to fit the target character
* Select BVH Armature, then new armature, 'Copy Bone Roll'
* Parent Target Character to Target Armature and correct vertex group weights
* Select BVH Armature, then new armature, 'Transfer MoCap Data'

Once the target character has been parented to the target armature, any desired bvh data can be transferred with the 'Transfer MoCap Data' operator, provided that:

* The bvh armatures have the same structure
* The bvh armatures have the same bone names

## Technical Design

The add-on will offer a series of operators to be used pre and post rigging, which will ensure that the process of moving the actual bvh data is handled separately from the assignment of vertex group weights.

However, because of the simplistic design, bvh files that have different core armatures will need to have the actual rigging process repeated.  The add-on only assists with copying the data to a unified armature, it will not correct differences between them.

### Pre-Rigging
Before rigging the target character, a separate rig will be created which matches the bvh rig.  For this, users
will be given a new operator 'Copy Armature without BVH Data'.  The armature will then need to be scaled to proportion
with the desired character, and taken into edit mode where the bones should be moved to match the rest position of the character.  If desired, the user may also add face and finger controls to the armature.  Then, the user will need to restore the bone rolls to that of the original armature, for which they will
be given a new operator 'Copy Bone Roll'.

At this point, the user will parent the target character to the new armature, and ensure that all vertex groups used in the parenting have the correct weights assigned.  This can be extremely time consuming, and the results should be saved separately so that it can be used repeatedly for bvh files from the same source.

### Post-Rigging
After rigging the target character, a series of constraints will be used to force the bvh actions on the target armature:

* Copy Rotation - for all bones in target armature, copying bvh armature
* Copy Location - for all hip bones in target armature, copying bvh armature

Then, we need to create a series of keyframes at specified intervals on the target armature, before removing the constraints.  All of this will be contained within a single operator, 'Transfer MoCap Data'.
