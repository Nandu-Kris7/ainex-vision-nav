# ainex-vision-nav

Camera-guided navigation for an Ainex humanoid robot using ROS (Noetic) + onboard capture + a vision-language “brain” (currently via OpenAI API).

This project demonstrates a complete loop:
**camera → inference → discrete action → ROS motion primitive → repeat**, with optional user interaction at junctions.

Research project conducted under the supervision of **Professor Myung (Michael) Cho**.

---

## What it does (current)

- Captures a frame from the robot camera (`/camera/image_raw`)
- Sends the image to a model for a decision
- Model returns **strict JSON** with one of:
  - `MOVE_FORWARD_SHORT`
  - `TURN_LEFT_90`
  - `TURN_RIGHT_90`
  - `STOP`
  - `ASK_USER("Left or right?")`
- Executes motion using the Ainex walking stack (ROS topic/service)

---

## Why this architecture

- The AI does **high-level reasoning** only.
- Low-level gait stability remains inside the existing Ainex controller.
- Safer + faster to prototype.

---

## Repo structure

- `robot_cmds/` motion primitives + camera capture scripts
- `brain/` decision code (single-step + loop)
- `configs/` baseline params + env templates
- `docs/` architecture, safety, roadmap

---

## Setup (robot side)

### Python dependency

python3 -m pip install --user -U openai.

## Licsnse

MIT — see LICENSE.
