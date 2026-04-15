# ✈️ Wanderly Travel Planner

An AI-powered travel planner built with GitHub Copilot customization: custom agents, skills, and prompt files working together.

**Ask about any city.** If Wanderly knows it, you get instant curated recommendations. If not, it auto-generates a guide and caches it for next time.

## What's inside

| Layer | File | What it does |
|---|---|---|
| Project context | `.github/copilot-instructions.md` | Tells Copilot about the project |
| Agent | `.github/agents/wanderly.agent.md` | ✈️ Wanderly, enthusiastic travel planner with personality |
| Skill | `.github/skills/city-explorer/` | City data, recommendation scripts, itinerary templates |
| Instructions | `.github/instructions/` | Path-specific rules for markdown and Python files |
| Prompts | `.github/prompts/` | `/plan-my-day` and `/discover-city` reusable commands |
| App | `src/` | Python CLI for exploring cities |
| Visualization | `docs/seoul-guide.html` | Interactive dark-mode travel guide with map, cards, and timeline |

## Quick start

```bash
git clone https://github.com/beagandica/wanderly-travel.git
cd wanderly-travel
code .
pip install -r requirements.txt
```

Open Copilot Chat, select **Wanderly** from the `@` picker, and ask:
- *"What should I eat in Seoul?"*
- *"Plan a 2-day trip to Bucheon"*
- *"Discover Tokyo for me"*

Or use the commands:
- `/plan-my-day`: generate a day itinerary
- `/discover-city`: build a guide for a new city

## CLI

```bash
python -m src.main explore seoul --vibe food --count 3
python -m src.main explore bucheon --vibe culture
python -m src.main cities
```

## Adding a city

Just create one markdown file at `.github/skills/city-explorer/references/[city].md` following the same format as `seoul.md`. No code changes needed.

Or ask Wanderly: *"Tell me about Lisbon"*, it will auto-generate and cache the guide.

## Visualization

Open `docs/seoul-guide.html` in a browser for an interactive guide with:
- 🗺️ Map with pins for every recommendation
- 🍜 Food cards with budget filters
- 🏛️ Landmark cards with time estimates
- 🌙 Nightlife section
- 📅 2-day visual itinerary timeline
- 💬 Korean survival phrases

## Built with

- [GitHub Copilot](https://github.com/features/copilot) agent mode
- Python 3.12+ / Pydantic
- [Leaflet.js](https://leafletjs.com/) for maps
- [OpenTripMap API](https://opentripmap.io/) for city discovery (optional)
