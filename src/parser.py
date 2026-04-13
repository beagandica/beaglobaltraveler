"""Parse city reference markdown files into structured data."""
import re
from pathlib import Path

from src.models import Recommendation


def parse_table_rows(content: str, header_marker: str) -> list[dict[str, str]]:
    """Extract table rows following a specific header in markdown.

    Args:
        content: Full markdown file content.
        header_marker: The header text to find (e.g., "## Food").

    Returns:
        List of dicts with column headers as keys.
    """
    lines = content.splitlines()
    in_section = False
    headers: list[str] = []
    rows: list[dict[str, str]] = []

    for line in lines:
        if line.strip().startswith("## ") and header_marker.lower() in line.lower():
            in_section = True
            continue

        if in_section and line.strip().startswith("## "):
            break

        if not in_section:
            continue

        if line.strip().startswith("| ---") or line.strip().startswith("|---"):
            continue

        if line.strip().startswith("|") and not headers:
            headers = [h.strip() for h in line.split("|") if h.strip()]
            continue

        if line.strip().startswith("|") and headers:
            values = [v.strip() for v in line.split("|") if v.strip()]
            if len(values) >= len(headers):
                rows.append(dict(zip(headers, values)))

    return rows


def load_recommendations(city_file: Path, category: str) -> list[Recommendation]:
    """Load recommendations from a specific section of a city file.

    Args:
        city_file: Path to the city markdown reference file.
        category: Section header to parse (e.g., "Food", "Landmarks").

    Returns:
        List of Recommendation objects.
    """
    content = city_file.read_text(encoding="utf-8")
    rows = parse_table_rows(content, f"## {category}")

    recommendations: list[Recommendation] = []
    for row in rows:
        recommendations.append(Recommendation(
            name=row.get("Name", ""),
            category=row.get("Category", ""),
            neighborhood=row.get("Neighborhood", ""),
            budget=row.get("Budget", ""),
            description=row.get("Description", ""),
            must_order=row.get("Must-order", ""),
            time_needed=row.get("Time needed", ""),
        ))

    return recommendations


def load_city_name(city_file: Path) -> str:
    """Extract the city display name from the first H1 heading.

    Args:
        city_file: Path to the city markdown reference file.

    Returns:
        City name string.
    """
    content = city_file.read_text(encoding="utf-8")
    match = re.search(r"^# (.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else city_file.stem.title()


def list_available_cities(references_dir: Path) -> list[str]:
    """List all city reference files available.

    Args:
        references_dir: Path to the references directory.

    Returns:
        List of city names (lowercase, no extension).
    """
    if not references_dir.exists():
        return []
    return [f.stem for f in references_dir.glob("*.md")]
