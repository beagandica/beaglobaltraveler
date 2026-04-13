# Travel Planner — Copilot instructions

## Project overview

This is a **Python-based Travel Planner** application that helps users explore cities around the world. It provides curated recommendations for food, landmarks, neighborhoods, and activities, and generates personalized day-by-day itineraries.

The project is designed to be extensible: each city is a self-contained data module, so adding a new destination means adding a new reference file, not changing code.

## Tech stack

- **Language**: Python 3.12+
- **Framework**: CLI-based (argparse), with optional FastAPI layer later
- **Storage**: Markdown reference files per city in `.github/skills/`
- **Testing**: pytest
- **Linting**: ruff (configured in pyproject.toml)

## Build and run commands

```
pip install -r requirements.txt    # Install dependencies
python src/main.py --city seoul    # Run the planner
pytest tests/ -v                   # Run all tests
ruff check src/ tests/             # Run linter
```

## Project structure

- `src/` — application source code (planner logic, CLI entry point)
- `docs/` — travel guides and contributor docs
- `tests/` — pytest test suite
- `.github/` — Copilot customization (agents, skills, instructions, prompts)

## Coding standards

- Type hints on all function signatures
- Use Pydantic models for structured data (cities, recommendations, itineraries)
- Every public function must have a docstring with Args/Returns
- Use pathlib.Path for all file operations, never os.path
- Use logging module, never print() in library code (print is OK in CLI output)
- Keep functions under 30 lines, extract helpers for complex logic
- f-strings for formatting, never .format() or %
