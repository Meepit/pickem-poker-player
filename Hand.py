import cv2
from Screen import Screen
import pytesseract
from pytesseract import image_to_string


class Hand(object):
    def __init__(self, screen):
        self.screen = screen
        self._cards = screen.get_card_locations(screen.screen)

    def get_cards(self):
        return [self._cards["card{0}".format(i)]["coord"] for i in range(1, 5)]

    def get_card_coord(self, card_num):
        try:
            return self.cards["card{0}".format(card_num)]
        except KeyError:
            print("Invalid card, card_num must be an integer between 1-4 inclusive")

    def set_card_value(self, card_num, rank, suit):
        if card_num not in range(1, 5):
            raise ValueError('card_num must be an integer between 1-4 inclusive')
        self._cards["card{0}".format(card_num)]["rank"] = rank
        self._cards["card{0}".format(card_num)]["suit"] = suit

    def get_rank(self, card_num):
        if card_num not in range(1, 5):
            raise ValueError('card_num must be an integer between 1-4 inclusive')
        # Rank makes up about 27% of the card, suit makes up about 25%
        coords = self.get_card_coord(card_num)
        rank_offset = int((coords[3] - coords[1]) * 0.27)
        rank = ImageGrab.grab((x1, y1, x1 + rank_offset, y1 + rank_offset))
        rank = rank.convert("1")  # Convert to black/white for better detection.
        rank_str = image_to_string(rank, config='-psm 10000 -c tessedit_char_whitelist=0123456789JQKA')
        if rank_str == "10":
            rank_str = "T"
        if len(rank_str) == 0 or len(rank_str) > 1:
            print("There was a problem detecting rank. Detected as {0}. Retrying".format(rank_str))
            time.sleep(1)
            return self.get_rank(card_num)
        return rank_str

