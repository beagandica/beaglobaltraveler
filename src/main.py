"""CLI entry point for the Travel Planner."""
import argparse
import logging
import random
from pathlib import Path

from src.parser import load_recommendations, list_available_cities, load_city_name

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

REFERENCES_DIR = Path(__file__).parent.parent / ".github" / "skills" / "city-explorer" / "references"

VIBE_CATEGORIES = {
    "food": ["Street food", "Korean BBQ", "Korean traditional", "Noodles",
             "Cafe", "Seafood", "Fine dining", "Breakfast", "Cafe/themed"],
    "culture": ["Culture", "Museum", "Architecture", "Nature/Culture"],
    "nightlife": ["Clubs/bars", "Bars", "Street tents", "Club", "Wine"],
    "chill": ["Walk", "Scenic", "Views", "Cafe", "Nature/Culture"],
}


def cmd_explore(args: argparse.Namespace) -> None:
    """Show recommendations for a city, optionally filtered by vibe.

    Args:
        args: Parsed CLI arguments with city, vibe, and count.
    """
    city_file = REFERENCES_DIR / f"{args.city.lower()}.md"
    if not city_file.exists():
        logger.error(f"No guide found for '{args.city}'. Available: {', '.join(list_available_cities(REFERENCES_DIR))}")
        return

    city_name = load_city_name(city_file)
    logger.info(f"\n✈️  Exploring {city_name}\n")

    sections = ["Food", "Landmarks and activities", "Nightlife"]
    all_recs = []
    for section in sections:
        all_recs.extend(load_recommendations(city_file, section))

    if args.vibe and args.vibe in VIBE_CATEGORIES:
        targets = VIBE_CATEGORIES[args.vibe]
        all_recs = [r for r in all_recs if r.category in targets]

    if not all_recs:
        logger.info(f"No recommendations found for vibe '{args.vibe}'.")
        return

    picks = random.sample(all_recs, min(args.count, len(all_recs)))
    for rec in picks:
        logger.info(f"  📍 {rec.name}")
        logger.info(f"     {rec.category} · {rec.neighborhood} · {rec.budget}")
        if rec.description:
            logger.info(f"     {rec.description}")
        logger.info("")

    logger.info("Happy wandering! ✈️\n")


def cmd_cities(args: argparse.Namespace) -> None:
    """List all available city guides.

    Args:
        args: Parsed CLI arguments (unused).
    """
    cities = list_available_cities(REFERENCES_DIR)
    if not cities:
        logger.info("No city guides found. Add markdown files to the references directory.")
        return

    logger.info("\n🌍 Available cities:\n")
    for city in sorted(cities):
        logger.info(f"  • {city.title()}")
    logger.info("")


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="✈️ Travel Planner: explore cities with curated recommendations"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    explore_parser = subparsers.add_parser("explore", help="Get recommendations for a city")
    explore_parser.add_argument("city", help="City name (e.g., seoul)")
    explore_parser.add_argument("--vibe", choices=["food", "culture", "nightlife", "chill"],
                                help="Filter by vibe")
    explore_parser.add_argument("--count", type=int, default=5, help="Number of picks")
    explore_parser.set_defaults(func=cmd_explore)

    cities_parser = subparsers.add_parser("cities", help="List available city guides")
    cities_parser.set_defaults(func=cmd_cities)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
