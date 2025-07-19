import json
import re
import os
from tools.file_tools import (
    list_directory,
    read_file,
    write_file,
    delete_lines,
    make_directory,
)
from llm_client import call_groq, build_prompt


def normalize_path(filepath):
    """
    Ensure file operations are always inside 'workspace'.
    """
    if not filepath.startswith("workspace"):
        filepath = os.path.join("workspace", filepath.lstrip("/"))
    return filepath


def parse_llm_response(response):
    """
    Extracts the first valid JSON object from an LLM response.
    """
    try:
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception:
        print(f"[WARN] Invalid JSON after extraction:\n{response}")
    return {"action": "end", "args": {}, "message": "Invalid JSON after extraction"}


def llm_decision(task, context):
    """
    Uses Groq LLM to decide the next tool action.
    """
    prompt = build_prompt(task, context)
    response = call_groq(prompt)
    return parse_llm_response(response)


def tool_executor(action):
    """
    Executes tool commands based on LLM action.
    """
    tool = action.get("action")
    args = action.get("args", {})

    if tool == "list_directory":
        return list_directory(args.get("path", "workspace"))

    elif tool == "read_file":
        return read_file(normalize_path(args["filepath"]))

    elif tool == "write_file":
        return write_file(
            normalize_path(args["filepath"]),
            args["content"],
            args.get("mode", "overwrite"),
        )

    elif tool == "delete_lines":
        return delete_lines(
            normalize_path(args["filepath"]), args["start"], args["end"]
        )
    elif tool == "make_directory":
        return make_directory(normalize_path(args["path"]))
    elif tool == "end":
        return "[END] Agent stopped."

    else:
        return f"[ERROR] Unknown tool: {tool}"


def run_agent(initial_task):
    """
    Simple loop to interact with LLM and execute tools.
    """
    history = []
    task = initial_task
    MAX_CYCLES = 10
    HISTORY_LIMIT = 10

    print(f"🧠 Starting task: {task}")

    for cycle in range(1, MAX_CYCLES + 1):
        context = "\n".join(history[-HISTORY_LIMIT:])
        action = llm_decision(task, context)
        print(f"[LLM ACTION]: {action}")

        if action["action"] == "end":
            print("✅ Task completed by LLM.")
            break

        result = tool_executor(action)
        print(f"[TOOL RESULT]: {result}\n")

        history.append(
            f"Action: {action} => Result: {result} + File Structure till now:\n{list_directory('workspace')}"
        )

    else:
        print("[STOP] Max cycles reached without completion.")
