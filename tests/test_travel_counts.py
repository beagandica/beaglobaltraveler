"""Count and membership regressions against Bea's supplied destination list."""

import pytest
from playwright.sync_api import Page, expect

COUNTRIES = {
    "LATAM": (
        "Venezuela|Colombia|Brazil|Chile|Argentina|Paraguay|Uruguay|Panama|"
        "Costa Rica|El Salvador"
    ).split("|"),
    "Caribbean": "Aruba|Haiti|Bahamas|Jamaica|Dominican Republic".split("|"),
    "North America": ["United States", "Canada", "Mexico"],
    "Europe": (
        "Germany|Austria|Poland|Hungary|Czech Republic|France|Portugal|Denmark|"
        "Netherlands|Belgium|Spain|Monaco|Switzerland|England|Scotland|Italy|"
        "Holy See (Vatican City)|Luxembourg|Greece|Iceland|Russia|Finland|Sweden|"
        "Estonia|Malta|Andorra|Liechtenstein|Croatia|Bosnia and Herzegovina|Norway|Ireland"
    ).split("|"),
    "Middle East": ["Turkey", "United Arab Emirates", "Israel", "Palestine", "Syria", "Qatar"],
    "Africa": ["Morocco", "Seychelles", "Kenya", "Tanzania", "Madagascar", "Mauritius"],
    "Oceania": ["Australia", "New Zealand", "Fiji"],
    "Asia": (
        "China|India|Vietnam|Cambodia|Laos|Thailand|Malaysia|Singapore|Japan|"
        "Maldives|South Korea|Indonesia"
    ).split("|"),
}
TERRITORIES = {
    "Caribbean": [
        "Cayman Islands", "US Virgin Islands", "British Virgin Islands",
        "Puerto Rico", "Sint Maarten",
    ],
    "Oceania": ["French Polynesia"],
}
TOTALS = {
    "countries": 76, "territories": 6, "destinations": 82,
    "regions": 8, "continents": 6, "countriesToGoal": 24,
}


def test_destination_membership_matches_supplied_list(page: Page, website_url: str) -> None:
    """Check exact membership, uniqueness, and the personal counting convention.

    Args:
        page: The isolated browser page.
        website_url: The local website URL.
    Returns:
        None.
    """
    page.goto(website_url)
    regions = page.evaluate("travelRegions")
    assert {region["key"] for region in regions} == set(COUNTRIES)
    all_names: list[str] = []
    for region in regions:
        countries = [place[0] for place in region["countries"]]
        territories = [place[0] for place in region["territories"]]
        assert sorted(countries) == sorted(COUNTRIES[region["key"]])
        assert sorted(territories) == sorted(TERRITORIES.get(region["key"], []))
        all_names.extend(countries + territories)
    assert len(all_names) == len(set(all_names)) == 82
    assert page.evaluate("travelTotals") == TOTALS
    expect(page.locator("#map .leaflet-interactive")).to_have_count(82)


@pytest.mark.parametrize("filename", ["index.html", "about.html"])
@pytest.mark.parametrize("scripts_enabled", [True, False], ids=["rendered", "static"])
def test_page_totals_and_fallbacks(
    page: Page, website_url: str, filename: str, scripts_enabled: bool
) -> None:
    """Check visible counters and static fallback values on both pages.

    Args:
        page: The isolated browser page.
        website_url: The local website URL.
        filename: The homepage or About page.
        scripts_enabled: Whether scripts may update the HTML.
    Returns:
        None.
    """
    if not scripts_enabled:
        page.context.new_cdp_session(page).send(
            "Emulation.setScriptExecutionDisabled", {"value": True}
        )
    page.goto(f"{website_url}{filename}")
    for key, value in TOTALS.items():
        if key == "countriesToGoal" and filename == "index.html":
            continue
        elements = page.locator(f'[data-travel-stat="{key}"]')
        assert elements.count() > 0, f"Missing {key} on {filename}"
        expect(elements).to_have_text([str(value)] * elements.count())
    expect(page.locator(".counting-note")).to_contain_text("England and Scotland")


@pytest.mark.parametrize("scripts_enabled", [True, False], ids=["rendered", "static"])
def test_about_region_breakdowns(page: Page, website_url: str, scripts_enabled: bool) -> None:
    """Check About badges match the country and additional-territory breakdown.

    Args:
        page: The isolated browser page.
        website_url: The local website URL.
        scripts_enabled: Whether scripts may update the HTML.
    Returns:
        None.
    """
    if not scripts_enabled:
        page.context.new_cdp_session(page).send(
            "Emulation.setScriptExecutionDisabled", {"value": True}
        )
    page.goto(f"{website_url}about.html")
    expect(page.locator("[data-travel-region]")).to_have_count(8)
    for key, countries in COUNTRIES.items():
        label = f"{len(countries)} countries"
        territories = len(TERRITORIES.get(key, []))
        if territories:
            noun = "territory" if territories == 1 else "territories"
            label += f" + {territories} {noun}"
        expect(page.locator(f'[data-travel-region="{key}"]')).to_have_text(label)


def test_territories_are_labeled_separately(page: Page, website_url: str) -> None:
    """Ensure territories remain visible without inflating the country count.

    Args:
        page: The isolated browser page.
        website_url: The local website URL.
    Returns:
        None.
    """
    page.goto(website_url)
    expect(page.locator(".territory-label")).to_have_count(6)
    names = page.locator("li:has(.territory-label) .place-name").all_text_contents()
    assert sorted(names) == sorted(sum(TERRITORIES.values(), []))
    expect(page.locator(".place-name")).to_have_count(82)
    europe = page.locator(".region-card").filter(has=page.get_by_text("Europe", exact=True))
    europe.locator("summary").click()
    expect(europe.locator(".region-count")).to_have_text("31 countries")
    expect(europe.get_by_text("England", exact=True)).to_be_visible()
    expect(europe.get_by_text("Scotland", exact=True)).to_be_visible()
    expect(europe.get_by_text("United Kingdom", exact=True)).to_have_count(0)


def test_social_metadata_uses_confirmed_totals(page: Page, website_url: str) -> None:
    """Check the static social previews no longer claim seven continents.

    Args:
        page: The isolated browser page.
        website_url: The local website URL.
    Returns:
        None.
    """
    page.goto(website_url)
    for selector in ('meta[property="og:description"]', 'meta[name="twitter:description"]'):
        content = page.locator(selector).get_attribute("content")
        assert content and "76 countries" in content and "6 continents" in content
        assert "7 continents" not in content
    description = page.locator('meta[name="description"]').get_attribute("content")
    assert description and "76 countries" in description
    page.goto(f"{website_url}about.html")
    content = page.locator('meta[property="og:description"]').get_attribute("content")
    assert content and "76 countries" in content
