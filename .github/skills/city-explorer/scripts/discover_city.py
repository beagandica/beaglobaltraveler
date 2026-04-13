"""Discover a new city and generate a reference guide.

Uses OpenTripMap API (free, requires key via OTM_API_KEY env var) to fetch
real points of interest. Falls back to a structured template if no key is set.

Usage:
    python discover_city.py --city tokyo --country japan
    python discover_city.py --city "new york" --country usa
"""
import argparse
import json
import logging
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

OTM_BASE = "https://api.opentripmap.com/0.1/en/places"


def slugify(name: str) -> str:
    """Convert a city name to a lowercase kebab-case filename slug.

    Args:
        name: City name (e.g., "New York", "São Paulo").

    Returns:
        Kebab-case slug (e.g., "new-york", "sao-paulo").
    """
    slug = name.lower().strip()
    # Replace common accented chars
    replacements = {"ã": "a", "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n", "ü": "u"}
    for old, new in replacements.items():
        slug = slug.replace(old, new)
    # Replace spaces and underscores with hyphens
    slug = slug.replace(" ", "-").replace("_", "-")
    # Remove anything that's not alphanumeric or hyphen
    slug = "".join(c for c in slug if c.isalnum() or c == "-")
    # Collapse multiple hyphens
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")


def fetch_otm_geoname(city: str, country: str, api_key: str) -> dict | None:
    """Look up a city's coordinates via OpenTripMap geoname endpoint.

    Args:
        city: City name.
        country: Country name (used as hint).
        api_key: OpenTripMap API key.

    Returns:
        Dict with lat, lon, name, country or None if not found.
    """
    try:
        url = f"{OTM_BASE}/geoname?name={urllib.parse.quote(city)}&apikey={api_key}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
            if "lat" in data:
                return data
    except Exception as e:
        logger.warning(f"Geoname lookup failed: {e}")
    return None


def fetch_otm_pois(lat: float, lon: float, api_key: str, kinds: str = "", limit: int = 20) -> list[dict]:
    """Fetch points of interest near coordinates from OpenTripMap.

    Args:
        lat: Latitude.
        lon: Longitude.
        api_key: OpenTripMap API key.
        kinds: Comma-separated POI categories (e.g., "foods", "cultural").
        limit: Max results.

    Returns:
        List of POI dicts with name, kinds, dist, xid.
    """
    try:
        params = urllib.parse.urlencode({
            "radius": 10000,
            "lon": lon,
            "lat": lat,
            "kinds": kinds,
            "limit": limit,
            "apikey": api_key,
            "format": "json",
        })
        url = f"{OTM_BASE}/radius?{params}"
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read())
            # Filter out unnamed POIs
            return [p for p in data if p.get("name", "").strip()]
    except Exception as e:
        logger.warning(f"POI fetch failed for kinds='{kinds}': {e}")
    return []


def generate_from_api(city: str, country: str, api_key: str) -> str:
    """Generate a city guide using OpenTripMap API data.

    Args:
        city: City name.
        country: Country name.
        api_key: OpenTripMap API key.

    Returns:
        Markdown content for the city guide.
    """
    geo = fetch_otm_geoname(city, country, api_key)
    if not geo:
        logger.error(f"Could not find coordinates for {city}. Falling back to template.")
        return generate_template(city, country)

    lat, lon = geo["lat"], geo["lon"]
    logger.info(f"Found {city} at ({lat}, {lon})")

    # Fetch different categories of POIs
    cultural = fetch_otm_pois(lat, lon, api_key, kinds="cultural,architecture,historic", limit=15)
    food = fetch_otm_pois(lat, lon, api_key, kinds="foods,restaurants", limit=15)
    nightlife = fetch_otm_pois(lat, lon, api_key, kinds="amusements,nightclubs,bars", limit=10)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    lines = [
        f"> ⚠️ Auto-generated guide ({now}) — not yet curated by a human. Verify recommendations before relying on them.",
        "",
        f"# {city.title()} city guide",
        "",
        "## Overview",
        "",
        f"{city.title()} ({country.title()}) — a city waiting to be explored.",
        f"This guide was auto-generated from OpenTripMap data and should be reviewed and enriched with local knowledge.",
        "",
        "**Currency**: [Add local currency]",
        "**Language tip**: [Add language tip]",
        "",
        "## Neighborhoods",
        "",
        "| Neighborhood | Vibe | Best for | Transit |",
        "|---|---|---|---|",
        "| [Add neighborhoods after research] | | | |",
        "",
        "## Food",
        "",
        "| Name | Category | Neighborhood | Budget | Description | Must-order |",
        "|---|---|---|---|---|---|",
    ]

    if food:
        for poi in food[:10]:
            name = poi.get("name", "Unknown")
            kinds = poi.get("kinds", "").split(",")[0].replace("_", " ").title()
            lines.append(f"| {name} | {kinds} | [neighborhood] | $$ | [Add description] | [Add must-order] |")
    else:
        lines.append("| [Add restaurants after research] | | | | | |")

    lines.extend([
        "",
        "## Landmarks and activities",
        "",
        "| Name | Category | Neighborhood | Budget | Time needed | Description |",
        "|---|---|---|---|---|---|",
    ])

    if cultural:
        for poi in cultural[:10]:
            name = poi.get("name", "Unknown")
            kinds = poi.get("kinds", "").split(",")[0].replace("_", " ").title()
            lines.append(f"| {name} | {kinds} | [neighborhood] | $ | 1-2 hours | [Add description] |")
    else:
        lines.append("| [Add landmarks after research] | | | | | |")

    lines.extend([
        "",
        "## Nightlife",
        "",
        "| Name | Category | Neighborhood | Budget | Description |",
        "|---|---|---|---|---|",
    ])

    if nightlife:
        for poi in nightlife[:5]:
            name = poi.get("name", "Unknown")
            kinds = poi.get("kinds", "").split(",")[0].replace("_", " ").title()
            lines.append(f"| {name} | {kinds} | [neighborhood] | $$ | [Add description] |")
    else:
        lines.append("| [Add nightlife spots after research] | | | | |")

    lines.extend([
        "",
        "## Transit tips",
        "",
        "- [Add transit card info]",
        "- [Add subway/bus details]",
        "- [Add taxi tips]",
        "- [Add recommended map app]",
        "",
        "## Useful phrases",
        "",
        "| English | Local | Romanization |",
        "|---|---|---|",
        "| Hello | [Add] | [Add] |",
        "| Thank you | [Add] | [Add] |",
        "| Delicious! | [Add] | [Add] |",
        "| How much? | [Add] | [Add] |",
        "| Cheers! | [Add] | [Add] |",
        "",
    ])

    return "\n".join(lines)


