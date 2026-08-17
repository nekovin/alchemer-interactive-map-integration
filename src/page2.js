(function () {
  const css = `
    #park-map-wrapper {
      --accent: #d32f2f;
      --accent-dark: #b71c1c;
      --accent-soft: #fdecea;
      --accent-border: #f5c6c2;
      --border: #dfe1e5;
      --text: #202124;
      color-scheme: light;
      font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
      color: var(--text);
    }
    #park-map-wrapper * { box-sizing: border-box; }
    #park-map-wrapper h2, #park-map-wrapper h3 { color: var(--accent-dark); }

    /* ---- side-by-side search row (stacks on narrow screens) ---- */
    #park-map-wrapper .search-row {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: flex-start;
      margin-bottom: 16px;
    }
    #park-map-wrapper .search-col { flex: 1 1 260px; min-width: 0; }
    #park-map-wrapper .search-col > label {
      display: block;
      margin-bottom: 6px;
      font-size: 13px;
      font-weight: 600;
      color: #444;
    }
    #location-search, #park-map-wrapper .search-box { width: 100%; }
    /* PlaceAutocompleteElement is a shadow-DOM web component - only its host
       sizing is reliably controllable, so we match .search-box to IT. */
    #location-search gmp-place-autocomplete { width: 100%; display: block; min-height: 42px; }

    #park-map-wrapper .search-box {
      display: flex;
      align-items: center;
      height: 42px;
      padding: 0 12px;
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 6px;
      box-shadow: 0 1px 2px rgba(0, 0, 0, .08);
      transition: border-color .15s, box-shadow .15s;
    }
    #park-map-wrapper .search-box:focus-within {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(211, 47, 47, .15);
    }
    #park-map-wrapper .search-box svg { flex: 0 0 auto; margin-right: 8px; }
    #park-map-wrapper .search-box input {
      flex: 1;
      height: 100%;
      border: none;
      outline: none;
      background: transparent;
      font-size: 14px;
      color: var(--text);
    }

    /* park-name search results */
    #list-holder { list-style: none; margin: 8px 0; padding: 0; }
    #list-holder:empty { display: none; }
    #list-holder li {
      padding: 8px 10px;
      cursor: pointer;
      border-radius: 6px;
      font-size: 14px;
    }
    #list-holder li:hover { background: var(--accent-soft); }

    /* location-search degraded notice */
    #places-notice { display: none; margin-top: 6px; font-size: 12px; color: var(--accent-dark); }
    #park-map-wrapper .retry-link {
      background: none; border: none; padding: 0;
      color: var(--accent); font: inherit; cursor: pointer; text-decoration: underline;
    }

    /* ---- map + loading / error overlays ---- */
    #map-wrap {
      position: relative;
      width: 100%;
      height: 600px;
      border: 1px solid #ccc;
      border-radius: 8px;
      overflow: hidden;
    }
    #map-wrap #map { width: 100%; height: 100%; }

    #map-loader {
      position: absolute;
      inset: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 14px;
      z-index: 2;
      background: linear-gradient(90deg, #ececec 25%, #f5f5f5 37%, #ececec 63%);
      background-size: 400% 100%;
      animation: parkmap-shimmer 1.4s ease infinite;
    }
    @keyframes parkmap-shimmer { 0% { background-position: 100% 0; } 100% { background-position: 0 0; } }
    #park-map-wrapper .spinner {
      width: 40px; height: 40px;
      border: 4px solid rgba(211, 47, 47, .2);
      border-top-color: var(--accent);
      border-radius: 50%;
      animation: parkmap-spin .9s linear infinite;
    }
    @keyframes parkmap-spin { to { transform: rotate(360deg); } }
    #park-map-wrapper .loader-text { font-size: 14px; color: #555; }

    #map-error {
      position: absolute;
      inset: 0;
      display: none; /* toggled to flex by showError() */
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 14px;
      text-align: center;
      padding: 24px;
      z-index: 3;
      background: #fff;
    }
    #park-map-wrapper .error-icon { font-size: 32px; }
    #park-map-wrapper .error-text { font-size: 15px; color: #333; max-width: 340px; }

    #park-map-wrapper .retry-btn {
      padding: 10px 20px;
      font-size: 15px;
      font-weight: 600;
      background: var(--accent);
      color: #fff;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      transition: background .15s;
    }
    #park-map-wrapper .retry-btn:hover { background: var(--accent-dark); }

    /* ---- selected parks as removable chips ---- */
    #selected-empty { color: #777; font-style: italic; }
    #selected-holder {
      list-style: none;
      margin: 8px 0;
      padding: 0;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    #selected-holder:empty { display: none; }
    #park-map-wrapper .chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 6px 4px 12px;
      background: var(--accent-soft);
      color: var(--accent-dark);
      border: 1px solid var(--accent-border);
      border-radius: 999px;
      font-size: 13px;
    }
    #park-map-wrapper .chip-remove {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 18px; height: 18px;
      padding: 0;
      border: none;
      border-radius: 50%;
      background: rgba(183, 28, 28, .12);
      color: var(--accent-dark);
      font-size: 12px;
      line-height: 1;
      cursor: pointer;
    }
    #park-map-wrapper .chip-remove:hover { background: var(--accent); color: #fff; }
  `;
  const styleEl = document.createElement("style");
  styleEl.textContent = css;
  document.head.appendChild(styleEl);
})();

