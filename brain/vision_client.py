import base64
import json
import os
import re
from typing import Any, Dict, Optional

from openai import OpenAI

from prompts import NAV_PROMPT, ALLOWED_ACTIONS


def _extract_first_json(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract and parse the first JSON object from model output.
    Returns None if parsing fails.
    """
    if not text:
        return None

    m = re.search(r"\{.*\}", text.strip(), re.DOTALL)
    if not m:
        return None

    try:
        obj = json.loads(m.group(0))
        if isinstance(obj, dict):
            return obj
    except Exception:
        return None
    return None


def call_llm_action(image_path: str, user_text: Optional[str] = None) -> Dict[str, Any]:
    """
    Sends image + prompt to the model and returns a dict like:
      {"action":"MOVE_FORWARD_SHORT"}
      {"action":"ASK_USER", "question":"Left or right?"}
    Always returns a safe dict (defaults to STOP).
    """
    # Ensure API key exists (OpenAI SDK uses env var OPENAI_API_KEY)
    if not os.environ.get("OPENAI_API_KEY"):
        return {"action": "STOP", "error": "OPENAI_API_KEY not set"}

    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    extra = ""
    if user_text:
        extra = (
            f"\nUser input: {user_text}\n"
            "If the user clearly chose left/right, decide TURN_LEFT_90 or TURN_RIGHT_90 accordingly.\n"
            "If unclear, choose STOP.\n"
        )

    client = OpenAI()

    resp = client.responses.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": NAV_PROMPT + extra},
                    {"type": "input_image", "image_url": f"data:image/jpeg;base64,{b64}"},
                ],
            }
        ],
        temperature=float(os.environ.get("OPENAI_TEMPERATURE", "0")),
        max_output_tokens=int(os.environ.get("OPENAI_MAX_TOKENS", "140")),
    )

    text = (resp.output_text or "").strip()
    obj = _extract_first_json(text)

    if not obj:
        return {"action": "STOP"}

    action = obj.get("action", "STOP")
    if action not in ALLOWED_ACTIONS:
        return {"action": "STOP"}

    if action == "ASK_USER":
        q = obj.get("question", "Left or right?")
        return {"action": "ASK_USER", "question": q}

    return {"action": action}