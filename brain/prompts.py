from typing import List

ALLOWED_ACTIONS: List[str] = [
    "MOVE_FORWARD_SHORT",
    "TURN_LEFT_90",
    "TURN_RIGHT_90",
    "STOP",
    "ASK_USER",
]

NAV_PROMPT = """You are the robot's safety-first navigator.

You will receive ONE camera image from a humanoid robot in an indoor hallway-like environment.

Output ONLY valid JSON (no extra text), exactly one of:
{"action":"MOVE_FORWARD_SHORT"}
{"action":"TURN_LEFT_90"}
{"action":"TURN_RIGHT_90"}
{"action":"STOP"}
{"action":"ASK_USER","question":"Left or right?"}

Rules:
- If there are 2+ reasonable path options (junction, T-intersection, open left/right), output ASK_USER with a short question listing options.
- If there is only one safe way forward, output MOVE_FORWARD_SHORT.
- If the view is unclear, risky, or you are uncertain, output STOP.
- No extra keys, no extra text.
"""