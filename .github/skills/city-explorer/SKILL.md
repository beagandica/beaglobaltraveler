---
name: city-explorer
description: >
  Explore cities with curated recommendations for food, landmarks,
  neighborhoods, and activities. Use when someone asks about things
  to do in a city, where to eat, neighborhood guides, transit tips,
  itinerary planning, or "plan my day". Also triggers on city names
  like Seoul, Tokyo, or "what should I do today". Supports generating
  random recommendations by vibe (foodie, culture, nightlife, chill).
---

# City Explorer

## When to use

- Someone asks what to do, see, or eat in a city
- Someone wants a day-by-day itinerary
- Someone asks for neighborhood recommendations
- Someone wants a random "surprise me" recommendation
- Someone mentions a specific city name

## Boundaries

- Only recommend places that exist in the reference data files
- Do not fabricate restaurants, landmarks, or addresses
- For cities without reference data, say so and offer to help build one
- Do not provide real-time info (weather, prices, hours) as data may be outdated

## Workflow: Recommend places

1. Check if `references/[city].md` exists
2. If it does NOT exist, follow the **Discover new city** workflow first
3. Read the city reference file from `references/[city].md`
4. Identify the traveler's vibe or interest (food, culture, nightlife, chill)
5. Filter recommendations by category and neighborhood
6. Present 3-5 top picks with name, description, budget level, and transit tip
7. Include at least one local phrase related to the recommendation

## Workflow: Build itinerary

1. Check if `references/[city].md` exists
2. If it does NOT exist, follow the **Discover new city** workflow first
3. Read the city reference file from `references/[city].md`
4. Ask how many days the traveler has (if not specified)
5. Group recommendations by neighborhood to minimize transit time
6. Create a day-by-day plan with morning, afternoon, and evening blocks
7. Include meal recommendations near each activity
8. Add transit directions between stops

## Workflow: Surprise me

1. Check if any city reference files exist in `references/`
2. Run `scripts/recommend.py --city [city] --vibe [vibe]` to get a random pick
3. Read the full details from the reference file
4. Present it with enthusiasm and a "why you'll love this" note

## Workflow: Discover new city

Use this workflow when the traveler asks about a city that has no reference file yet.

1. Search `references/` to confirm no file exists for this city
2. Run `scripts/discover_city.py --city [city] --country [country]` to generate a starter guide
3. Enrich the generated template with your knowledge and `fetch` from travel sources:
   - Fill in real neighborhoods, restaurants, landmarks, nightlife, transit tips, and local phrases
   - Add budget levels, descriptions, and must-order items
4. **Automatically save** the completed guide as `references/[city-slug].md` (lowercase, kebab-case)
5. Add `> ⚠️ Auto-generated guide (YYYY-MM-DD) — verify recommendations before relying on them.` at the top
6. Proceed with the original request (recommend, itinerary, or surprise me) using the freshly saved guide
7. The next time anyone asks about this city, the reference file is already there — no regeneration needed

**Important**: Always use lowercase kebab-case for filenames (e.g., `new-york.md`, `sao-paulo.md`). The filename must match what `recommend.py` expects.

## Decision table

| User request | Workflow |
|---|---|
| "What should I eat/do/see in [city]?" (reference exists) | Recommend places |
| "What should I eat/do/see in [city]?" (no reference) | Discover new city → Recommend places |
| "Plan my day/trip in [city]" (reference exists) | Build itinerary |
| "Plan my day/trip in [city]" (no reference) | Discover new city → Build itinerary |
| "Surprise me" or "random recommendation" | Surprise me |
| "Add [city]" or "discover [city]" | Discover new city |

## References

- `references/seoul.md` — Seoul guide (curated): neighborhoods, food, landmarks, activities, transit
- `references/bucheon.md` — Bucheon guide (curated): neighborhoods, food, landmarks, activities, transit
- Additional city files follow the same format (one file per city, auto-generated files marked with ⚠️)

## Scripts

- `scripts/recommend.py --city <city> --vibe <vibe>` — picks a random recommendation filtered by city and vibe category
- `scripts/discover_city.py --city <city> --country <country>` — generates a new city guide from OpenTripMap API (if `OTM_API_KEY` is set) or a structured template. Use `--dry-run` to preview without saving.

## Assets

- `assets/itinerary-template.md` — template for day-by-day itinerary output

## Output contract

- Every recommendation includes: name, category, neighborhood, budget ($/$$/$$), one-line description, transit tip
- Itineraries are organized by day with morning/afternoon/evening blocks
- At least one local phrase per response
- Always end with Wanderly's travel sign-off
