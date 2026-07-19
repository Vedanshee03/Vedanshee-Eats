"""Merge geocoded results with manual fixes and emit data.js for the site."""
import json

# Manual coordinates for places Nominatim missed or matched incorrectly.
# approx=True marks best-guess placements (shown as "approximate" in the popup).
MANUAL = {
    3:   (40.7477, -73.9866, False),  # Valla Table - 2 W 32nd St, Koreatown
    4:   (40.7614, -73.9910, True),   # Hyderabadi Zaiqa - Hell's Kitchen area
    9:   (40.7593, -73.9905, True),   # A Pasta Bar - Hell's Kitchen area
    23:  (40.7625, -73.9954, False),  # Jolly Goat Coffee Bar - 10th Ave & W 46th
    28:  (40.733920, -73.993144, False),  # Dorado Tacos - 28 E 12th St
    31:  (40.7530, -73.9847, True),   # Moonbowls - Midtown
    35:  (40.7420, -74.0048, False),  # Starbucks Reserve Roastery - 61 9th Ave
    39:  (40.7520, -73.9720, True),   # Hashi Mart - Midtown East
    63:  (40.7640, -73.9880, True),   # Dovetail Bakery
    66:  (40.7578, -73.9819, False),  # Adel's Halal Cart - W 46th & 6th Ave
    67:  (40.7550, -73.9860, True),   # Acadia - Midtown (bad geocode: realty trust)
    69:  (40.7523, -73.9840, True),   # The Soiree - Midtown
    72:  (40.7375, -73.9905, False),  # Lillie's Victorian - 13 E 17th St
    73:  (40.763653, -73.989041, False),  # Rancho Tequileria - 741 9th Ave
    76:  (40.743540, -73.980013, False),  # Norma Gastronomia Siciliana - 438 3rd Ave
    80:  (40.7620, -73.9836, False),  # Din Tai Fung - 1633 Broadway
    87:  (40.7158, -73.9970, True),   # Mr Wu Dim Sum - Chinatown
    90:  (40.7635, -73.9885, False),  # Hibernia - 401 W 50th St
    93:  (40.7570, -73.9840, True),   # Frena - Midtown
    95:  (40.7280, -73.9870, True),   # Omakaseed - East Village
    98:  (40.7413, -73.9836, False),  # Saravana Bhavan - 81 Lexington Ave
    101: (40.7628, -73.9945, True),   # Chai Samosa - Hell's Kitchen
    104: (40.7370, -73.9820, True),   # McCarthy's Pub - Gramercy
    105: (40.7600, -73.9910, True),   # Kustom Matcha & Espresso Bar - Hell's Kitchen
    106: (40.734646, -73.992793, False),  # Taboonette - 30 E 13th St
    107: (45.210097, -123.192765, False),  # 1882 Grille
    108: (45.209808, -123.197378, False),  # Abuela's Nuestra Cocina
    109: (45.210652, -123.194050, False),  # Cypress Restaurant & Bar
    110: (45.210221, -123.197097, False),  # Harvest Fresh Grocery & Deli
    111: (45.209784, -123.197113, False),  # La Rambla Restaurant
    112: (45.210096, -123.194078, False),  # Los Molcajetes
    113: (45.209909, -123.196420, False),  # Pizza Capo
    114: (45.210121, -123.196445, False),  # Pura Vida Cocina
    115: (45.196270, -123.206218, False),  # Sushi Kyo
    116: (45.210115, -123.196372, False),  # Taste of India One
    117: (45.200625, -123.204143, False),  # Geraldi's
    118: (45.209847, -123.194735, False),  # Pinot Vista Tasting Lounge
    119: (45.210163, -123.195479, False),  # Union Block Coffee
    120: (45.209814, -123.197459, False),  # The Grove Tasting Room
    121: (45.210105, -123.193499, False),  # Terra Vina Wines Tasting Room
    122: (45.209917, -123.193813, False),  # R. Stuart & Co. Tasting Room
    123: (45.209898, -123.193478, False),  # Acorn to Oak Wine Experience
    124: (45.209825, -123.197242, False),  # Jacob Williams Winery
    125: (37.767050, -122.429112, False),  # Verve Coffee Roasters
    126: (37.805294, -122.431900, True),   # Equator Coffees - branch may vary
    127: (37.443313, -122.160910, False),  # Meyhouse Palo Alto
    128: (37.753866, -122.420551, False),  # Beretta Valencia
    129: (34.073768, -118.309520, False),  # DALKOM Dessert Cafe
    130: (34.045390, -118.264035, False),  # Mr. Masala
    131: (34.025034, -118.396413, False),  # Cali Tandoor
    132: (34.062062, -118.302651, True),   # BCD Tofu House - branch may vary
    133: (34.083384, -118.348053, False),  # Le Ciel Pink
    134: (34.066434, -118.254117, False),  # The Park's Finest
    135: (34.075898, -118.344919, False),  # Mensch Bakery & Kitchen
    136: (34.083659, -118.341963, False),  # Tony Khachapuri
    137: (34.052900, -118.303955, False),  # Amandine Patisserie Cafe
    138: (34.047673, -118.435370, False),  # Taste of Tehran
    139: (34.049048, -118.260676, True),   # California Pizza Kitchen - branch may vary
    140: (34.076078, -118.255180, False),  # Gyoza Bar
    141: (34.082729, -118.272342, False),  # Pho Cafe
    142: (34.050631, -118.308838, False),  # Cafe de Mama
    143: (34.039763, -118.298739, False),  # Moonbowls
    144: (34.039790, -118.298733, True),   # Joe's Pizza - branch may vary
    145: (34.061474, -118.298824, True),   # The Halal Guys - branch may vary
    146: (34.032184, -118.360756, False),  # Mizlala West Adams
    147: (34.143429, -118.398960, True),   # Chin Chin - branch may vary
    148: (34.044710, -118.232493, False),  # Kombu Sushi
    149: (34.017364, -118.278205, False),  # Thai Corner Food Express
    150: (34.050540, -118.254103, True),   # Sweetgreen - branch may vary
    151: (34.097847, -118.328424, True),   # Veggie Grill - branch may vary
    152: (34.104149, -118.328731, False),  # Barn Farm Breakfast
    153: (34.017610, -118.409715, False),  # Abhiruchi Grill
    154: (33.981829, -118.225747, True),   # La Monarca Bakery - branch may vary
    155: (34.024923, -118.278720, False),  # Pot of Cha
    156: (34.045187, -118.249543, False),  # Wake and Late
    157: (34.041090, -118.426875, True),   # Maria's Italian Kitchen - branch may vary
    158: (34.080536, -118.092966, False),  # Banh Cuon Tay Ho - San Gabriel
    160: (34.041940, -118.235469, True),   # Urth Caffe - branch may vary
    161: (34.139645, -118.023592, False),  # Nirvana Indian Cuisine
    162: (34.048814, -118.240482, True),   # Cafe Dulce - branch may vary
    163: (34.025165, -118.285251, False),  # Insomnia Cookies
    164: (34.047991, -118.240192, False),  # Yoboseyo Superette
    165: (34.025232, -118.284393, False),  # Il Giardino
    166: (34.025505, -118.284492, False),  # Bruxie USC Village
    167: (34.025033, -118.284979, True),   # SunLife Organics - branch may vary
    168: (34.026055, -118.284737, True),   # Bandit Chow Mein food truck - USC area
    169: (34.024929, -118.285231, False),  # Ramen Kenjo
    170: (34.046080, -118.235494, True),   # Salt & Straw - branch may vary
    171: (34.067755, -118.383496, False),  # Tagine Beverly Hills
    172: (34.071794, -118.358061, True),   # The Cheesecake Factory - branch may vary
    173: (34.045360, -118.236221, True),   # Alfred Coffee - branch may vary
    174: (34.076293, -118.357190, False),  # Della Terra
    175: (34.072250, -118.357371, False),  # Alma Cocina de Mexico
    176: (34.071264, -118.356533, False),  # Nordstrom Ebar at The Grove
    177: (34.146173, -118.131210, False),  # Annapurna Grill
    178: (34.020945, -118.402098, False),  # Annapurna Cuisine
    179: (34.048431, -118.240732, False),  # SomiSomi - Little Tokyo
    180: (32.872096, -117.213358, False),  # True Food Kitchen - Westfield UTC
    181: (32.870485, -117.212483, False),  # Wushiland Boba - Westfield UTC
    182: (32.870382, -117.212040, False),  # Shake Shack - Westfield UTC
    183: (32.871803, -117.212958, False),  # La Colombe - Westfield UTC
    184: (38.910182, -77.064611, False),   # Tatte Bakery & Cafe - Georgetown
    185: (38.904910, -77.063660, False),   # Clyde's of Georgetown
    186: (38.901804, -77.059746, False),   # Founding Farmers Fishers & Bakers
    187: (38.904768, -77.065150, False),   # Osteria Mozza - Georgetown
    188: (38.908305, -77.063992, False),   # Boulangerie Christophe
    189: (38.915532, -77.067805, False),   # Otto Neo Mediterranean
    190: (40.733519, -73.993502, False),   # Blank Street Coffee - University Place
    191: (40.733782, -74.000652, False),   # Fonty's Deli + Dukaan
    192: (32.847012, -117.273786, False),  # Puesto La Jolla
    193: (45.211152, -123.198929, False),  # Dutch Bros Coffee - NE 5th St
    194: (34.047070, -118.256634, False),  # Bottega Louie - DTLA
    195: (34.034378, -118.283583, False),  # Ebaes - University Park
    196: (34.034334, -118.283652, False),  # Nature's Brew
    197: (34.032087, -118.284331, False),  # QWENCH Juice Bar - University Park
    198: (33.961852, -118.370379, False),  # Randy's Donuts - Inglewood flagship
}

