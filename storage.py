from locations import balcony, basement, forest, room, sport_ground, street, swamp

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
    "swamp":{

    }
}

modules = {
    "room": room,
    "balcony": balcony,
    "street": street,
    "basement": basement,
    "swamp": swamp,
    "forest" : forest,
    "sport_ground": sport_ground
}

paths = {
    "room": [],
    "street": [],
    "balcony": ["room"],
    "basement": []
}