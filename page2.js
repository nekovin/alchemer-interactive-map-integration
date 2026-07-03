// ---------- inject CSS (Alchemer strips <style> from question HTML) ----------
(function () {
  const css = `
    #park-map-wrapper { color-scheme: light; font-family: Arial, sans-serif; }

    #location-search,
    #park-map-wrapper .search-box {
      width: 100%;
      max-width: 400px;
    }
    #location-search gmp-place-autocomplete { width: 100%; }

    #park-map-wrapper label {
      display: block;
      margin-bottom: 5px;
    }

    #park-map-wrapper .search-box {
      display: flex;
      align-items: center;
      box-sizing: border-box;
      height: 40px;
      padding: 0 12px;
      background: #fff;
      border: 1px solid #dfe1e5;
      border-radius: 4px;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
    }
    #park-map-wrapper .search-box:focus-within { border-color: #1a73e8; }
    #park-map-wrapper .search-box svg { flex: 0 0 auto; margin-right: 8px; }
    #park-map-wrapper .search-box input {
      flex: 1;
      height: 100%;
      border: none;
      outline: none;
      background: transparent;
      font-family: Roboto, Arial, sans-serif;
      font-size: 14px;
      color: #202124;
    }

    /* results + selected lists: tidy spacing, and collapse entirely when empty */
    #list-holder,
    #selected-holder {
      margin: 8px 0;
      padding-left: 20px;
    }
    #list-holder:empty,
    #selected-holder:empty { display: none; }
  `;
  const styleEl = document.createElement("style");
  styleEl.textContent = css;
  document.head.appendChild(styleEl);
})();

/* Alchemer JavaScript Action - park selection map (v2, debug checkpoints)
   Changes from v1:
   - removed loading=async from the Maps loader URL (can defer google.maps.Map
     past the callback in some load orders; your original working version
     didn't use it)
   - missing #map div now retries instead of silently returning
   - numbered [PARKMAP] checkpoint logs so the console shows exactly how far
     the script gets
*/

console.log("[PARKMAP 1] JS action loaded");

const finalAzureUrl = 'https://alchemer01.blob.core.windows.net/4463/parks_data/parks_data.json?sp=r&st=2026-07-01T05:48:03Z&se=2026-07-29T14:03:03Z&spr=https&sv=2026-02-06&sr=b&sig=qw578tyhKN%2FJLu60G2eBMA7nDDrVpjGrgtuHKP%2FJogo%3D';
const ALCHEMER_HIDDEN_FIELD_ID = "sgE-391014007-2-19-element"; // THIS NEEDS TO BE MAINTAINED IF SOMEBODY SCREWS W MY CODE >:(
const GOOGLE_MAPS_KEY = "AIzaSyBnhF8F278dHno51nyrbqBEQn_rELO4mQE";

// ---------- data ----------
fetch(finalAzureUrl, { method: "GET", mode: "cors" })
  .then(response => {
    if (!response.ok) throw new Error("Azure HTTP Error: " + response.status);
    return response.json();
  })
  .then(jsonData => {
    window.azureParksData = jsonData;
    console.log("[PARKMAP 2] Azure data saved,", jsonData.length, "parks");
  })
  .catch(error => {
    console.error("[PARKMAP 2-FAIL] Fetch failed:", error);
  });

// ---------- state ----------
let userSelections = [];
const parkRegistry = new Map(); // park.name -> { park, polygon, selected }
let map = null;

// ---------- Alchemer sync (runs on every change, no submit button needed) ----------
function updateAlchemerField() {
  const alchemerField = document.getElementById(ALCHEMER_HIDDEN_FIELD_ID);
  if (!alchemerField) {
    console.warn("[PARKMAP] Hidden field not found:", ALCHEMER_HIDDEN_FIELD_ID);
    return;
  }
  alchemerField.value = userSelections.join(", ");
  alchemerField.dispatchEvent(new Event("change", { bubbles: true }));
}

// ---------- selected-parks list under the map ----------
function renderSelections() {
  const selectedHolder = document.getElementById("selected-holder");
  const selectedCount = document.getElementById("selected-count");
  const selectedEmpty = document.getElementById("selected-empty");
  if (!selectedHolder) return;

  selectedHolder.innerHTML = "";
  if (selectedCount) selectedCount.textContent = userSelections.length;
  if (selectedEmpty) selectedEmpty.style.display = userSelections.length ? "none" : "";

  userSelections.forEach(name => {
    const entry = parkRegistry.get(name);
    const li = document.createElement("li");
    li.textContent = name + "  \u2715";
    li.title = "Click to remove";
    li.style.cursor = "pointer";
    li.addEventListener("click", () => setSelected(entry, false));
    selectedHolder.appendChild(li);
  });
}

// ---------- single source of truth for select / deselect ----------
function setSelected(entry, selected) {
  entry.selected = selected;
  entry.polygon.setOptions({
    fillColor: selected ? entry.park.selectedColor : entry.park.defaultColor,
    strokeColor: selected ? entry.park.selectedColor : entry.park.defaultColor
  });

  if (selected) {
    if (!userSelections.includes(entry.park.name)) {
      userSelections.push(entry.park.name);
    }
  } else {
    userSelections = userSelections.filter(item => item !== entry.park.name);
  }

  renderSelections();
  updateAlchemerField();
  console.log("Current Selections Array:", userSelections);
}