GOOGLE_QUERIES = {
    28: "Dorado Tacos & Quesadillas, 28 E 12th St, New York, NY 10003",
    54: "Merci Market, 59 5th Ave, New York, NY 10003",
    73: "Rancho Tequileria, 741 9th Ave, New York, NY 10019",
    76: "Norma Gastronomia Siciliana, 438 3rd Ave, New York, NY 10016",
    106: "Taboonette, 30 E 13th St, New York, NY 10003",
}

with open("geocoded.json") as f:
    geocoded_by_id = {p["id"]: p for p in json.load(f)}

with open("data_source.json") as f:
    places = json.load(f)

out = []
for display_id, p in enumerate(places, start=1):
    if p["id"] in MANUAL:
        lat, lng, approx = MANUAL[p["id"]]
    elif p["id"] in geocoded_by_id and geocoded_by_id[p["id"]]["lat"] is not None:
        geocoded = geocoded_by_id[p["id"]]
        lat, lng, approx = geocoded["lat"], geocoded["lng"], False
    else:
        raise SystemExit(f"No coordinates for {p['name']} (id {p['id']})")
    out.append({
        # Display id is sequential; MANUAL/GOOGLE_QUERIES stay keyed by the
        # stable "id" in data_source.json.
        "id": display_id,
        "name": p["name"],
        "cuisine": p["cuisine"],
        "category": p["category"],
        "region": p.get("region", "nyc"),
        "location": p.get("location", "New York City"),
        "mapQuery": GOOGLE_QUERIES.get(
            p["id"],
            p["query"] if p.get("region") not in (None, "nyc") else None,
        ),
        "lat": round(lat, 6),
        "lng": round(lng, 6),
        "approx": approx,
    })

with open("data.js", "w") as f:
    f.write("// Auto-generated by build_data.py — edit coordinates here if a pin looks off\n")
    f.write("const PLACES = ")
    f.write(json.dumps(out, indent=2, ensure_ascii=False))
    f.write(";\n")

print(f"Wrote data.js with {len(out)} places ({sum(1 for o in out if o['approx'])} approximate)")
