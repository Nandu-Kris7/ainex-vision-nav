# Architecture

This project is built as a layered autonomy stack on top of the Ainex robot's existing walking controller.

The key design idea is separation of responsibilities:

- **Perception + Reasoning (AI “brain”)**: decides what to do next based on the camera view and (optionally) user intent.
- **Execution (motion primitives)**: performs the chosen action using trusted ROS interfaces from the Ainex walking stack.
- **Safety defaults**: when uncertain or when inputs fail, the system chooses `STOP`.

---

## Dataflow

High-level loop:

1. **Capture** a frame from the robot camera over ROS
2. **Send** the image to the decision module (cloud model today)
3. **Receive** a strict JSON action
4. **Execute** the action as a motion primitive
5. **Repeat** until stopped

---

## ROS interfaces used (current)

### Camera

- Source topic (primary):
  - `/camera/image_raw` (type: `sensor_msgs/Image`)
- Other available topics may exist (compressed/rectified), but the current capture uses `image_raw` because it is the most reliable.

### Walking controller (Ainex stack)

- Parameter topic:
  - `/walking/set_param` (type: `ainex_interfaces/WalkingParam`)
- Command service/topic (depends on the Ainex system configuration):
  - Typical command service:
    - `/walking/command` (service: `ainex_interfaces/SetWalkingCommand` or similar)
  - Typical commands:
    - `start`, `stop`, `forward`, `turn_left`, `turn_right`

> Motion primitives should keep the low-level gait stable and only expose discrete actions to the brain.

---

## Modules in this repo

### `robot_cmds/` (execution primitives)

These scripts are intended to be **repeatable** building blocks.

Typical primitives:

- `capture.sh`: saves `~/captures/capture.jpg` from a ROS image topic
- `forward_short.sh`: moves forward for a short duration / number of cycles
- `turn_left_90.sh`: turns left approximately 90 degrees
- `turn_right_90.sh`: turns right approximately 90 degrees
- `stop.sh`: stops motion immediately

### `brain/` (decision / control loop)

- `demo_core.py`
  - Captures one frame
  - Sends to model
  - Prints the returned action (and may optionally execute)
- `demo_loop.py`
  - Repeats capture → decide → execute in a loop
  - Supports ASK_USER branching (junction case)
  - Stops with Ctrl+C or user input

---

## Decision contract (strict JSON)

To keep execution safe and predictable, the decision module must output only:

- `{"action":"MOVE_FORWARD_SHORT"}`
- `{"action":"TURN_LEFT_90"}`
- `{"action":"TURN_RIGHT_90"}`
- `{"action":"STOP"}`
- `{"action":"ASK_USER","question":"Left or right?"}`

Rules:

- If uncertain → `STOP`
- If multiple valid options → `ASK_USER`
- Only one clear safe path → `MOVE_FORWARD_SHORT`

This reduces the chance that a language model produces unsafe or ambiguous outputs.

---

## Future architecture: onboard inference

Today:

- Brain uses **cloud inference** (OpenAI API) for rapid prototyping.

Future:

- Replace API calls with an onboard model (quantized)
- Add a safety gate module that uses lightweight perception (e.g., junction detection) for fast fail-safe behavior
- Add closed-loop feedback using IMU and gait correction for drift reduction

---

## Safety and limitations

Known limitations (current prototype):

- Drift can occur due to gait asymmetry and floor friction
- No global mapping or localization (no odometry-based planning yet)
- Visual reasoning depends on lighting and camera framing

Mitigations:

- Default STOP on uncertainty
- Keep motion primitives short and repeatable
- Add micro-corrections or IMU-based correction in future iterations
