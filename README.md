# Vedanshee eats — A Stars Hollow Food Diary

A Gilmore Girls–themed interactive map of restaurants, cafes, wineries, bakeries, and coffee stops across New York City, McMinnville, the San Francisco Bay Area, and Los Angeles.

## How to run it

No build step needed — it's a plain static site. From this folder, run:

```bash
python3 -m http.server 8741
```

Then open [http://localhost:8741](http://localhost:8741) in your browser.

(Opening `index.html` directly by double-clicking also works in most browsers.)

## Features

- Interactive Leaflet map with color-coded, emoji pins for every place
- Location tabs for all places, New York City, McMinnville, the San Francisco Bay Area, and Los Angeles
- Filter chips by category (Coffee, Pizza, Wine Tasting, Bagels, etc.)
- Search box that matches names, cuisines, and locations
- Click a card in the sidebar to fly to its pin; click a pin to see a Gilmore Girls quip and a Google Maps link
- Rotating Lorelai/Rory/Michel quotes in the header
- Autumn-in-Stars-Hollow color palette, string lights, and serif typography

## Files

- `index.html`, `styles.css`, `app.js` — the site itself
- `data.js` — the restaurant list with coordinates (edit here if a pin looks off)
- `data_source.json` — the original list with search queries
- `geocode.py` — fetches coordinates from OpenStreetMap Nominatim
- `build_data.py` — merges geocoded results + manual fixes into `data.js`

## Fixing a pin location

Some pins (marked "pin location approximate" in their popup) were placed by hand
because the geocoder couldn't find them. To fix one, either edit its `lat`/`lng`
directly in `data.js`, or update the `MANUAL` dictionary in `build_data.py` and
rerun `python3 build_data.py`.
