# Lab 1 walkthrough: what we built and tested

## Overview

**Lab**: Build Your Own AI Agent & Skill (4-session series)
**Theme**: Travel Planner with Wanderly ✈️ (reusable for any city)
**Date**: April 13, 2026
**Repo**: `https://github.com/beagandica/wanderly-travel`

## Session 1: Foundation (repo + copilot-instructions.md)

### What we built
- Scaffolded `copilot-lab/` repo with git init
- Created folder structure: `.github/agents/`, `.github/instructions/`, `.github/prompts/`, `.github/skills/`, `src/`, `docs/`
- Wrote `.github/copilot-instructions.md` with:
  - Project overview (Python-based Travel Planner)
  - Tech stack (Python 3.12+, Pydantic, pytest, ruff)
  - Build and run commands
  - Project structure description
  - Coding standards (type hints, pathlib, f-strings, 30-line limit)

### What we tested
- ✅ Asked Copilot *"What does this project do?"* and it answered from instructions
- ✅ Copilot correctly identified build commands and coding standards

## Session 2: Build your agent (wanderly.agent.md)

### What we built
- Created `.github/agents/wanderly.agent.md` with:
  - **Name**: Wanderly ✈️
  - **Personality**: Enthusiastic travel planner, calls user "traveler", poetic about food, storyteller for landmarks, Korean phrases sprinkled in, travel sign-offs
  - **Tools**: read, edit, search, execute (no fetch — stays grounded in reference data)
  - **Priorities**: Authentic experiences > practical details > personalization > safety
  - **Boundaries**: No booking, no made-up places, always include budget, note dietary needs

### What we tested
- ✅ Selected Wanderly from `@` picker, asked *"Introduce yourself"* — responded in character
- ✅ Agent maintained personality across interactions
- ✅ Agent refused to make up places when no reference data existed (Bucheon test before adding data)

## Session 3: Build your skill (city-explorer)

### What we built
- Created `.github/skills/city-explorer/` with full structure:
  - **SKILL.md**: Three workflows (recommend places, build itinerary, surprise me) with decision table and trigger descriptions
  - **references/seoul.md**: Comprehensive Seoul guide with 8 neighborhoods, 10 restaurants, 10 landmarks, 5 nightlife spots, transit tips, Korean phrases (all with budget levels)
  - **references/bucheon.md**: Bucheon guide with 6 neighborhoods, 8 restaurants, 8 landmarks, 4 nightlife spots (added as second city to prove extensibility)
  - **scripts/recommend.py**: Python script that picks random recommendations filtered by city and vibe (food/culture/nightlife/chill)
  - **assets/itinerary-template.md**: Day-by-day template with morning/afternoon/evening blocks

### What we tested
- ✅ Asked Wanderly *"What should I eat in Seoul?"* — pulled from reference data with budget and transit
- ✅ Used `/plan-my-day` prompt with "seoul" and "foodie" — generated full itinerary saved to `docs/`
- ✅ Script ran successfully: `python recommend.py --city seoul --vibe food --count 3`
- ✅ Wanderly correctly refused Bucheon before reference data existed (boundaries held)
- ✅ After adding `bucheon.md`, Wanderly could plan Bucheon trips (extensibility confirmed)

## Session 4: Connect the layers (instructions + prompt file)

### What we built
- **Path-specific instructions**:
  - `.github/instructions/markdown.instructions.md` (applyTo: `**/*.md`) — ATX headings, emoji conventions, travel-specific rules
  - `.github/instructions/python.instructions.md` (applyTo: `**/*.py`) — type hints, pathlib, UTF-8 encoding
- **Prompt file**:
  - `.github/prompts/plan-my-day.prompt.md` — reusable `/plan-my-day` command with city and vibe parameters, 10-step workflow, saves output to `docs/`

### What we tested
- ✅ `/plan-my-day` appeared in the `/` picker and accepted parameters
- ✅ Generated itinerary followed markdown instruction rules
- ✅ Full-stack composition: project context + agent persona + skill data + path rules all active simultaneously

## Bonus: Python application code

### What we built
- `src/models.py` — Pydantic models: Recommendation, DayBlock, DayPlan, Itinerary, City
- `src/parser.py` — Markdown table parser that reads city reference files into structured data
- `src/main.py` — CLI with two commands:
  - `python -m src.main explore seoul --vibe food` — random recommendations
  - `python -m src.main cities` — list available city guides
- `requirements.txt` — pydantic dependency

### What we tested
- ✅ CLI ran successfully for Seoul and Bucheon
- ✅ Vibe filtering worked (food, culture, nightlife, chill)
- ✅ `cities` command showed both Seoul and Bucheon

## Generated artifacts

Wanderly created these docs during testing (saved to `docs/`):
- `docs/seoul-2day-foodie-culture.md` — 2-day Seoul food and culture itinerary
- `docs/seoul-neighborhood-day-trips.md` — Seoul day trip alternatives guide

## Key takeaways

1. **Adding a city = adding one markdown file.** No code changes needed. The skill, agent, and CLI all pick it up automatically.
2. **Boundaries work.** Wanderly refused to fabricate Bucheon data before the reference file existed. The "don't make up places" rule held.
3. **Layers compose.** Project instructions + agent personality + skill knowledge + path rules all stack without conflicts.
4. **Smart discovery.** When no reference exists, Wanderly auto-generates a guide and caches it for future use.
5. **The `/plan-my-day` prompt** shows how reusable commands can wrap agent + skill into a one-click workflow.
6. **The Python app** demonstrates that the Copilot customization layer (`.github/`) wraps real application code in `src/`.

## Commit history

| Commit | Description | Files |
|---|---|---|
| `13b2c6a` | Scaffold lab structure | 2 files |
| `7ba80cc` | Complete lab: Wanderly agent, city-explorer skill, instructions, prompt | 9 files |
| `6048420` | Add travel planner Python app (models, parser, CLI) | 6 files |
| `2b2374b` | Add Bucheon city guide | 2 files |

**Total**: 19 files, ~1,300 lines of content
