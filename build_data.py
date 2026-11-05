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
    199: (45.210263, -123.198197, False),  # Wildwood Cafe
    200: (45.214079, -123.198747, False),  # Sushi Ninja
    201: (45.207767, -123.198265, False),  # Baker St Cafe - Thai Kitchen
    202: (40.739591, -73.995570, False),   # Guac Time Mexican Grill - Chelsea
    203: (40.667095, -73.981225, False),   # The Soup Bowl of Park Slope
    204: (40.758835, -73.978814, False),   # Madras Dosa Company - Rockefeller Center
    205: (40.726860, -73.987650, False),   # Malai Marke Indian Cuisine
    206: (40.728874, -74.001004, False),   # Hello Saigon Restaurant
    207: (40.764161, -73.988100, False),   # Bombay Grill House - Hell's Kitchen
    208: (40.770108, -73.991856, False),   # White Noise Coffee - Hell's Kitchen
    209: (40.761780, -73.994302, False),   # Coffee T Bagels - Hell's Kitchen
    210: (40.761756, -73.989791, False),   # Elephant Ear Thai Eatery
    211: (40.759846, -73.991369, False),   # Gregory's Coffee - Hell's Kitchen
    212: (40.759114, -73.991914, False),   # Grind The NYC Coffee Shop
    213: (40.756007, -73.994171, False),   # Cafe Aroma - Hell's Kitchen
    214: (40.756771, -73.989841, False),   # Bluestone Lane - Times Square
    215: (27.943259, -82.446635, False),   # Shortwave Coffee - Sparkman Wharf
    216: (27.960024, -82.435229, False),   # Columbia Restaurant - Ybor City
    217: (27.945990, -82.526437, False),   # Curry Leaves Indian Cuisine - Westshore Plaza
    218: (40.763522, -73.992424, False),   # Rice X Beans - Hell's Kitchen
    219: (40.758474, -73.928820, False),   # Koukla Espresso Bar - Astoria
    220: (40.756949, -73.998026, False),   # The Gyro Project - Hudson Yards
    221: (40.758861, -73.989869, False),   # The Stinger Cocktail Bar & Kitchen
    222: (39.199840, -85.925248, False),   # Upland Brewing Company - Columbus IN
    223: (39.202298, -85.922284, False),   # Taku Steakhouse
    224: (39.204214, -85.920947, False),   # Thai Connection
    225: (39.203080, -85.921323, False),   # Fresh Take Kitchen
    226: (39.203022, -85.922147, False),   # Lucabe Coffee Co - downtown
    227: (39.202161, -85.921988, False),   # Yats
    228: (39.222743, -85.902050, False),   # Marco's Pizza - 25th St
    229: (39.222853, -85.887871, False),   # Pho Shiki
    230: (39.201910, -85.921460, False),   # Winnie Tea Bar - downtown
    231: (39.214589, -85.880523, False),   # Yummy Bowl
    232: (39.223498, -85.877959, False),   # E Sushi
    233: (39.229381, -85.900221, False),   # Fazoli's
    234: (39.223163, -85.915107, False),   # Olesya's Kitchen
    235: (39.220906, -85.887644, False),   # Panera Bread
    236: (39.223147, -85.915318, False),   # Le Fernandez Cafe
    237: (39.200843, -85.920796, False),   # Masala Magic - 217 Washington St Ste A
    238: (39.767960, -86.159673, False),   # Buca di Beppo - Indianapolis
    239: (40.725937, -74.001416, False),   # Vesuvio Bakery - SoHo
    240: (40.742094, -73.982686, False),   # Kailash Parbat - Kips Bay
    241: (40.767574, -73.993169, False),   # Afficionado Coffee Roasters - Hell's Kitchen
    242: (40.711576, -73.957803, False),   # L'industrie Pizza - Williamsburg
    243: (40.720329, -73.996756, False),   # Cafe Roma - Little Italy
    244: (40.694578, -73.994254, False),   # Khaosan - Brooklyn Heights
    245: (40.759561, -73.826211, False),   # Morning Bakery - Flushing Chinatown
    246: (40.768828, -73.988559, False),   # Rex Coffee - Hell's Kitchen
    247: (40.760849, -73.988969, False),   # Frisson Espresso - Hell's Kitchen
    248: (40.724992, -74.003233, False),   # Piccola Cucina Osteria - SoHo
    249: (40.717878, -73.990789, False),   # Dirt Candy - Lower East Side
    250: (38.915281, -77.067738, False),   # Caspian Crust - Georgetown
    251: (38.911496, -77.032357, False),   # Rice Market - Logan Circle
    252: (38.903372, -77.064724, False),   # Grace Street Coffee Roasters - Georgetown
    253: (40.729318, -73.998320, False),   # Spicy Moon - West Village (68 W 3rd St)
    254: (40.731804, -73.958127, False),   # Chinta Thai - Greenpoint
    255: (40.732664, -73.985162, False),   # Saperavi - East Village (245 E 14th St)
    256: (40.753881, -73.984932, False),   # Breads Bakery - Bryant Park (1080 6th Ave)
    257: (40.753751, -73.983543, True),    # Toastieland - Bryant Park Winter Village stall
    258: (40.765524, -73.991575, False),   # Il Melograno - Hell's Kitchen
    259: (40.743124, -74.009142, False),   # Ammi - Market 57, Pier 57
    260: (40.743365, -74.009234, False),   # Good to Go by JBF - Market 57, Pier 57
    261: (40.754595, -73.999390, False),   # Russ & Daughters - Hudson Yards (502 W 34th St)
    262: (29.716252, -95.414832, False),   # Hamsa - Rice Village, Houston
    263: (29.744721, -95.383522, False),   # Soto - Montrose, Houston
    264: (29.735472, -95.418788, False),   # Verandah - Kirby Collection, Houston
    265: (29.736785, -95.418622, False),   # Carrabba's - The Original on Kirby, Houston
    266: (29.272466, -94.818496, False),   # Grotto - San Luis Resort, Galveston
    267: (29.307134, -94.782913, False),   # The Sunflower Bakery & Cafe - Galveston
    268: (30.257075, -97.739324, False),   # Salvation Pizza - Rainey St, Austin
    269: (30.258702, -97.738691, False),   # Little Lucy's - Rainey St, Austin
    270: (30.263615, -97.743904, False),   # Fareground - One Eleven Congress, Austin
    271: (30.262727, -97.743688, False),   # Alfred Coffee - The LINE Austin
    272: (30.256425, -97.738871, False),   # Cuvée Coffee - Natiivo lobby, Rainey St, Austin
    273: (30.261574, -97.724348, False),   # Tamale House East - East 6th St, Austin
    274: (30.316147, -97.708497, False),   # Foodpath Indian Cuisine - North Loop, Austin
    275: (30.308018, -97.750483, False),   # Kerbey Lane Cafe - Central (original), Austin
}

