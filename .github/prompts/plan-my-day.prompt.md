---
name: plan-my-day
description: Generate a personalized day itinerary for any city using Wanderly
agent: wanderly
tools:
  - read
  - edit
  - search
  - execute
---

Plan a day in ${input:city:City name, e.g., Seoul} for a traveler who wants a ${input:vibe:Vibe, foodie, culture, nightlife, or chill} experience.

## Steps

1. Read the city reference data from `.github/skills/city-explorer/references/${input:city}.md`
2. Run `python .github/skills/city-explorer/scripts/recommend.py --city ${input:city} --vibe ${input:vibe} --count 5` to get initial picks
3. Read the itinerary template from `.github/skills/city-explorer/assets/itinerary-template.md`
4. Build a single-day itinerary with morning, afternoon, and evening blocks
5. Group activities by neighborhood to minimize transit time
6. Include a meal recommendation near each activity
7. Add transit directions between each stop
8. Include at least one local phrase with translation
9. Save the itinerary to `docs/${input:city}-day-plan.md`
10. Deliver the plan in Wanderly's enthusiastic voice with the travel sign-off
