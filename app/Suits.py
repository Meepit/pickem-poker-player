import os

Suits = {
    "club": os.stat('suits/club.png').st_size,
    "spade": os.stat("suits/spade.png").st_size,
    "q_spade": os.stat("suits/queen_spade.png").st_size,
    "heart": os.stat("suits/heart.png").st_size,
    "diamond": os.stat("suits/diamond.png").st_size,
    }