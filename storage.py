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
        "usersData" : {}, 
        "locationImages" : {
            0 : open("assets/basement.png"), 
            1 : open("assets/ping-pong.png"), 
            2 : open("assets/ping-pong.png"), 
            3 : open("assets/ping-pong.png"), 
            4 : open("assets/ping-pong.png"), 
            5 : open("assets/ping-pong.png"), 
            6 : open("assets/shop.png")
        }

    },
    "forest": {

    },
    "swamp":{

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
    "forest" : forest,
    "sport_ground": sport_ground
}

paths = {
    "room": [],
    "street": [],
    "balcony": ["room"],
    "basement": []
}