/* Alchemer JavaScript Action - park selection map (v3)
   Changes from v2:
   - real loading skeleton/spinner + friendly error panel with Retry (the v2
     .loader / #map-interface-content / #map-loader references pointed at
     elements that never existed - all dead branches)
   - capped retry-with-backoff on the Azure fetch and Maps script load (v2
     retried forever every 100/200ms and had no script.onerror at all)
   - idempotent init: repeated refreshes / double callbacks can't stack a
     second Places widget or redraw polygons
   - side-by-side search bars, red UI accents, selected parks as chips
   This file MIRRORS index.html's <script>; keep the two in sync.
*/

console.log("[PARKMAP] JS action loaded (v3)");

const finalAzureUrl = 'https://alchemer01.blob.core.windows.net/4463/parks_data/parks_data.json?sp=r&st=2026-07-01T05:48:03Z&se=2026-07-29T14:03:03Z&spr=https&sv=2026-02-06&sr=b&sig=qw578tyhKN%2FJLu60G2eBMA7nDDrVpjGrgtuHKP%2FJogo%3D';
const ALCHEMER_HIDDEN_FIELD_ID = "sgE-391014007-2-19-element"; // THIS NEEDS TO BE MAINTAINED IF SOMEBODY SCREWS W MY CODE >:(
const GOOGLE_MAPS_KEY = "AIzaSyBnhF8F278dHno51nyrbqBEQn_rELO4mQE";

/* =========================================================================
   Shared helpers - MIRRORED FROM index.html (no build system, no imports).
   ========================================================================= */
const delay = ms => new Promise(r => setTimeout(r, ms));

// Retry a promise-returning fn up to `attempts` times with 500/1000/2000ms backoff.
async function retryWithBackoff(taskFn, opts) {
  const { attempts = 3, baseDelay = 500, label = "task" } = opts || {};
  let lastErr;
  for (let n = 1; n <= attempts; n++) {
    try { return await taskFn(); }
    catch (err) {
      lastErr = err;
      console.warn("[retry] " + label + " attempt " + n + "/" + attempts + " failed:", err);
      if (n < attempts) await delay(baseDelay * Math.pow(2, n - 1));
    }
  }
  throw lastErr;
}

const SLOW_LOAD_MS = 12000;
let slowLoadTimer = null;

function showLoader(text) {
  const errorPanel = document.getElementById("map-error");
  if (errorPanel) errorPanel.style.display = "none";
  const loader = document.getElementById("map-loader");
  if (!loader) return;
  loader.style.display = "flex";
  const t = loader.querySelector(".loader-text");
  if (t) t.textContent = text || "Loading map…";
  clearTimeout(slowLoadTimer);
  slowLoadTimer = setTimeout(function () {
    if (t) t.textContent = "Still loading the map — this can take a moment on slow connections…";
  }, SLOW_LOAD_MS);
}

function hideLoader() {
  clearTimeout(slowLoadTimer);
  const loader = document.getElementById("map-loader");
  if (loader) loader.style.display = "none";
}

// Fatal error over the map area, with a wired Retry button.
function showError(message, onRetry) {
  hideLoader();
  const panel = document.getElementById("map-error");
  if (!panel) return;
  const msg = panel.querySelector(".error-text");
  if (msg) msg.textContent = message;
  panel.style.display = "flex";
  const btn = panel.querySelector(".retry-btn");
  if (btn) btn.onclick = function () { panel.style.display = "none"; onRetry(); };
}

