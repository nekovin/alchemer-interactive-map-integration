# Reference

Documentation links for techniques used in this project.

## Script loading & execution order
- [MDN: `<script>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script) — overview of all script attributes.
- [MDN: `type="module"` (deferred by default)](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#module) — why module scripts run after classic scripts.
- [MDN: `defer` attribute & execution order](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#defer) — when deferred scripts run.
- [MDN: `async` attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#async) — async scripts run as soon as they load (relevant to the Google Maps `async defer` tag).

## JavaScript
- [MDN: `Array.prototype.forEach()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach)
- [MDN: `Array.prototype.filter()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter)
- [MDN: `Array.prototype.includes()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/includes)
- [MDN: `CustomEvent`](https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent)
- [MDN: `EventTarget.addEventListener()`](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener)
- [MDN: Import attributes (`with { type: "json" }`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import/with)
- [MDN: `String.prototype.includes()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/includes) — case-insensitive search matching.
- [MDN: `Map`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map) — park registry keyed by name.
- [Maps JavaScript API: `Map.panTo()` / `setZoom()`](https://developers.google.com/maps/documentation/javascript/reference/map#Map.panTo) — focus the map on a searched park.

## HTML / CSS
- [MDN: `<style>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/style)

## Source data (Parks Victoria PARKRES)
- [DataVic: search / download Victorian spatial data (`.gdb`, `.shp`, `.tab`)](https://www.data.vic.gov.au/) — where PARKRES is distributed.
- [Vicmap Features of Interest / Parks Victoria PARKRES](https://discover.data.vic.gov.au/dataset/parkres-parks-and-reserves) — the parks & reserves feature class.
- [GDAL `ogr2ogr` (convert `.gdb`/`.shp` → GeoJSON)](https://gdal.org/en/stable/programs/ogr2ogr.html) — likely conversion step to `PARKRE_geo.json`.
- [OGR Esri File Geodatabase (`.gdb`) driver](https://gdal.org/en/stable/drivers/vector/openfilegdb.html)
- [OGR ESRI Shapefile (`.shp`) driver](https://gdal.org/en/stable/drivers/vector/shapefile.html)

## Google Maps
- [Maps JavaScript API: Polygons](https://developers.google.com/maps/documentation/javascript/shapes#polygons)
- [Polygon `paths` (array of paths → separate loops, even-odd rule)](https://developers.google.com/maps/documentation/javascript/reference/polygon#PolygonOptions.paths)
- [Maps JavaScript API: Events](https://developers.google.com/maps/documentation/javascript/events)
- [Maps JavaScript API: Load the API (callback)](https://developers.google.com/maps/documentation/javascript/load-maps-js-api)

https://developers.google.com/maps/documentation/javascript/events
https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener
