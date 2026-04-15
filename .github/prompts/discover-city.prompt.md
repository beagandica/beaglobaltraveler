---
name: discover-city
description: Discover a new city and generate a reusable travel guide for Wanderly
agent: wanderly
tools:
  - read
  - edit
  - search
  - execute
  - fetch
---

Discover ${input:city:City name, e.g., Tokyo} in ${input:country:Country, e.g., Japan} and build a comprehensive travel guide.

## Steps

1. Check if `.github/skills/city-explorer/references/` already has a guide for this city
2. If it exists, say so and offer to update it instead
3. Run `python .github/skills/city-explorer/scripts/discover_city.py --city "${input:city}" --country "${input:country}" --dry-run` to generate a starter guide
4. Review the output, if it's just a template (no API key), enrich it with your knowledge:
   - Add 6-8 real neighborhoods with vibes and transit
   - Add 8-10 real restaurants with budget levels and must-order items
   - Add 8-10 real landmarks with time needed and descriptions
   - Add 4-5 nightlife spots
   - Add transit tips specific to this city
   - Add 6-8 useful local phrases with romanization
5. Use `fetch` to verify key facts from travel websites if uncertain
6. Present the completed guide to the traveler for review
7. Ask: "Want me to save this as a reusable city guide?"
8. If confirmed, save to `.github/skills/city-explorer/references/[city-slug].md`
9. Deliver with Wanderly's enthusiastic sign-off
