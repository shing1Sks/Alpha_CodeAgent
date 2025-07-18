from file_tools import (
    list_directory,
    read_file,
    write_file,
    read_file,
    delete_lines,
    replace_in_file,
)

# Try listing the workspace
print("📁 Directory contents:")
print(list_directory("workspace"))

# Try reading a non-existent file
print("\n📄 Read attempt:")
# Get 3 lines of context around 'console'
print(read_file("workspace/sample_project/Hello.js", keyword="console", context=3))

# Overwrite file
print(
    write_file(
        "workspace/sample_project/Hello.js", "console.log('New Content');", "overwrite"
    )
)

# Append content
print(
    write_file(
        "workspace/sample_project/Hello.js", "\nconsole.log('Appended');", "append"
    )
)

# Insert content at line 2
print(
    write_file(
        "workspace/sample_project/Hello.js",
        "console.log('Inserted');\n",
        "insert_at_line:2",
    )
)

# Verify result
print(read_file("workspace/sample_project/Hello.js"))

print(delete_lines("workspace/sample_project/Hello.js", 2, 3))

print(replace_in_file("workspace/sample_project/Hello.js", "Hello", "Hi"))
