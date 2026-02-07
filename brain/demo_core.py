#!/usr/bin/env python3
import os
import subprocess
from typing import Optional

from brain.vision_client import call_llm_action
from executor import execute_action

CAPTURE_SH = os.path.expanduser("~/robot_cmds/capture.sh")
CAPTURE_JPG = os.path.expanduser("~/captures/capture.jpg")


def capture_one() -> str:
    r = subprocess.run([CAPTURE_SH], check=False)
    if r.returncode != 0 or (not os.path.exists(CAPTURE_JPG)):
        raise RuntimeError("Capture failed. Check camera topic + capture.sh.")
    return CAPTURE_JPG


def main(user_text: Optional[str] = None) -> None:
    print("Capturing...")
    img = capture_one()
    print(f"OK: {img}")

    print("Sending to OpenAI...")
    decision = call_llm_action(img, user_text=user_text)
    print("Decision:", decision)

    action = decision.get("action", "STOP")
    dry_run = os.environ.get("DRY_RUN", "1") == "1"
    auto_exec = os.environ.get("AUTO_EXEC", "0") == "1"
    forward_cycles = int(os.environ.get("FORWARD_CYCLES", "6"))

    execute_action(action, dry_run=dry_run, auto_exec=auto_exec, forward_cycles=forward_cycles)


if __name__ == "__main__":
    main()