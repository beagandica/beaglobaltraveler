/* Bea's personal travel-count convention, not a sovereign-state inventory.
 * England and Scotland count separately. Territory grouping follows her list.
 * Coordinates are representative map pins, not a record of individual stops.
 */
var travelRegions = [
    {
        key: 'LATAM', name: 'Latin America', emoji: '\ud83c\udf0e', color: '#22c55e',
        countries: [
            ['Venezuela', 8, -66], ['Colombia', 4.6, -74.1],
            ['Brazil', -15.8, -47.9], ['Chile', -33.4, -70.7],
            ['Argentina', -34.6, -58.4], ['Paraguay', -25.3, -57.6],
            ['Uruguay', -34.9, -56.2], ['Panama', 9, -79.5],
            ['Costa Rica', 9.9, -84.1], ['El Salvador', 13.7, -89.2]
        ],
        territories: []
    },
    {
        key: 'Caribbean', name: 'Caribbean', emoji: '\ud83c\udfd6\ufe0f', color: '#14b8a6',
        countries: [
            ['Aruba', 12.5, -70], ['Haiti', 18.5, -72.3],
            ['Bahamas', 25, -77.4], ['Jamaica', 18.1, -77.3],
            ['Dominican Republic', 18.5, -69.9]
        ],
        territories: [
            ['Cayman Islands', 19.3, -81.4], ['US Virgin Islands', 18.3, -64.9],
            ['British Virgin Islands', 18.4, -64.6], ['Puerto Rico', 18.2, -66.5],
            ['Sint Maarten', 18, -63.1]
        ]
    },
    {
        key: 'North America', name: 'North America', emoji: '\ud83d\uddfd', color: '#3b82f6',
        countries: [
            ['United States', 39.8, -98.6], ['Canada', 56.1, -106.3],
            ['Mexico', 23.6, -102.6]
        ],
        territories: []
    },
    {
        key: 'Europe', name: 'Europe', emoji: '\ud83c\udff0', color: '#f97316',
        countries: [
            ['Germany', 51.2, 10.5], ['Austria', 47.5, 14.6],
            ['Poland', 51.9, 19.1], ['Hungary', 47.2, 19.5],
            ['Czech Republic', 49.8, 15.5], ['France', 46.6, 2.2],
            ['Portugal', 39.4, -8.2], ['Denmark', 56.3, 9.5],
            ['Netherlands', 52.1, 5.3], ['Belgium', 50.5, 4.5],
            ['Spain', 40.5, -3.7], ['Monaco', 43.7, 7.4],
            ['Switzerland', 46.8, 8.2], ['England', 51.5074, -0.1278],
            // Scotland: OpenStreetMap relation 58446; England uses the London guide pin.
            ['Scotland', 56.7861, -4.1141], ['Italy', 41.9, 12.5],
            ['Holy See (Vatican City)', 41.9, 12.45], ['Luxembourg', 49.8, 6.1],
            ['Greece', 39.1, 21.8], ['Iceland', 64.1, -21.9],
            ['Russia', 61.5, 105.3], ['Finland', 61.9, 25.7],
            ['Sweden', 60.1, 18.6], ['Estonia', 58.6, 25],
            ['Malta', 35.9, 14.4], ['Andorra', 42.5, 1.5],
            ['Liechtenstein', 47.2, 9.6], ['Croatia', 45.1, 15.2],
            ['Bosnia and Herzegovina', 43.9, 17.7], ['Norway', 60.5, 8.5],
            ['Ireland', 53.1, -8]
        ],
        territories: []
    },
    {
        key: 'Middle East', name: 'Middle East', emoji: '\ud83d\udd4c', color: '#eab308',
        countries: [
            ['Turkey', 39.9, 32.9], ['United Arab Emirates', 23.4, 53.8],
            ['Israel', 31, 34.9], ['Palestine', 31.9, 35.2],
            ['Syria', 35, 38.5], ['Qatar', 25.3, 51.2]
        ],
        territories: []
    },
    {
        key: 'Africa', name: 'Africa', emoji: '\ud83e\udd81', color: '#ef4444',
        countries: [
            ['Morocco', 31.8, -7.1], ['Seychelles', -4.7, 55.5],
            ['Kenya', 0, 37.9], ['Tanzania', -6.4, 34.9],
            ['Madagascar', -18.8, 46.9], ['Mauritius', -20.3, 57.6]
        ],
        territories: []
    },
    {
        key: 'Oceania', name: 'Oceania', emoji: '\ud83c\udfc4', color: '#60a5fa',
        countries: [
            ['Australia', -25.3, 133.8], ['New Zealand', -40.9, 174.9],
            ['Fiji', -18, 179]
        ],
        territories: [['French Polynesia', -17.7, -149.4]]
    },
    {
        key: 'Asia', name: 'Asia', emoji: '\ud83c\udfef', color: '#4ade80',
        countries: [
            ['China', 35.9, 104.2], ['India', 20.6, 79],
            ['Vietnam', 14.1, 108.3], ['Cambodia', 12.6, 104.9],
            ['Laos', 19.9, 102.5], ['Thailand', 15.9, 100.9],
            ['Malaysia', 4.2, 101.9], ['Singapore', 1.4, 103.8],
            ['Japan', 36.2, 138.3], ['Maldives', 3.2, 73.2],
            ['South Korea', 36.5, 127.8], ['Indonesia', -2.5, 118]
        ],
        territories: []
    }
];

function getRegionPlaces(region) {
    return region.countries.concat(region.territories);
}

function formatRegionCount(region) {
    var label = region.countries.length + ' countries';
    if (region.territories.length) {
        label += ' + ' + region.territories.length
            + (region.territories.length === 1 ? ' territory' : ' territories');
    }
    return label;
}

var travelTotals = {countries: 0, territories: 0, regions: travelRegions.length, continents: 6};
travelRegions.forEach(function(region) {
    travelTotals.countries += region.countries.length;
    travelTotals.territories += region.territories.length;
});
travelTotals.destinations = travelTotals.countries + travelTotals.territories;
travelTotals.countriesToGoal = 100 - travelTotals.countries;

function renderTravelCounts() {
    document.querySelectorAll('[data-travel-stat]').forEach(function(element) {
        var value = travelTotals[element.dataset.travelStat];
        element.textContent = value;
        if (element.hasAttribute('data-target')) {
            element.dataset.target = value;
        }
    });
    document.querySelectorAll('[data-travel-region]').forEach(function(element) {
        var region = travelRegions.find(function(item) {
            return item.key === element.dataset.travelRegion;
        });
        element.textContent = formatRegionCount(region);
    });
}
