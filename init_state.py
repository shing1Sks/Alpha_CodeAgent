import json
import os

STATE_FILE = "agent_state.json"

default_state = {
    "task": "Add a new page in React app",
    "status": "in_progress",
    "message": None,
    "cycle": 0,
}


def reset_state():
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(default_state, f, indent=2)
    print(f"[RESET] {STATE_FILE} initialized with default state.")


if __name__ == "__main__":
    reset_state()
