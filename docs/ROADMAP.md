# Roadmap

## Phase 1 (current): Reliable primitives + closed-loop demo

- Stable forward/turn/stop primitives
- Reliable frame capture from ROS camera topics
- LLM/VLM returns strict JSON actions
- Continuous decision loop + user input at junctions

## Phase 2: Robust behavior

- Junction detection → ASK_USER reliably
- Safety gate + uncertainty handling
- Heading correction (micro-turn correction, then IMU-based)
- Improve stability under different floors/lighting

## Phase 3: Onboard inference

- Replace cloud inference with onboard model (quantized)
- Reduce latency + enable offline operation
- Add fallback policies (rule-based safety)
- Optimize CPU/memory for Raspberry Pi constraints
