import os
import subprocess
from typing import Dict, Optional

DEFAULT_ACTION_SCRIPTS = {
    "STOP": "~/robot_cmds/stop.sh",
    "TURN_LEFT_90": "~/robot_cmds/turn_left_90.sh",
    "TURN_RIGHT_90": "~/robot_cmds/turn_right_90.sh",
    "MOVE_FORWARD_SHORT": "~/robot_cmds/forward_short.sh",
}


def _expand(path: str) -> str:
    return os.path.expanduser(path)


def run_script(path: str, args: Optional[list] = None) -> int:
    cmd = [_expand(path)]
    if args:
        cmd += args
    r = subprocess.run(cmd, check=False)
    return int(r.returncode)


def execute_action(
    action: str,
    scripts: Dict[str, str] = DEFAULT_ACTION_SCRIPTS,
    dry_run: bool = True,
    auto_exec: bool = False,
    forward_cycles: int = 6,
) -> None:
    """
    Executes one action using robot_cmds scripts.
    - dry_run: if True, prints only.
    - auto_exec: if False, asks confirmation for non-STOP actions.
    """
    if action not in scripts:
        print(f"[executor] Unknown action '{action}', falling back to STOP")
        action = "STOP"

    if dry_run:
        print(f"[DRY_RUN] would execute: {action}")
        return

    if (not auto_exec) and action != "STOP":
        ans = input(f"Execute {action}? [y/N/q] ").strip().lower()
        if ans == "q":
            raise KeyboardInterrupt()
        if ans != "y":
            print("[executor] Skipped.")
            return

    script = scripts[action]
    if action == "MOVE_FORWARD_SHORT":
        rc = run_script(script, args=[str(forward_cycles)])
    else:
        rc = run_script(script)

    if rc != 0:
        print(f"[executor] WARN: script returned non-zero ({rc}) for action {action}")