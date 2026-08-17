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
- [FileGDB format spec (reverse-engineered): file layout & `aXXXXXXXX` naming](https://github.com/rouault/dump_gdbtable/wiki/FGDB-Spec) — what `.gdbtable`/`.gdbtablx`/`.spx`/`.atx` hold and the hex dataset IDs.
- [Esri: system tables in a file geodatabase](https://desktop.arcgis.com/en/arcmap/latest/manage-data/geodatabases/geodatabase-system-tables.htm) — `GDB_SystemCatalog`, `GDB_Items`, etc. (IDs 1–8).
- [GeoPandas: `read_file()`](https://geopandas.org/en/stable/docs/reference/api/geopandas.read_file.html) — reads a `.gdb` folder (pass `layer=`).
- [GeoPandas: `list_layers()`](https://geopandas.org/en/stable/docs/reference/api/geopandas.list_layers.html) — enumerate layers in a multi-layer `.gdb`.
- [GeoPandas: `GeoDataFrame.to_crs()`](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_crs.html) — PARKRES is VicGrid94 (EPSG:3111); GeoJSON needs EPSG:4326.
- [GeoPandas: `GeoDataFrame.to_file()`](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_file.html) — write with `driver="GeoJSON"`.
- [GeoPandas: reading/writing files & engines](https://geopandas.org/en/stable/docs/user_guide/io.html) — `pyogrio` is the default engine.
- [pyogrio docs](https://pyogrio.readthedocs.io/en/latest/) — the GDAL-backed engine geopandas uses (ships GDAL in its wheel).
- [EPSG:3111 — GDA94 / Vicgrid](https://epsg.io/3111) — the projection Victorian spatial data is distributed in.
- [Shapely: `Polygon.exterior`](https://shapely.readthedocs.io/en/stable/reference/shapely.Polygon.html) — the outer ring we emit per polygon (holes are dropped).
- [Shapely: `MultiPolygon.geoms`](https://shapely.readthedocs.io/en/stable/reference/shapely.MultiPolygon.html) — iterate the parts of a multipart park.
- [Shapely: `geom_type`](https://shapely.readthedocs.io/en/stable/manual.html#object.geom_type) — Polygon vs MultiPolygon dispatch.

## Category lookup (PV_parks_piers.xlsx)
- [pandas: `read_excel()`](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html) — read the Label/Category sheet.
- [pandas: `DataFrame.to_excel()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html) — write the unmatched-labels report.
- [pandas: Excel I/O user guide](https://pandas.pydata.org/docs/user_guide/io.html#excel-files) — engine selection and gotchas.
- [openpyxl docs](https://openpyxl.readthedocs.io/en/stable/) — the `.xlsx` engine pandas uses.
- [Python: `re.sub()`](https://docs.python.org/3/library/re.html#re.sub) — normalising labels before matching.
- [Python: `dict.setdefault()`](https://docs.python.org/3/library/stdtypes.html#dict.setdefault) — grouping geometries by park name.
- [OGR ESRI Shapefile (`.shp`) driver](https://gdal.org/en/stable/drivers/vector/shapefile.html)

## Google Maps
- [Maps JavaScript API: Polygons](https://developers.google.com/maps/documentation/javascript/shapes#polygons)
- [Polygon `paths` (array of paths → separate loops, even-odd rule)](https://developers.google.com/maps/documentation/javascript/reference/polygon#PolygonOptions.paths)
- [Maps JavaScript API: Events](https://developers.google.com/maps/documentation/javascript/events)
- [Maps JavaScript API: Load the API (callback)](https://developers.google.com/maps/documentation/javascript/load-maps-js-api)
- [Places API: `PlaceAutocompleteElement` (location search widget, `gmp-select` event)](https://developers.google.com/maps/documentation/javascript/place-autocomplete-new) — the second search bar.
- [Places API: `fetchFields()` (location, viewport)](https://developers.google.com/maps/documentation/javascript/reference/place#Place.fetchFields)

https://developers.google.com/maps/documentation/javascript/events
https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener
