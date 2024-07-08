import json
DEFAULT_BUTTONS = ["/locations", "/stats"]

try:
    with open('save.json', 'r', encoding='utf-8') as f:
        load = json.load(f)
        users = load[0]
        locations = load[1]
except:
    users = {}
    locations = {
        "room": {
            "usersData": {}
        },
        "balcony": {
            "usersData": {}
        },
        "basement": {
            "usersData": {},
            "StoreOffers": {
                #OffererId: [[itemName, costValue(cookies)], ...]
                "-1" : []
            }
        },
        "forest": {
            "usersData": {

            }
        },
        "swamp": {
            "usersData": {}
        },
        "choice": {
            "usersData": {}
        },
        "eatery": {
            "usersData": {}
        },
        "sport_ground": {
            "players": []
        },
        'first_aid_station': {
            "usersData": {}
        }
    }




rooms = {
    3: (304, 307, 312, 314, 315, 316, 317, 318, 333, 321, 322, 323, 327, 329, 330, 332),
    4: (402, 403, 404, 405, 415, 407, 408, 409, 410, 411, 412, 413, 414, 406, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 431, 432, 433, 430)
}