def generate_template(city: str, country: str) -> str:
    """Generate a blank city guide template (no API needed).

    Args:
        city: City name.
        country: Country name.

    Returns:
        Markdown template for the city guide.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    return f"""> ⚠️ Auto-generated guide ({now}) — not yet curated by a human. Verify recommendations before relying on them.

# {city.title()} city guide

## Overview

{city.title()} ({country.title()}) — a city waiting to be explored.
Fill in this template with real recommendations from local knowledge or travel research.

**Best time to visit**: [Add]
**Currency**: [Add]
**Language tip**: [Add]

## Neighborhoods

| Neighborhood | Vibe | Best for | Transit |
|---|---|---|---|
| [Add neighborhood] | [vibe] | [best for] | [transit] |

## Food

| Name | Category | Neighborhood | Budget | Description | Must-order |
|---|---|---|---|---|---|
| [Add restaurant] | [category] | [neighborhood] | $ | [description] | [must-order] |

## Landmarks and activities

| Name | Category | Neighborhood | Budget | Time needed | Description |
|---|---|---|---|---|---|
| [Add landmark] | [category] | [neighborhood] | $ | [time] | [description] |

## Nightlife

| Name | Category | Neighborhood | Budget | Description |
|---|---|---|---|---|
| [Add spot] | [category] | [neighborhood] | $ | [description] |

## Transit tips

- [Add transit card info]
- [Add subway/bus details]
- [Add taxi tips]
- [Add recommended map app]

## Useful phrases

| English | Local | Romanization |
|---|---|---|
| Hello | [Add] | [Add] |
| Thank you | [Add] | [Add] |
| Delicious! | [Add] | [Add] |
| How much? | [Add] | [Add] |
| Cheers! | [Add] | [Add] |
"""


def main() -> None:
    """CLI entry point for city discovery."""
    parser = argparse.ArgumentParser(description="Discover a new city and generate a reference guide")
    parser.add_argument("--city", required=True, help="City name (e.g., tokyo, 'new york')")
    parser.add_argument("--country", default="", help="Country name for context")
    parser.add_argument("--output", help="Output file path (default: references/[city-slug].md)")
    parser.add_argument("--dry-run", action="store_true", help="Print to stdout instead of saving")
    args = parser.parse_args()

    api_key = os.environ.get("OTM_API_KEY", "")
    slug = slugify(args.city)

    if not args.output:
        output_dir = Path(__file__).parent.parent / "references"
        args.output = str(output_dir / f"{slug}.md")

    # Check if file already exists
    output_path = Path(args.output)
    if output_path.exists() and not args.dry_run:
        logger.info(f"Guide already exists: {output_path}")
        logger.info("Use --dry-run to preview a regeneration, or delete the file first.")
        return

    if api_key:
        logger.info(f"🔍 Discovering {args.city} via OpenTripMap API...")
        content = generate_from_api(args.city, args.country, api_key)
    else:
        logger.info(f"📝 No OTM_API_KEY set. Generating template for {args.city}...")
        content = generate_template(args.city, args.country)

    if args.dry_run:
        sys.stdout.reconfigure(encoding="utf-8")
        print(content)
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        logger.info(f"✅ Saved to {output_path}")
        logger.info(f"   Filename slug: {slug}.md")
        logger.info("   Review and enrich with local knowledge before sharing!")


if __name__ == "__main__":
    main()
