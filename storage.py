from locations import balcony, basement, forest, room, sport_ground, street, swamp, first_aid_station

users = {}

locations = {
    "room": {

    },
    "street": {

    },
    "balcony": {

    },
    "basement": {

    },
    "forest": {

    },
    "swamp": {

    },
    'first_aid_station': {

    }
}

rooms = {
    3: (304, 307, 312, 314, 315, 316, 317, 318, 333, 321, 322, 323, 327, 329, 330, 332),
    4: (402, 403, 404, 405, 415, 407, 408, 409, 410, 411, 412, 413, 414, 406, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 431, 432, 433, 430)
}

modules = {
    "room": room,
    "balcony": balcony,
    "street": street,
    "basement": basement,
    "swamp": swamp,
    "forest": forest,
    "sport_ground": sport_ground,
    'first_aid_station': first_aid_station
}

paths = {
    "room": [],
    "street": [],
    "balcony": ["room"],
    "basement": []
}
