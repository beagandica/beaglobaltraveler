# ✈️ beaglobaltraveler

An AI-powered travel planner built with GitHub Copilot customization: custom agents, skills, and prompt files working together.

**Ask about any city.** If beaglobaltraveler knows it, you get instant curated recommendations. If not, it auto-generates a guide and caches it for next time.

## What's inside

| Layer | File | What it does |
|---|---|---|
| Project context | `.github/copilot-instructions.md` | Tells Copilot about the project |
| Agent | `.github/agents/wanderly.agent.md` | ✈️ Bea's travel guide, enthusiastic travel planner with personality |
| Skill | `.github/skills/city-explorer/` | City data, recommendation scripts, itinerary templates |
| Instructions | `.github/instructions/` | Path-specific rules for markdown and Python files |
| Prompts | `.github/prompts/` | `/plan-my-day` and `/discover-city` reusable commands |
| App | `src/` | Python CLI for exploring cities |
| Visualization | `docs/seoul-guide.html`, `docs/bali-guide.html`, ... | Interactive dark-mode travel guides with maps, cards, and itineraries |

## Quick start

```bash
git clone https://github.com/beagandica/beaglobaltraveler.git
cd beaglobaltraveler
code .
pip install -r requirements.txt
```

Open Copilot Chat, select **@wanderly** (Bea's travel guide) from the picker, and ask:
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

Or ask @wanderly: *"Tell me about Lisbon"*, it will auto-generate and cache the guide.

## Visualization

Open any guide in `docs/` (for example `docs/seoul-guide.html` or `docs/bali-guide.html`) in a browser for an interactive guide with:
- 🗺️ Map with pins for every recommendation
- 🍜 Food cards with budget filters
- 🏛️ Landmark cards with time estimates
- 🌙 Nightlife section
- 📅 2-day visual itinerary timeline
- 💬 Korean survival phrases

### Website maps and destination lists

Serve the site locally from the repository root:

```powershell
python -m http.server 8000 --directory docs --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/`.
Use an HTTP server rather than opening HTML files directly so map requests include a browser referrer.
All maps share `docs/map.js` and `docs/map.css`, using OpenStreetMap standard tiles with no API key.
Dark styling applies only to the tiles, preserving marker and control colors.
Keep visible OpenStreetMap attribution and normal browser caching.
Do not add tile prefetching or offline downloads; follow the [tile usage policy](https://operations.osmfoundation.org/policies/tiles/).
Tile availability is best-effort; a visible notice reports failed tile requests.

The homepage region cards expand by click, Enter, or Space into alphabetical destination lists.
`docs\travel-data.js` is the shared source for map pins, region lists, country and territory counts, and the homepage and About page totals.
Its grouping follows Bea's personal travel list, not a sovereign-state inventory: England and Scotland are separate entries, Aruba is in the country count, and Sint Maarten is in the territory list.
Countries and additional territories are separate arrays, so territories are not added to the country count.
Nested cities and stops are not additional country entries.
The confirmed totals are 76 countries, 6 additional territories, 82 destinations, 8 regions, and 6 continents.
When changing the data, also update the static HTML fallback text and social metadata; the count regression tests check those snapshots.

### Website regression tests

```powershell
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python -m pytest tests -q
```

The suite checks every guide map, attribution, failed tiles, region list contents, keyboard access, narrow screens, and existing guide links.
It downloads the pinned Leaflet JavaScript and CSS once per run; network access to the Leaflet CDN is required.
Map tiles are mocked to avoid sending automated browsing traffic to the community tile servers.

## Built with

- [GitHub Copilot](https://github.com/features/copilot) agent mode
- Python 3.12+ / Pydantic
- [Leaflet.js](https://leafletjs.com/) for maps
- [OpenTripMap API](https://opentripmap.io/) for city discovery (optional)
