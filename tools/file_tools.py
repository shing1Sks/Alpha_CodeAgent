import os
import re


def list_directory(path, depth=2):
    """
    Recursively list directories and files up to a given depth.
    Returns a string tree representation.
    """
    if not os.path.exists(path):
        return f"[ERROR] Path '{path}' does not exist."

    def _walk_dir(current_path, current_depth, current_prefix):
        entries = []
        try:
            items = sorted(os.listdir(current_path))
        except PermissionError:
            return [current_prefix + "[Permission Denied]"]

        for i, entry in enumerate(items):
            full_path = os.path.join(current_path, entry)
            connector = "└── " if i == len(items) - 1 else "├── "
            line = current_prefix + connector + entry

            if os.path.isdir(full_path) and current_depth < depth:
                sub_prefix = current_prefix + (
                    "    " if i == len(items) - 1 else "│   "
                )
                sub_entries = _walk_dir(full_path, current_depth + 1, sub_prefix)
                entries.append(line)
                entries.extend(sub_entries)
            else:
                entries.append(line)
        return entries

    tree = [path]
    tree.extend(_walk_dir(path, 1, ""))
    return "\n".join(tree)


def read_file(filepath, lines=None, keyword=None, context=2):
    """
    Read full file, specific lines, or keyword matches with context.

    Args:
        filepath (str): File path.
        lines (tuple): (start, end) lines (1-based, inclusive).
        keyword (str): Keyword to search for.
        context (int): Number of lines before/after keyword for context.
    """
    if not os.path.exists(filepath):
        return f"[ERROR] File '{filepath}' not found."

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.readlines()

    # Case 1: Specific line range
    if lines:
        start, end = lines
        return "".join(content[start - 1 : end])

    # Case 2: Keyword search with context (merged)
    if keyword:
        keyword_lower = keyword.lower()
        matches = []
        covered_until = -1  # Track the last line we've already added

        for idx, line in enumerate(content):
            if keyword_lower in line.lower():
                start = max(0, idx - context)
                end = min(len(content), idx + context + 1)

                # Skip if this match is within already covered range
                if start <= covered_until:
                    continue

                covered_until = end  # Update the last covered line
                snippet = "".join(content[start:end])
                matches.append(
                    f"--- Context (lines {start + 1}-{end}) ---\n{snippet.strip()}\n"
                )

        return "\n".join(matches) if matches else f"[No matches for '{keyword}']"

    # Case 3: Full content
    return "".join(content)


def write_file(filepath, content, mode="overwrite"):
    """
    Write or modify a file.

    Args:
        filepath (str): Target file.
        content (str): Content to write.
        mode (str): 'overwrite' | 'append' | 'insert_at_line:X'
    """
    dir_path = os.path.dirname(filepath)
    if dir_path:  # Only create directories if the path is not empty
        os.makedirs(dir_path, exist_ok=True)

    if mode == "overwrite":
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"[OVERWRITE] File '{filepath}' updated."

    elif mode == "append":
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(content)
        return f"[APPEND] Content added to '{filepath}'."

    elif mode.startswith("insert_at_line:"):
        try:
            line_num = int(mode.split(":")[1])
        except ValueError:
            return "[ERROR] Invalid line number in 'insert_at_line'."

        if not os.path.exists(filepath):
            return f"[ERROR] File '{filepath}' not found."

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if line_num < 1 or line_num > len(lines) + 1:
            return "[ERROR] Line number out of range."

        lines.insert(line_num - 1, content)
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return f"[INSERT] Content inserted at line {line_num} in '{filepath}'."

    else:
        return f"[ERROR] Invalid mode '{mode}'."


def delete_lines(filepath, start, end):
    """
    Delete lines in a file from 'start' to 'end' (1-based indices).
    """
    import os

    if not os.path.exists(filepath):
        return f"[ERROR] File '{filepath}' not found."

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if start < 1 or end > len(lines) or start > end:
        return "[ERROR] Invalid line range."

    del lines[start - 1 : end]

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return f"[DELETE] Lines {start}-{end} removed from '{filepath}'."


def normalize_path(filepath):
    """
    Ensure file operations are always inside 'workspace'.
    """
    if not filepath.startswith("workspace"):
        filepath = os.path.join("workspace", filepath.lstrip("/"))
    return filepath


def make_directory(path):
    """
    Creates a directory (recursively).
    """
    path = normalize_path(path)
    if os.path.exists(path):
        return f"[MKDIR] Directory '{path}' already exists."

    os.makedirs(path, exist_ok=True)
    return f"[MKDIR] Directory '{path}' created."
