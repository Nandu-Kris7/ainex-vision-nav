# Introduction

Humanoid navigation in indoor environments requires perception, reasoning, and stable locomotion under limited compute and imperfect actuation. This work follows a layered approach: a high-level reasoning module selects actions from a small set of reliable motion primitives, while the existing walking controller provides stability and joint-level execution.

The resulting system demonstrates an end-to-end loop—camera capture on the robot, model-based action selection, and ROS-based execution—with a clear pathway toward onboard autonomy through model deployment and incremental control improvements.
