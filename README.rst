.. figure:: https://travis-ci.org/AO-StreetArt/BlendMoCap.svg?branch=master
   :alt:

BlendMoCap by AO
================

BlendMoCap is a Blender Addon designed to allow the use of BVH data in real animations.  This project was started because of frustration with both the built in Blender Motion Capture add-on, as well as MakeWalk.

As a result of the difficulties encountered with these tools, we have made several key design decisions regarding BlendMoCap:

  - BlendMoCap is not a one-click motion capture transfer solution.  These have proven to be very difficult and time-consuming to maintain, thus often failing to meet the needs of the artist in critical situations.  They have also proven difficult to work with and extend, due to the complex algorithms needed to compensate for differences between rigs.
  - BlendMoCap is used as a set of small operators within a larger transfer workflow, which is rig-focused.  While this is more time consuming, it allows the artist the ability to tweak and fix the motion transfer at each step, ensuring that the result is production-ready.
  - BlendMoCap makes a critical assumption: that the motion capture data rig and the target rig have the same structure.  This is compensated for in the workflow, but does require re-rigging characters for use with different motion capture data sets.  In general, motion capture files taken the same way will have similar structures, and the rig for one will work for many.  However, with sufficient differences in the motion capture rigs, the target model will need to be re-rigged in order to compensate.

In a nutshell: BlendMoCap is slow and tedious, but is able to compensate for most characters and motion capture files in production scenarios.  It is easily extensible with a very simple code base.  It is supported by the AO Team, and we welcome anyone who would like to report issues to help improve the tool.

Contributing
------------

We welcome contributions, please see the Contributing.md file for instructions.
