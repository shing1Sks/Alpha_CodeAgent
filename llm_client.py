import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def call_groq(prompt, model="llama3-8b-8192"):
    """
    Calls the Groq API with the provided prompt and returns the raw text response.
    """
    response = groq_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()


def build_prompt(task, context=""):
    """
    Constructs a concise, example-driven prompt for the LLM.
    """

    tools_description = """
You are an autonomous coding agent with access to these tools:

TOOLS:
1. list_directory(path: str)
   - Lists files/folders in a directory.
   - Example:
     { "action": "list_directory", "args": {"path": "/workspace"}, "message": "Checking project structure." }

2. read_file(filepath: str)
   - Reads the content of a file.
   - Example:
     { "action": "read_file", "args": {"filepath": "/workspace/index.html"}, "message": "Reading HTML file." }

3. write_file(filepath: str, content: str, mode: str)
   - Creates or edits files. If the directory does not exist, call make_directory first.
   - mode: "overwrite" or "append".
   - Example:
     { "action": "write_file", "args": {"filepath": "/workspace/app.js", "content": "console.log('Hello');", "mode": "overwrite"}, "message": "Creating JS file." }

4. delete_lines(filepath: str, start: int, end: int)
   - Deletes a range of lines from a file.
   - Example:
     { "action": "delete_lines", "args": {"filepath": "/workspace/app.js", "start": 2, "end": 5}, "message": "Removing unused code." }

FINAL RULES:
- Dont try to create any directories, just directly write files to accomplish the task.
- Respond **only** with a single valid JSON object (no extra text or commentary).
- End the task with:
  { "action": "end", "args": {}, "message": "Task complete." }
"""

    return f"""
TASK: {task}

CONTEXT (Previous actions and results):
{context}

Your job:
- Think step by step.
- Use only the tools listed.
- Output a valid JSON response with one action at a time.

What is your next action?
{tools_description}
"""
