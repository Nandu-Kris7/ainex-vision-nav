# Demo Procedure (Lab Checklist)

This demo shows the complete pipeline:
**camera → AI decision → action selection → robot execution**.

## Pre-flight

- Robot on a flat surface with decent traction
- Robot battery sufficient
- Emergency stop ready (stop script and physical access)

---

## 1) Start ROS / robot stack (robot side)

If your robot uses a systemd service:

sudo systemctl restart start_app_node.service

## 2) Verify ROS connection

echo $ROS_MASTER_URI
rosnode list | head

Expected:
ROS_MASTER_URI is <"<http://localhost:11311">> (when SSH'd into the robot)
rosnode list returns nodes (not an error)

## 3) Verify camera publishing

rostopic hz /camera/image_raw -w 2

Expected:
a non-zero rate (e.g., ~20–30 Hz)

## 4) Capture a test frame

./robot_cmds/capture.sh
ls -lh ~/captures/capture.jpg

Expected:
capture script prints OK
capture.jpg exists and has non-zero size

## 5) Dry-run decision test (no motion)

DRY_RUN=1 python3 brain/demo_loop.py

Expected:
repeatedly prints decisions (MOVE / STOP / ASK_USER)
no robot movement

## 6) Junction test (ASK_USER)

DRY_RUN=1 python3 brain/demo_loop.py

Expected:
decision becomes:
{"action":"ASK_USER","question":"Left or right?"}
user enters answer
model returns TURN_LEFT_90 or TURN_RIGHT_90

## 7) Live execution test (motion enabled)

DRY_RUN=0 python3 brain/demo_loop.py

Expected:
terminal prompts you before motion
robot executes short safe motions

## 8) Stop / abort

./robot_cmds/stop.sh
