// map_functions.js

var map; // Declare the map variable globally
var drawnItems = new L.FeatureGroup();

function initializeMap() {
    // Initialize the map with a default view
    map = L.map('map').setView([51.505, -0.09], 13); // Use appropriate coordinates

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);

    // Add the drawn items layer to the map
    map.addLayer(drawnItems);

    // Initialize the Draw plugin
    new L.Control.Draw({
        edit: {
            featureGroup: drawnItems
        }
    }).addTo(map);

    // Event listener for when a shape is drawn
    map.on('draw:created', function (event) {
        var layer = event.layer;
        drawnItems.addLayer(layer);
    });

    console.log("Map initialized");
}

// Function to get drawn features as GeoJSON
function getDrawnFeatures() {
    return drawnItems.toGeoJSON();
}

// Function to save drawn features
function saveDrawings() {
    var geojsonData = getDrawnFeatures();
    pyqt_save_drawings(JSON.stringify(geojsonData)); // Call the Python method to save
}

// Connect the saveDrawings function to Python
window.pyqt_save_drawings = function(data) {
    console.log("Data to save:", data); // Debugging
    
    console.log("Drawings saved");
};