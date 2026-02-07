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

- Ubuntu / ROS Noetic
- Robot reachable via SSH (IP example)
- Camera topic name used (/camera/image_rect_color etc.)

### Python dependency

- Install deps: python3 -m pip install --user -r requirements.txt
- Set env: source ~/.config/ainex_vision_nav/openai.env
- Run: DRY_RUN=0 python3 brain/demo_loop.py

## Troubleshooting Tips

- “No frames” → restart service: sudo systemctl restart start_app_node.service
- “Can’t communicate with master” → check ROS_MASTER_URI
- Verify camera: rostopic hz /camera/image_raw -w 2

## License

MIT — see LICENSE.
