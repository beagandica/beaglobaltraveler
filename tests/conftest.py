"""Browser fixtures for the static travel website."""

from collections.abc import Iterator
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlparse

import pytest
from playwright.sync_api import Browser, Page, Route, sync_playwright

DOCS = Path(__file__).resolve().parents[1] / "docs"
LEAFLET = "https://unpkg.com/leaflet@1.9.4/dist/"
TILE = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256">'
    '<rect width="256" height="256" fill="#eee"/></svg>'
)


@pytest.fixture(scope="session")
def website_url() -> Iterator[str]:
    """Serve the real static files on an ephemeral local port.

    Args:
        None.
    Returns:
        An iterator yielding the site's base URL.
    """
    handler = partial(SimpleHTTPRequestHandler, directory=str(DOCS))
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_port}/"
        finally:
            server.shutdown()
            thread.join()


@pytest.fixture(scope="session")
def browser() -> Iterator[Browser]:
    """Launch one Chromium process for the regression suite.

    Args:
        None.
    Returns:
        An iterator yielding the browser.
    """
    with sync_playwright() as playwright:
        browser_instance = playwright.chromium.launch()
        yield browser_instance
        browser_instance.close()


@pytest.fixture(scope="session")
def leaflet_assets(browser: Browser) -> dict[str, bytes]:
    """Fetch the pinned Leaflet assets once, never real map tiles.

    Args:
        browser: The session browser.
    Returns:
        JavaScript and CSS responses indexed by URL.
    """
    with browser.new_context() as context:
        assets = {}
        for name in ("leaflet.js", "leaflet.css"):
            url = f"{LEAFLET}{name}"
            response = context.request.get(url)
            assert response.ok, f"Cannot load test dependency: {url}"
            assets[url] = response.body()
        return assets


def _route_request(route: Route, assets: dict[str, bytes]) -> None:
    url = route.request.url
    if url in assets:
        content_type = "text/css" if url.endswith(".css") else "text/javascript"
        route.fulfill(body=assets[url], content_type=content_type)
    elif urlparse(url).hostname == "tile.openstreetmap.org":
        route.fulfill(body=TILE, content_type="image/svg+xml")
    elif urlparse(url).hostname == "127.0.0.1":
        route.continue_()
    else:
        route.fulfill(status=204)


@pytest.fixture
def page(browser: Browser, leaflet_assets: dict[str, bytes]) -> Iterator[Page]:
    """Create an isolated page with tile and analytics traffic intercepted.

    Args:
        browser: The session browser.
        leaflet_assets: Cached Leaflet responses.
    Returns:
        An iterator yielding a page with no production tile requests.
    """
    with browser.new_context(viewport={"width": 1440, "height": 1000}) as context:
        context.route("**/*", lambda route: _route_request(route, leaflet_assets))
        yield context.new_page()
