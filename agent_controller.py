import json
from tools.file_tools import list_directory, write_file, read_file
from tools.task_tools import set_task_flag

STATE_FILE = "agent_state.json"


def load_state():
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def run_agent_cycle():
    state = load_state()
    task = state.get("task", "")
    cycle = state.get("cycle", 0) + 1

    print(f"🚀 Agent Cycle {cycle} | Task: {task}")

    # === EXAMPLE: Add new React page ===
    if "new page" in task.lower():
        pages_dir = "workspace/sample_project"
        dir_tree = list_directory(pages_dir, depth=2)
        print(f"\n📂 Directory Tree:\n{dir_tree}\n")

        # STEP 1: Create the component if it doesn't exist
        new_file = f"{pages_dir}/NewPage.jsx"
        try:
            content = read_file(new_file)
            print("[INFO] NewPage.jsx already exists.")
        except:
            write_file(
                new_file,
                "export default function NewPage() {\n    return <div>New Page</div>\n}",
                "overwrite",
            )
            print("[CREATE] NewPage.jsx created.")

            set_task_flag("continue", "Component created. Router update next.")
            state["cycle"] = cycle
            save_state(state)
            return

        # STEP 2: Update router or App.jsx (not implemented yet, placeholder)
        print("[TODO] Update App.jsx routing for NewPage.jsx")
        set_task_flag("complete", "Page setup complete.")
        state["cycle"] = cycle
        save_state(state)
    else:
        print("[ERROR] No handler for this task.")
