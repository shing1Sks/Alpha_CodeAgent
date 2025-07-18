import json
import os
import re

STATE_FILE = "agent_state.json"


def set_task_flag(status, message=None):
    """
    Set the task status in agent_state.json.

    Args:
        status (str): "continue" or "complete"
        message (str): Optional status message
    """
    if status not in ["continue", "complete"]:
        return "[ERROR] Invalid status. Use 'continue' or 'complete'."

    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            try:
                state = json.load(f)
            except json.JSONDecodeError:
                state = {}

    state["status"] = status
    state["message"] = message
    state["cycle"] = state.get("cycle", 0) + 1

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    return f"[TASK FLAG] Status set to '{status}'. Message: {message}"


def summarize_file(filepath):
    """
    Simple static summary of a file.
    Counts lines and detects basic functions/classes (for JS/Python).
    """
    if not os.path.exists(filepath):
        return f"[ERROR] File '{filepath}' not found."

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.readlines()

    summary = {"file": filepath, "lines": len(content), "functions": [], "classes": []}

    # Basic detection for Python or JS
    for line in content:
        if re.match(r"^\s*def\s+\w+\(", line) or re.match(
            r"^\s*function\s+\w+\(", line
        ):
            summary["functions"].append(line.strip())
        if re.match(r"^\s*class\s+\w+", line):
            summary["classes"].append(line.strip())

    return summary
