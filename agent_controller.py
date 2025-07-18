import json
from tools.file_tools import list_directory, write_file, read_file
from tools.task_tools import set_task_flag
import os

STATE_FILE = "agent_state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"task": "", "status": "in_progress", "message": None, "cycle": 0}

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"task": "", "status": "in_progress", "message": None, "cycle": 0}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def add_route_to_app(app_file, component="NewPage"):
    """
    Adds a new route to App.jsx for the given component.
    """
    content = read_file(app_file)
    if "[ERROR]" in content:
        return f"[ERROR] Could not read {app_file}"

    lines = content.splitlines()

    # 1. Ensure import statement
    import_stmt = f'import {component} from "./{component}";'
    if import_stmt not in content:
        lines.insert(0, import_stmt)

    # 2. Insert <Route> into <Routes>
    route_line = f'    <Route path="/new" element={{<{component} />}} />'
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        if "<Routes>" in line and not inserted:
            new_lines.append(route_line)
            inserted = True

    new_content = "\n".join(new_lines)
    write_file(app_file, new_content, "overwrite")
    return "[UPDATE] App.jsx updated with new route."


def run_agent_cycle():
    state = load_state()
    task = state.get("task", "")
    cycle = state.get("cycle", 0) + 1

    print(f"🚀 Agent Cycle {cycle} | Task: {task}")

    if "new page" in task.lower():
        pages_dir = "workspace/sample_project"
        app_file = f"{pages_dir}/App.jsx"

        # STEP 1: Create component
        new_file = f"{pages_dir}/NewPage.jsx"
        if not os.path.exists(new_file):
            print(f"[INFO] Creating {new_file}")
            write_file(
                new_file,
                "export default function NewPage() {\n    return <div>New Page</div>\n}",
                "overwrite",
            )
            set_task_flag("continue", "Component created. Router update next.")
            state["cycle"] = cycle
            save_state(state)
            return

        # STEP 2: Update router/App.jsx
        if os.path.exists(app_file):
            print("[INFO] Updating App.jsx for routing...")
            result = add_route_to_app(app_file)
            print(result)
        else:
            print("[WARN] App.jsx not found. Skipping router update.")

        set_task_flag("complete", "Page setup complete.")
        state["cycle"] = cycle
        save_state(state)
    else:
        print("[ERROR] No handler for this task.")