GOOGLE_QUERIES = {
    28: "Dorado Tacos & Quesadillas, 28 E 12th St, New York, NY 10003",
    54: "Merci Market, 59 5th Ave, New York, NY 10003",
    73: "Rancho Tequileria, 741 9th Ave, New York, NY 10019",
    76: "Norma Gastronomia Siciliana, 438 3rd Ave, New York, NY 10016",
    106: "Taboonette, 30 E 13th St, New York, NY 10003",
    # Exact suite address — business name may not resolve in Google Maps
    237: "217 Washington St Ste A, Columbus, IN 47201",
    # Multi-branch chains — pin the specific branch visited
    246: "REX, 864 10th Ave, New York, NY 10019",
    247: "Frisson Espresso, 326 W 47th St, New York, NY 10036",
    248: "Piccola Cucina Osteria, 196 Spring St, New York, NY 10012",
    253: "Spicy Moon, 68 W 3rd St, New York, NY 10012",
    255: "Saperavi, 245 E 14th St, New York, NY 10003",
    256: "Breads Bakery, 1080 6th Ave, New York, NY 10036",
    257: "Bank of America Winter Village at Bryant Park, New York, NY 10018",
    259: "Ammi, 25 11th Ave, New York, NY 10011",
    260: "Good To Go by JBF, 25 11th Ave, New York, NY 10011",
    261: "Russ & Daughters, 502 W 34th St, New York, NY 10001",
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
    entry = {
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
    }
    if p.get("michelin"):
        entry["michelin"] = p["michelin"]
    out.append(entry)

with open("data.js", "w") as f:
    f.write("// Auto-generated by build_data.py — edit coordinates here if a pin looks off\n")
    f.write("const PLACES = ")
    f.write(json.dumps(out, indent=2, ensure_ascii=False))
    f.write(";\n")

print(f"Wrote data.js with {len(out)} places ({sum(1 for o in out if o['approx'])} approximate)")
