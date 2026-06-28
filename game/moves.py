STANCE = "orthodox"

MOVES = {
    1: {
        "name": "Jab",
        "display": "1 — Jab",
        "hand": "left",
        "target": "head",
        "color": (0, 255, 0),
    },
    2: {
        "name": "Cross",
        "display": "2 — Cross",
        "hand": "right",
        "target": "head",
        "color": (0, 200, 255),
    },
    3: {
        "name": "Lead Hook",
        "display": "3 — Lead Hook",
        "hand": "left",
        "target": "head",
        "color": (255, 100, 0),
    },
    4: {
        "name": "Rear Hook",
        "display": "4 — Rear Hook",
        "hand": "right",
        "target": "head",
        "color": (255, 50, 50),
    },
    5: {
        "name": "Lead Uppercut",
        "display": "5 — Lead Uppercut",
        "hand": "left",
        "target": "head",
        "color": (180, 0, 255),
    },
    6: {
        "name": "Rear Uppercut",
        "display": "6 — Rear Uppercut",
        "hand": "right",
        "target": "head",
        "color": (220, 0, 255),
    },
}

COMBOS = {
    "Double Jab":           [1, 1],
    "Jab Cross":            [1, 2],
    "Jab Cross Hook":       [1, 2, 3],
    "Jab Cross Lead Hook Rear Hook": [1, 2, 3, 4],
}

DIFFICULTY = {
    "easy":   3.0,
    "medium": 2.0,
    "hard":   1.2,
}