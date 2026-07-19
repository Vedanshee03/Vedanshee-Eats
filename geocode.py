"""Geocode restaurants via Nominatim (OpenStreetMap). Rate-limited to 1 req/sec."""
import json
import ssl
import time
import urllib.parse
import urllib.request

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

HEADERS = {"User-Agent": "vedanshee-nyc-food-map/1.0 (personal project)"}
NYC_VIEWBOX = "-74.05,40.55,-73.75,40.92"


def geocode(query):
    params = urllib.parse.urlencode({
        "q": query,
        "format": "json",
        "limit": 1,
        "viewbox": NYC_VIEWBOX,
        "bounded": 1,
    })
    url = f"https://nominatim.openstreetmap.org/search?{params}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as resp:
        results = json.loads(resp.read().decode())
    if results:
        r = results[0]
        return float(r["lat"]), float(r["lon"]), r.get("display_name", "")
    return None


def main():
    with open("data_source.json") as f:
        places = json.load(f)

    for p in places:
        queries = [p["query"]]
        # fallback: name-only search
        if p["name"] not in p["query"]:
            queries.append(f'{p["name"]}, New York, NY')
        queries.append(f'{p["name"]}, Manhattan, NY')

        result = None
        for q in queries:
            try:
                result = geocode(q)
            except Exception as e:
                print(f"  error for {q!r}: {e}", flush=True)
                result = None
            time.sleep(1.1)
            if result:
                break

        if result:
            p["lat"], p["lng"], p["matched"] = result[0], result[1], result[2]
            print(f'OK   {p["id"]:3d} {p["name"]} -> {result[0]:.5f}, {result[1]:.5f}', flush=True)
        else:
            p["lat"], p["lng"], p["matched"] = None, None, None
            print(f'FAIL {p["id"]:3d} {p["name"]}', flush=True)

    with open("geocoded.json", "w") as f:
        json.dump(places, f, indent=2)

    failed = [p["name"] for p in places if p["lat"] is None]
    print(f"\nDone. {len(places) - len(failed)}/{len(places)} geocoded.")
    if failed:
        print("Failed:", ", ".join(failed))


if __name__ == "__main__":
    main()
