/* Shared basemap setup for the homepage and city guides. */
function addTravelBasemap(map) {
    var failedTiles = new Set();
    var notice = L.DomUtil.create('div', 'map-status');
    notice.setAttribute('role', 'status');
    notice.hidden = true;
    notice.textContent = 'Some map tiles could not load. Pins and destination lists are still available. Try reloading the page.';

    var status = L.control({position: 'bottomleft'});
    status.onAdd = function() {
        L.DomEvent.disableClickPropagation(notice);
        L.DomEvent.disableScrollPropagation(notice);
        return notice;
    };
    status.addTo(map);

    var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19,
        className: 'travel-basemap'
    });
    tiles.on('tileerror', function(event) {
        failedTiles.add(event.tile);
        notice.hidden = false;
    });
    tiles.on('tileload tileunload', function(event) {
        failedTiles.delete(event.tile);
        notice.hidden = failedTiles.size === 0;
    });
    return tiles.addTo(map);
}