// ---------- init (called by the Maps loader, retries until data + DOM ready) ----------
window.initAlchemerMap = function () {
  if (!window.azureParksData) {
    console.log("[PARKMAP 3] Park data not ready yet, retrying...");
    setTimeout(window.initAlchemerMap, 100);
    return;
  }
  var mapLoader = document.querySelector('.loader');
  if (mapLoader) { 
    mapLoader.style.display = 'none'; 
  }
  var mapContent = document.getElementById('map-interface-content');
  if (mapContent) {
    mapContent.style.display = 'block';
  }
  const mapElement = document.getElementById("map");
  if (!mapElement) {
    // was a silent return in v1 - now retry, Alchemer may not have the
    // question HTML in the DOM yet (or it stripped the div - watch for
    // this log repeating forever)
    console.warn("[PARKMAP 4-FAIL] #map div not found, retrying...");
    setTimeout(window.initAlchemerMap, 200);
    return;
  }

  console.log("[PARKMAP 4] Data + #map div found, building map");

  const parkData = window.azureParksData;

  // Bounding box around Victoria, AU.
  const vicBounds = {
    north: -32.9, south: -40.2, east: 150.0, west: 140.9
  };

  map = new google.maps.Map(mapElement, {
    zoom: 9,
    center: { lat: -37.8080, lng: 144.9750 },
    restriction: {
      latLngBounds: vicBounds, // can't pan the map outside Victoria
      strictBounds: false
    },
    minZoom: 6 // stop zooming out past the state
  });

  console.log("[PARKMAP 5] Map object created");

  map.addListener("tilesloaded", () => {
    console.log("[PARKMAP 6] Tiles loaded - map should be visible now");
    const loader = document.getElementById("map-loader");
    if (loader) loader.style.display = "none";
  });

  // ---- park polygons ----
  parkData.forEach(park => {
    const polygonHighlight = new google.maps.Polygon({
      paths: park.coords,
      strokeColor: park.defaultColor,
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: park.defaultColor,
      fillOpacity: 0.35,
      map: map
    });

    const entry = { park: park, polygon: polygonHighlight, selected: false };
    parkRegistry.set(park.name, entry);

    google.maps.event.addListener(polygonHighlight, "click", function () {
      setSelected(entry, !entry.selected);
    });
  });

  console.log("[PARKMAP 7] Polygons drawn:", parkRegistry.size);

  // ---- location search: Google Places autocomplete moves the map ----
  google.maps.importLibrary("places").then(function (placesLib) {
    const container = document.getElementById("location-search");
    if (!container) {
      console.warn("[PARKMAP 8-FAIL] #location-search div not found");
      return;
    }

    const placeAutocomplete = new placesLib.PlaceAutocompleteElement();
    placeAutocomplete.placeholder = "Search for a street / area..";
    placeAutocomplete.includedRegionCodes = ["au"];
    placeAutocomplete.locationRestriction = vicBounds; // only suggest places in Victoria
    container.appendChild(placeAutocomplete);

    placeAutocomplete.addEventListener("gmp-select", function (event) {
      const place = event.placePrediction.toPlace();
      place.fetchFields({ fields: ["location", "viewport"] }).then(function () {
        if (place.viewport) {
          map.fitBounds(place.viewport); // zoom to fit the whole place
        } else if (place.location) {
          map.setCenter(place.location);
          map.setZoom(11);
        }
      });
    });

    console.log("[PARKMAP 8] Places autocomplete ready");
  }).catch(function (err) {
    console.error("[PARKMAP 8-FAIL] Places library failed to load:", err);
  });

  // ---- park name search: filter parks, click a result to select + focus ----
  const searchbar = document.getElementById("searchbar");
  if (searchbar) searchbar.placeholder = "Search for parks here..."
  const listHolder = document.getElementById("list-holder");
  const MAX_RESULTS = 50;

  if (searchbar && listHolder) {
    searchbar.addEventListener("keyup", () => {
      const input = searchbar.value.trim().toLowerCase();
      listHolder.innerHTML = "";
      if (!input) return; // don't dump all 3,558 parks on an empty query

      const matches = parkData
        .filter(park => park.name.toLowerCase().includes(input))
        .slice(0, MAX_RESULTS);

      matches.forEach(park => {
        const entry = parkRegistry.get(park.name);
        const li = document.createElement("li");
        li.style.cursor = "pointer";
        li.textContent = park.name + (entry.selected ? " \u2713" : "");

        li.addEventListener("click", () => {
          setSelected(entry, !entry.selected);
          li.textContent = park.name + (entry.selected ? " \u2713" : "");
          const firstPoint = entry.park.coords && entry.park.coords[0] && entry.park.coords[0][0]; // first point of first ring
          if (firstPoint) {
            map.panTo(firstPoint);
            map.setZoom(15);
          }
        });

        listHolder.appendChild(li);
      });
    });
  } else {
    console.warn("[PARKMAP 9-FAIL] searchbar or list-holder not found in DOM");
  }
};

// ---------- Google Maps loader (classic callback style, no loading=async) ----------
(function () {
  if (window.google && window.google.maps && window.google.maps.Map) {
    console.log("[PARKMAP] Maps API already present, initialising directly");
    window.initAlchemerMap();
  } else {
    console.log("[PARKMAP] Injecting Maps API script");
    const script = document.createElement("script");
    script.src = "https://maps.googleapis.com/maps/api/js?key=" + GOOGLE_MAPS_KEY +
      "&v=weekly&libraries=places&callback=initAlchemerMap";
    script.type = "text/javascript";
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
  }
})();