// Non-fatal notice for the location search (map + park search still work).
function showPlacesNotice(onRetry) {
  const notice = document.getElementById("places-notice");
  if (!notice) return;
  notice.style.display = "block";
  const btn = notice.querySelector(".retry-link");
  if (btn) btn.onclick = function () { notice.style.display = "none"; onRetry(); };
}

/* ---------- state ---------- */
let userSelections = [];
const parkRegistry = new Map(); // park.name -> { park, polygon, selected }
let map = null;
let mapInitialized = false;      // idempotency guard
let domWaitCount = 0;
const MAX_DOM_WAITS = 25;        // ~5s at 200ms - then surface an error instead of looping forever

const vicBounds = { north: -32.9, south: -40.2, east: 150.0, west: 140.9 };

/* ---------- Alchemer sync (runs on every change, no submit button needed) ---------- */
function updateAlchemerField() {
  const alchemerField = document.getElementById(ALCHEMER_HIDDEN_FIELD_ID);
  if (!alchemerField) {
    console.warn("[PARKMAP] Hidden field not found:", ALCHEMER_HIDDEN_FIELD_ID);
    return;
  }
  alchemerField.value = userSelections.join(", ");
  alchemerField.dispatchEvent(new Event("change", { bubbles: true }));
}

/* ---------- selected-parks chips ---------- */
function renderSelections() {
  const selectedHolder = document.getElementById("selected-holder");
  const selectedCount = document.getElementById("selected-count");
  const selectedEmpty = document.getElementById("selected-empty");
  if (!selectedHolder) return;

  selectedHolder.innerHTML = "";
  if (selectedCount) selectedCount.textContent = userSelections.length;
  if (selectedEmpty) selectedEmpty.style.display = userSelections.length ? "none" : "";

  userSelections.forEach(function (name) {
    const entry = parkRegistry.get(name);
    const chip = document.createElement("li");
    chip.className = "chip";

    const label = document.createElement("span");
    label.textContent = name;

    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "chip-remove";
    remove.textContent = "✕";
    remove.title = "Remove";
    remove.setAttribute("aria-label", "Remove " + name);
    remove.addEventListener("click", function () { setSelected(entry, false); });

    chip.appendChild(label);
    chip.appendChild(remove);
    selectedHolder.appendChild(chip);
  });
}

/* ---------- single source of truth for select / deselect ---------- */
function setSelected(entry, selected) {
  entry.selected = selected;
  entry.polygon.setOptions({
    fillColor: selected ? entry.park.selectedColor : entry.park.defaultColor,
    strokeColor: selected ? entry.park.selectedColor : entry.park.defaultColor
  });

  if (selected) {
    if (!userSelections.includes(entry.park.name)) userSelections.push(entry.park.name);
  } else {
    userSelections = userSelections.filter(function (item) { return item !== entry.park.name; });
  }

  renderSelections();
  updateAlchemerField();
  console.log("Current Selections Array:", userSelections);
}

/* ---------- build steps ---------- */
function loadParkData() {
  return retryWithBackoff(function () {
    return fetch(finalAzureUrl, { method: "GET", mode: "cors" }).then(function (response) {
      if (!response.ok) throw new Error("Azure HTTP Error: " + response.status);
      return response.json();
    });
  }, { label: "park data" });
}

// Inject the Maps API script once; resolves on callback, rejects on script error.
function injectMapsScriptOnce() {
  return new Promise(function (resolve, reject) {
    if (window.google && window.google.maps && window.google.maps.Map) { resolve(); return; }
    // drop any prior (failed) tag so retries don't stack duplicate scripts
    document.querySelectorAll('script[data-parkmap-maps]').forEach(function (s) { s.remove(); });
    window.__parkMapMapsReady = function () { resolve(); };
    const script = document.createElement("script");
    script.dataset.parkmapMaps = "1";
    script.src = "https://maps.googleapis.com/maps/api/js?key=" + GOOGLE_MAPS_KEY +
      "&v=weekly&libraries=places&callback=__parkMapMapsReady";
    script.async = true;
    script.defer = true;
    script.onerror = function () { reject(new Error("Google Maps script failed to load")); };
    document.head.appendChild(script);
  });
}

