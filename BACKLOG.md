# Wanderly backlog

## Phase 1: Core content

| Item | Description | Status |
|---|---|---|
| Top 20 cities | Tokyo, Paris, London, New York, Bangkok, Dubai, Singapore, Istanbul, Barcelona, Rome, Amsterdam, Prague, Lisbon, Bali, Sydney, Mexico City, Marrakech, Kyoto, Reykjavik, Cape Town | Pending |
| City picker on HTML site | Landing page with clickable city cards (flags, names). Click to load that city's guide | Pending |
| User-submitted cities | `/suggest-city` prompt + form in HTML for users to add new destinations | Pending |
| No em dashes | Audit all files, replace em dashes. Add lint rule to markdown instructions | Pending |

## Phase 2: API integrations

| API | What it adds | Free tier | Priority |
|---|---|---|---|
| **Amadeus** (flights) | "How to get here" section with cheapest flights from user's origin | Free testing tier, pay-as-you-go in prod | High |
| **Amadeus** (hotels) | Hotel cards by budget ($, $$, $$$) in each city guide | Same key as flights | High |
| **Kiwi Tequila** | Multi-city trip routing ("Seoul + Tokyo + Bangkok in 10 days, best route?") | Free to register and test | High |
| **Ticketmaster** | "What's happening" section with upcoming concerts, shows, events per city | 5,000 free calls/day | Medium |
| **AeroDataBox** | Real-time flight status ("Is my flight on time?") | 600 free units/month | Low |
| **OpenTripMap** | Enrich auto-generated city guides with verified POI data, ratings, categories | Free with API key | Medium |

### API architecture

```
User asks about a city
        |
        v
  Reference file exists? ---yes---> Use cached data
        |
        no
        v
  discover_city.py + OpenTripMap ---> Generate base guide
        |
        v
  Amadeus API ---> Add flights + hotels
  Ticketmaster ---> Add local events
  Kiwi ---> Add routing options
        |
        v
  Save enriched guide to references/
  (cached for next time)
```

## Phase 3: UX and features

| Item | Description | Depends on |
|---|---|---|
| Multi-city trip planner | Plan trips across multiple cities with travel days between them | Kiwi API, Top 20 cities |
| Trip budget estimator | Total cost: flights + hotels + daily food/activities | Amadeus APIs |
| Smart packing list | Generate based on destination weather, trip length, activities | None |
| Audio pronunciation | "Listen" button for local phrases using browser speech synthesis | None |
| Dark/light mode toggle | Currently dark-only, add light theme option | None |
| Mobile-friendly design | Responsive layout for phone use while traveling | None |
| Shareable itinerary links | Standalone HTML itinerary, saveable as PDF | Multi-city planner |

## Phase 4: Wanderly agent upgrades

| Item | Description |
|---|---|
| Preference memory | Track user preferences (budget, food style, pace) in a file Wanderly reads |
| City comparison mode | "Compare Seoul vs Tokyo for a foodie trip" with side-by-side analysis |
| Seasonal recommendations | Best-time-to-visit data, seasonal events, date-aware suggestions |
| GitHub Pages deployment | Live site at beagandica.github.io/wanderly-travel |

## API keys needed

| Service | Sign up | Key storage |
|---|---|---|
| Amadeus | https://developers.amadeus.com | `AMADEUS_API_KEY` + `AMADEUS_API_SECRET` env vars |
| Kiwi Tequila | https://tequila.kiwi.com | `KIWI_API_KEY` env var |
| Ticketmaster | https://developer.ticketmaster.com | `TICKETMASTER_API_KEY` env var |
| AeroDataBox | https://aerodatabox.com | `AERODATABOX_API_KEY` env var |
| OpenTripMap | https://opentripmap.io | `OTM_API_KEY` env var |

All keys go in `.env` (already in `.gitignore`). Never committed to repo.
