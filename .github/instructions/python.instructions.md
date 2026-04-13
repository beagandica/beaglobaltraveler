---
applyTo: "**/*.py"
---

# Python standards for travel planner

- Type hints on all function signatures, including return types
- Use pathlib.Path for all file operations, never os.path
- Use argparse for CLI argument parsing
- Docstrings on all public functions with Args/Returns sections
- Use f-strings for string formatting
- Handle file-not-found errors gracefully with helpful messages
- Keep functions under 30 lines
- Use UTF-8 encoding when reading/writing files (travel data includes non-ASCII characters)
