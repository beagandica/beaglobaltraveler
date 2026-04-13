"""Pick a random travel recommendation from a city reference file."""
import sys
import random
import re
import argparse
from pathlib import Path


def load_recommendations(city_file: Path, vibe: str | None = None) -> list[dict]:
    """Load recommendations from a city markdown file.

    Args:
        city_file: Path to the city reference markdown file.
        vibe: Optional filter — food, culture, nightlife, or chill.

    Returns:
        List of recommendation dicts with name, category, neighborhood,
        budget, and description.
    """
    if not city_file.exists():
        print(f"Error: City file not found: {city_file}")
        sys.exit(1)

    content = city_file.read_text(encoding="utf-8")
    recommendations: list[dict] = []

    # Match table rows with at least 4 pipe-separated columns
    for line in content.splitlines():
        if not re.match(r"^\|.+\|.+\|.+\|.+\|", line):
            continue
        if line.strip().startswith("| ---") or line.strip().startswith("|---"):
            continue
        if line.strip().startswith("| Name") or line.strip().startswith("| #"):
            continue
        if line.strip().startswith("| English"):
            continue
        if line.strip().startswith("| Neighborhood"):
            continue

        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 4:
            recommendations.append({
                "name": parts[0],
                "category": parts[1],
                "neighborhood": parts[2],
                "budget": parts[3],
                "description": parts[4] if len(parts) > 4 else "",
            })

    # Filter by vibe if specified
    vibe_map = {
        "food": ["Street food", "Korean BBQ", "Korean traditional", "Noodles",
                 "Cafe", "Seafood", "Fine dining", "Breakfast", "Cafe/themed"],
        "culture": ["Culture", "Museum", "Architecture", "Nature/Culture"],
        "nightlife": ["Clubs/bars", "Bars", "Street tents", "Club", "Wine"],
        "chill": ["Walk", "Scenic", "Views", "Cafe", "Nature/Culture"],
    }

    if vibe and vibe.lower() in vibe_map:
        target_categories = vibe_map[vibe.lower()]
        recommendations = [
            r for r in recommendations
            if r["category"] in target_categories
        ]

    return recommendations


def main() -> None:
    """CLI entry point for random recommendation picker."""
    parser = argparse.ArgumentParser(description="Pick a random travel recommendation")
    parser.add_argument("--city", required=True, help="City name (matches reference filename)")
    parser.add_argument("--vibe", choices=["food", "culture", "nightlife", "chill"],
                        help="Filter by vibe category")
    parser.add_argument("--count", type=int, default=1, help="Number of recommendations")
    args = parser.parse_args()

    # Resolve city file path relative to the script location
    script_dir = Path(__file__).parent.parent
    city_file = script_dir / "references" / f"{args.city.lower()}.md"

    recommendations = load_recommendations(city_file, args.vibe)

    if not recommendations:
        print(f"No recommendations found for {args.city}"
              + (f" with vibe '{args.vibe}'" if args.vibe else ""))
        sys.exit(1)

    picks = random.sample(recommendations, min(args.count, len(recommendations)))

    for pick in picks:
        print()
        print(f"  📍 {pick['name']}")
        print(f"     Category: {pick['category']}")
        print(f"     Neighborhood: {pick['neighborhood']}")
        print(f"     Budget: {pick['budget']}")
        if pick["description"]:
            print(f"     {pick['description']}")
    print()


if __name__ == "__main__":
    main()
