"""Regression coverage for maps and expandable destination lists."""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

DOCS = Path(__file__).resolve().parents[1] / "docs"
MAP_PAGES = ["index.html", *sorted(path.name for path in DOCS.glob("*-guide.html"))]


def _region_label(countries: int, territories: int) -> str:
    label = f"{countries} countries"
    if territories:
        label += f" + {territories} {'territory' if territories == 1 else 'territories'}"
    return label


@pytest.mark.parametrize("filename", MAP_PAGES)
def test_all_maps_use_shared_basemap(page: Page, website_url: str, filename: str) -> None:
    """Check every map's tiles, styling, attribution, pins, and JavaScript.

    Args:
        page: The isolated browser page.
        website_url: The local website URL.
        filename: A page containing a map.
    Returns:
        None.
    """
    errors: list[str] = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(f"{website_url}{filename}", wait_until="networkidle")
    assert not errors, f"{filename}: {errors}"
    expect(page.locator(".travel-basemap .leaflet-tile-loaded").first).to_be_attached()
    attribution = page.locator('.leaflet-control-attribution a[href*="openstreetmap.org"]')
    page.locator("#map").scroll_into_view_if_needed()
    expect(attribution).to_be_visible()
    expect(page.locator(".map-status")).to_be_hidden()
    assert page.locator(".leaflet-marker-icon, .leaflet-interactive").count() > 0
    sources = page.locator(".leaflet-tile").evaluate_all("(tiles) => tiles.map(t => t.src)")
    assert all(url.startswith("https://tile.openstreetmap.org/") for url in sources)
    assert page.locator(".travel-basemap").evaluate("el => getComputedStyle(el).filter") != "none"
    assert page.locator(".leaflet-marker-pane").evaluate("el => getComputedStyle(el).filter") == "none"
    assert not errors, f"{filename}: {errors}"


@pytest.mark.parametrize("recovery_event", ["tileload", "tileunload"])
def test_tile_notice_recovery(page: Page, website_url: str, recovery_event: str) -> None:
    """Keep the notice until every failed tile recovers or leaves the viewport.

    Args:
        page: The isolated browser page.
        website_url: The local website URL.
        recovery_event: A tile recovery or removal event.
    Returns:
        None.
    """
    page.goto(f"{website_url}paris-guide.html", wait_until="networkidle")
    states = page.evaluate("""eventName => {
        let tiles;
        map.eachLayer(layer => { if (layer instanceof L.TileLayer) tiles = layer; });
        const first = document.createElement('img'), second = document.createElement('img');
        const hidden = () => document.querySelector('.map-status').hidden;
        tiles.fire('tileerror', {tile: first});
        tiles.fire('tileerror', {tile: second});
        tiles.fire('tileload', {tile: document.createElement('img')});
        const states = [hidden()];
        tiles.fire(eventName, {tile: first});
        states.push(hidden());
        tiles.fire(eventName, {tile: second});
        return [...states, hidden()];
    }""", recovery_event)
    assert states == [False, False, True]


def test_region_lists_match_map_data(page: Page, website_url: str) -> None:
    """Ensure all cards list their map destinations exactly once in name order.

    Args:
        page: The isolated browser page.
        website_url: The local website URL.
    Returns:
        None.
    """
    page.goto(website_url)
    regions = page.evaluate("""travelRegions.map(r => ({
        name: r.name, countries: r.countries.length, territories: r.territories.length,
        places: getRegionPlaces(r).map(p => p[0])
            .sort((a, b) => a.localeCompare(b, 'en'))
    }))""")
    expect(page.locator(".region-card")).to_have_count(len(regions))
    for region in regions:
        card = page.locator(".region-card").filter(
            has=page.get_by_text(region["name"], exact=True)
        )
        expect(card.locator(".region-places")).to_be_hidden()
        card.locator("summary").click()
        expect(card.locator(".region-places")).to_be_visible()
        expect(card.locator(".place-name")).to_have_text(region["places"])
        label = _region_label(region["countries"], region["territories"])
        expect(card.locator(".region-count")).to_have_text(label)
        card.locator("summary").click()
        expect(card.locator(".region-places")).to_be_hidden()


