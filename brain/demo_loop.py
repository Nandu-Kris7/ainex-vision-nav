#!/usr/bin/env python3
import os
import subprocess
import time

from brain.vision_client import call_llm_action
from brain.executor import execute_action

CAPTURE_SH = os.path.expanduser("~/robot_cmds/capture.sh")
CAPTURE_JPG = os.path.expanduser("~/captures/capture.jpg")


def capture_one() -> str:
    r = subprocess.run([CAPTURE_SH], check=False)
    if r.returncode != 0 or (not os.path.exists(CAPTURE_JPG)):
        raise RuntimeError("Capture failed. Check camera topic + capture.sh.")
    return CAPTURE_JPG


def main() -> None:
    sleep_s = float(os.environ.get("LOOP_SLEEP", "0.5"))
    dry_run = os.environ.get("DRY_RUN", "1") == "1"
    auto_exec = os.environ.get("AUTO_EXEC", "0") == "1"
    forward_cycles = int(os.environ.get("FORWARD_CYCLES", "6"))

    print("Loop started. Ctrl+C to stop.")
    print(f"DRY_RUN={dry_run} AUTO_EXEC={auto_exec} LOOP_SLEEP={sleep_s} FORWARD_CYCLES={forward_cycles}")

    while True:
        try:
            print("\nCapturing...")
            img = capture_one()
            print("OK:", img)

            d1 = call_llm_action(img)
            print("Decision 1:", d1)

            if d1.get("action") == "ASK_USER":
                q = d1.get("question", "Left or right?")
                ans = input(f"{q} (type q to quit) ").strip()
                if ans.lower() == "q":
                    break

                d2 = call_llm_action(img, user_text=ans)
                print("Decision 2:", d2)
                execute_action(
                    d2.get("action", "STOP"),
                    dry_run=dry_run,
                    auto_exec=auto_exec,
                    forward_cycles=forward_cycles,
                )
            else:
                execute_action(
                    d1.get("action", "STOP"),
                    dry_run=dry_run,
                    auto_exec=auto_exec,
                    forward_cycles=forward_cycles,
                )

        except KeyboardInterrupt:
            print("\nStopping.")
            break
        except Exception as e:
            print("ERROR:", e)

        time.sleep(sleep_s)


if __name__ == "__main__":
    main()