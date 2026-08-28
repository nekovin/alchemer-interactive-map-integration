# Study resources

Ordered by what this project actually exercises.

## JavaScript fundamentals

- MDN JavaScript Guide — https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide
- javascript.info (best structured free course) — https://javascript.info/
- Truthy / falsy, `||` and `??` — https://developer.mozilla.org/en-US/docs/Glossary/Truthy
- Array methods (map, filter, forEach, slice) — https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array

## DOM and events

- Introduction to events — https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events
- Event bubbling and capture — https://javascript.info/bubbling-and-capturing
- jQuery learning centre — https://learn.jquery.com/

## Async

- Promises — https://javascript.info/promise-basics
- async/await — https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Promises
- Using fetch — https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch

## HTTP

- HTTP overview — https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
- CORS (start here, it has bitten this project) — https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
- Caching — https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching
- Compression — https://developer.mozilla.org/en-US/docs/Web/HTTP/Compression
- Status codes — https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

## Google Maps JavaScript API

- Overview — https://developers.google.com/maps/documentation/javascript/overview
- Shapes (Polygon, Circle) — https://developers.google.com/maps/documentation/javascript/shapes
- Events — https://developers.google.com/maps/documentation/javascript/events
- Advanced markers — https://developers.google.com/maps/documentation/javascript/advanced-markers/overview

## Geospatial

- Coordinate reference systems explained — https://docs.qgis.org/latest/en/docs/gentle_gis_introduction/coordinate_reference_systems.html
- EPSG registry (look up 4326, 3111, 7844) — https://epsg.io/
- GeoPandas user guide — https://geopandas.org/en/stable/docs/user_guide.html
- Shapely manual — https://shapely.readthedocs.io/en/stable/manual.html
- Douglas-Peucker simplification — https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm

## Python packaging

- Packaging user guide — https://packaging.python.org/en/latest/
- pyproject.toml spec — https://packaging.python.org/en/latest/specifications/pyproject-toml/
- Entry points — https://packaging.python.org/en/latest/specifications/entry-points/
- argparse tutorial — https://docs.python.org/3/howto/argparse.html

## Reliability and system design

- Google SRE Book (free) — https://sre.google/sre-book/table-of-contents/
- Designing Data-Intensive Applications (Kleppmann) — the standard text
- Fail fast — https://en.wikipedia.org/wiki/Fail-fast
- Idempotence — https://en.wikipedia.org/wiki/Idempotence

## Azure

- Blob storage docs — https://learn.microsoft.com/en-us/azure/storage/blobs/
- SAS tokens — https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview
- Monitoring blob storage — https://learn.microsoft.com/en-us/azure/storage/blobs/monitor-blob-storage

## Testing

- pytest getting started — https://docs.pytest.org/en/stable/getting-started.html
- Python testing with pytest (Okken) — the standard book

## Local harness

Test a map action against the real `map-box.html` before pasting into Alchemer.

```
python3 -m http.server 8765 --directory src/parksres
```

Open http://localhost:8765/local/harness.html — pick the action, paste the payload
URL and Maps key, Run. The table shows what each hidden field would save.
"Run with hidden fields missing" simulates a stale field id.