def test_region_keyboard_and_long_list(page: Page, website_url: str) -> None:
    """Check keyboard toggling and access to the end of a long region list.

    Args:
        page: The isolated browser page.
        website_url: The local website URL.
    Returns:
        None.
    """
    page.goto(website_url)
    card = page.locator(".region-card").filter(has=page.get_by_text("Europe", exact=True))
    summary = card.locator("summary")
    summary.focus()
    page.keyboard.press("Enter")
    expect(card).to_have_attribute("open", "")
    page.keyboard.press("Tab")
    places = card.locator(".region-places")
    expect(places).to_be_focused()
    page.keyboard.press("End")
    expect(places.locator("li").last).to_be_in_viewport()
    summary.focus()
    page.keyboard.press("Space")
    expect(places).to_be_hidden()


@pytest.mark.parametrize("width", [320, 390, 768])
def test_region_layout_on_small_screens(page: Page, website_url: str, width: int) -> None:
    """Keep expanded cards within narrow viewports without clipped country names.

    Args:
        page: The isolated browser page.
        website_url: The local website URL.
        width: The viewport width in CSS pixels.
    Returns:
        None.
    """
    page.set_viewport_size({"width": width, "height": 844})
    page.goto(website_url)
    for card in page.locator(".region-card").all():
        card.locator("summary").click()
        expect(card.locator(".region-places")).to_be_visible()
        bounds = card.bounding_box()
        assert bounds and bounds["x"] >= 0 and bounds["x"] + bounds["width"] <= width
        assert card.evaluate("el => el.scrollWidth <= el.clientWidth")
    expect(page.locator(".region-card[open]")).to_have_count(8)


def test_tile_failure_keeps_pins_and_lists(page: Page, website_url: str) -> None:
    """Expose unavailable tiles without breaking the rest of the homepage.

    Args:
        page: The isolated browser page.
        website_url: The local website URL.
    Returns:
        None.
    """
    page.route("https://tile.openstreetmap.org/**", lambda route: route.abort())
    page.goto(website_url)
    expect(page.locator(".map-status")).to_be_visible()
    expect(page.locator(".map-status")).to_contain_text("could not load")
    assert page.locator(".leaflet-interactive").count() > 0
    card = page.locator(".region-card").filter(has=page.get_by_text("Asia", exact=True))
    card.locator("summary").click()
    expect(card.get_by_text("South Korea", exact=True)).to_be_visible()
    expect(card.get_by_text("Indonesia", exact=True)).to_be_visible()


def test_missing_leaflet_keeps_lists_and_guides(page: Page, website_url: str) -> None:
    """Keep homepage content usable when the external map library fails.

    Args:
        page: The isolated browser page.
        website_url: The local website URL.
    Returns:
        None.
    """
    page.route("**/leaflet.js", lambda route: route.abort())
    errors: list[str] = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(website_url)
    expect(page.locator("#map")).to_contain_text("The map could not load")
    card = page.locator(".region-card").first
    card.locator("summary").click()
    expect(card.locator(".region-places")).to_be_visible()
    expect(page.locator("a.city-card")).to_have_count(23)
    assert not errors


def test_live_guide_links_and_search(page: Page, website_url: str) -> None:
    """Keep all existing guide links and city filtering working.

    Args:
        page: The isolated browser page.
        website_url: The local website URL.
    Returns:
        None.
    """
    page.goto(website_url)
    links = page.locator("a.city-card").evaluate_all("(links) => links.map(a => a.getAttribute('href'))")
    assert len(links) == 23
    assert all((DOCS / link).is_file() for link in links)
    page.locator("#search").fill("Seoul")
    expect(page.locator(".city-card")).to_have_count(1)
    expect(page.locator(".city-card")).to_have_attribute("href", "seoul-guide.html")
    page.locator("#search").fill("")
    expect(page.locator(".city-card")).to_have_count(26)
