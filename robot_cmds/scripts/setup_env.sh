#!/usr/bin/env bash
set -euo pipefail

echo "[setup_env] Starting..."

# ---------- 0) Basic sanity ----------
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found."
  exit 1
fi

# ---------- 1) ROS environment ----------
# Source ROS if it exists (Noetic typical)
if [ -f /opt/ros/noetic/setup.bash ]; then
  # shellcheck disable=SC1091
  source /opt/ros/noetic/setup.bash
  echo "[setup_env] Sourced /opt/ros/noetic/setup.bash"
else
  echo "WARN: /opt/ros/noetic/setup.bash not found. ROS tools may not work."
fi

# Source your workspace if it exists
if [ -f "$HOME/ros_ws/devel/setup.bash" ]; then
  # shellcheck disable=SC1091
  source "$HOME/ros_ws/devel/setup.bash"
  echo "[setup_env] Sourced ~/ros_ws/devel/setup.bash"
else
  echo "WARN: ~/ros_ws/devel/setup.bash not found (ok if you don't use a workspace)."
fi

# ---------- 2) Ensure ~/.local/bin is on PATH ----------
# (You hit this earlier with user installs)
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  export PATH="$HOME/.local/bin:$PATH"
  echo "[setup_env] Added ~/.local/bin to PATH for this shell"
fi

# ---------- 3) Repo root detection ----------
# Expect this script is run from repo or anywhere; find repo root by going up from this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "[setup_env] Repo root: $REPO_ROOT"

# ---------- 4) Python deps strategy ----------
# We support a "vendor deps" folder like you used: ~/robot_cmds/pydeps
# If your repo uses a different folder, adjust PYDEPS_DIR below.
PYDEPS_DIR="$HOME/robot_cmds/pydeps"
mkdir -p "$PYDEPS_DIR"

# Make PY deps available to Python without venv
export PYDEPS="$PYDEPS_DIR"
export PYTHONPATH="$PYDEPS:${PYTHONPATH:-}"
echo "[setup_env] PYTHONPATH includes: $PYDEPS"

# Install python deps into PYDEPS (no venv)
# This avoids messing with system site-packages and keeps it reproducible.
REQ_FILE="$REPO_ROOT/requirements.txt"
if [ -f "$REQ_FILE" ]; then
  echo "[setup_env] Installing Python deps into $PYDEPS_DIR from requirements.txt"
  python3 -m pip install --upgrade pip >/dev/null 2>&1 || true
  python3 -m pip install --target "$PYDEPS_DIR" -r "$REQ_FILE"
else
  echo "WARN: requirements.txt not found at $REQ_FILE (skipping pip install)."
fi

# ---------- 5) OpenAI key loading (safe) ----------
# You used configs/env.example — we’ll load a local env file if present.
# Create one at: ~/.config/ainex_vision_nav/openai.env (or adjust)
ENV_DIR="$HOME/.config/ainex_vision_nav"
ENV_FILE="$ENV_DIR/openai.env"
mkdir -p "$ENV_DIR"

if [ -f "$ENV_FILE" ]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  echo "[setup_env] Loaded OpenAI env from $ENV_FILE"
else
  echo "WARN: No OpenAI env file found at $ENV_FILE"
  echo "      Create it like:"
  echo "      mkdir -p $ENV_DIR"
  echo "      echo 'export OPENAI_API_KEY=\"YOUR_KEY\"' > $ENV_FILE"
fi

# ---------- 6) ROS network defaults ----------
# If you're controlling ON the robot, localhost master is fine.
# If you're controlling FROM a PC, you usually set ROS_MASTER_URI on the PC side.
# So here we only set it if it's unset.
if [ -z "${ROS_MASTER_URI:-}" ]; then
  export ROS_MASTER_URI="http://localhost:11311"
  echo "[setup_env] ROS_MASTER_URI defaulted to $ROS_MASTER_URI"
else
  echo "[setup_env] ROS_MASTER_URI already set: $ROS_MASTER_URI"
fi

# ROS_IP can help if ROS complains about networking; keep optional
if [ -z "${ROS_IP:-}" ] && command -v hostname >/dev/null 2>&1; then
  # Try to get primary IP quickly (best effort)
  IP_GUESS="$(hostname -I 2>/dev/null | awk '{print $1}' || true)"
  if [ -n "$IP_GUESS" ]; then
    export ROS_IP="$IP_GUESS"
    echo "[setup_env] ROS_IP guessed as $ROS_IP"
  fi
fi

# ---------- 7) Quick checks ----------
echo "[setup_env] Quick checks:"
python3 - <<'PY' || true
import sys
print("  python:", sys.version.split()[0])
PY

python3 - <<'PY' || true
import os
k = os.environ.get("OPENAI_API_KEY")
print("  OPENAI_API_KEY:", ("set" if k else "NOT set"))
PY

if command -v rostopic >/dev/null 2>&1; then
  echo "  rostopic: OK"
else
  echo "  rostopic: NOT found (ROS not sourced?)"
fi

echo "[setup_env] Done."
echo "Tip: run this in your shell with:"
echo "  source scripts/setup_env.sh"