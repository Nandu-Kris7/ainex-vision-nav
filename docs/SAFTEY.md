# Safety

- Start in DRY_RUN mode (no motion).
- Use STOP as the default fallback.
- Keep the robot on a flat surface with good traction.
- Keep a hand near the robot during early motion tests.
- If camera capture fails: STOP and retry.
- If ROS master cannot be reached: do not attempt motion.
- If the robot becomes unstable, stop immediately and re-check walking parameters.
