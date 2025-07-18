from file_tools import list_directory, read_file

# Try listing the workspace
print("📁 Directory contents:")
print(list_directory("workspace"))

# Try reading a non-existent file
print("\n📄 Read attempt:")
# Get 3 lines of context around 'console'
print(read_file("workspace/sample_project/Hello.js", keyword="console", context=3))