function drawPolygons(parkData) {
  if (parkRegistry.size) return; // idempotent - don't redraw on retry
  parkData.forEach(function (park) {
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
}

// Location search: Google Places autocomplete moves the map. Non-fatal (degraded).
function setupPlaces() {
  return retryWithBackoff(function () {
    return google.maps.importLibrary("places");
  }, { label: "places" }).then(function (placesLib) {
    const container = document.getElementById("location-search");
    if (!container) return;
    if (container.querySelector("gmp-place-autocomplete")) return; // idempotent - already attached

    const placeAutocomplete = new placesLib.PlaceAutocompleteElement();
    placeAutocomplete.placeholder = "Search for a street / area..";
    placeAutocomplete.includedRegionCodes = ["au"];
    placeAutocomplete.locationRestriction = vicBounds; // only suggest places in Victoria
    container.replaceChildren(placeAutocomplete);

    placeAutocomplete.addEventListener("gmp-select", function (event) {
      const place = event.placePrediction.toPlace();
      place.fetchFields({ fields: ["location", "viewport"] }).then(function () {
        if (place.viewport) {
          map.fitBounds(place.viewport);
        } else if (place.location) {
          map.setCenter(place.location);
          map.setZoom(11);
        }
      });
    });
  });
}

// Park-name search: filter parks, click a result to select + focus it.
function setupSearch(parkData) {
  const searchbar = document.getElementById("searchbar");
  const listHolder = document.getElementById("list-holder");
  const MAX_RESULTS = 50;
  if (!searchbar || !listHolder) {
    console.warn("[PARKMAP] searchbar or list-holder not found in DOM");
    return;
  }
  searchbar.placeholder = "Search for parks here...";

  searchbar.addEventListener("keyup", function () {
    const input = searchbar.value.trim().toLowerCase();
    listHolder.innerHTML = "";
    if (!input) return; // don't dump all 3,558 parks on an empty query

    parkData
      .filter(function (park) { return park.name.toLowerCase().includes(input); })
      .slice(0, MAX_RESULTS)
      .forEach(function (park) {
        const entry = parkRegistry.get(park.name);
        const li = document.createElement("li");
        li.style.cursor = "pointer";
        li.textContent = park.name + (entry.selected ? " ✓" : "");
        li.addEventListener("click", function () {
          setSelected(entry, !entry.selected);
          li.textContent = park.name + (entry.selected ? " ✓" : "");
          const firstPoint = entry.park.coords && entry.park.coords[0] && entry.park.coords[0][0];
          if (firstPoint) { map.panTo(firstPoint); map.setZoom(15); }
        });
        listHolder.appendChild(li);
      });
  });
}

// Build the map + polygons once the #map div exists (capped wait, no infinite loop).
function buildMap() {
  if (mapInitialized) return;

  const mapElement = document.getElementById("map");
  if (!mapElement) {
    if (++domWaitCount > MAX_DOM_WAITS) {
      console.warn("[PARKMAP] #map div never appeared");
      showError("The map area didn't load. Please try again.", function () { domWaitCount = 0; buildMap(); });
      return;
    }
    setTimeout(buildMap, 200);
    return;
  }

  const parkData = window.azureParksData;

  map = new google.maps.Map(mapElement, {
    zoom: 9,
    center: { lat: -37.8080, lng: 144.9750 },
    restriction: { latLngBounds: vicBounds, strictBounds: false }, // can't pan outside Victoria
    minZoom: 6 // stop zooming out past the state
  });

  map.addListener("tilesloaded", function () { hideLoader(); });

  drawPolygons(parkData);
  setupSearch(parkData);
  mapInitialized = true;

  // Places is non-fatal - degrade gracefully if it fails.
  setupPlaces().catch(function (err) {
    console.error("[places] failed to load:", err);
    showPlacesNotice(function () {
      setupPlaces().catch(function (e) { console.error("[places] retry failed:", e); });
    });
  });
}

/* ---------- orchestration (Retry re-runs the failed step; guards skip done work) ---------- */
async function start() {
  showLoader();

  if (!window.azureParksData) {
    try {
      window.azureParksData = await loadParkData();
      console.log("[PARKMAP] Azure data saved,", window.azureParksData.length, "parks");
    } catch (e) {
      showError("We couldn't load the list of parks. Please check your connection.", start);
      return;
    }
  }

  try {
    await retryWithBackoff(injectMapsScriptOnce, { label: "maps api" });
  } catch (e) {
    showError("The map failed to load. Please try again.", start);
    return;
  }

  buildMap();
}

// Back-compat: anything still calling the old global re-enters the orchestrator.
window.initAlchemerMap = start;

start();
