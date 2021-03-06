import cv2
from Screen import Screen
from Suits import Suits
import pytesseract
from pytesseract import image_to_string
import time
from PIL import ImageGrab
import os


class Hand(object):
    def __init__(self, screen):
        self.screen = screen
        self._cards = screen.get_card_locations(screen.screen)
        self.suits = Suits

    def get_hand(self):
        """
        Return string representation of hand
        :return: str
        """
        str = ""
        for i in range(1, 5):
            str += self._cards["card{0}".format(i)]["rank"] + self._cards["card{0}".format(i)]["suit"] + " "
        return str

    def get_card_coord(self, card_num):
        """
        Returns coordinates of a card
        :param card_num: Number between 1 and 4 inclusive.
        :return: tuple of coordinates.
        """
        try:
            return self._cards["card{0}".format(card_num)]["coord"]
        except KeyError:
            print("Invalid card, card_num must be an integer between 1-4 inclusive")

    @staticmethod
    def validate_card_num(card_num):
        if card_num not in range(1, 5):
            raise ValueError('card_num must be an integer between 1-4 inclusive')

    def set_card_rank(self, card_num, rank):
        self.validate_card_num(card_num)
        self._cards["card{0}".format(card_num)]["rank"] = rank

    def set_card_suit(self, card_num, suit):
        self.validate_card_num(card_num)
        self._cards["card{0}".format(card_num)]["suit"] = suit

    def get_card_rank(self, card_num):
        self.validate_card_num(card_num)
        try:
            return self._cards["card{0}".format(card_num)]["rank"]
        except KeyError:
            print("Card {0} has no rank set".format(card_num))

    def get_card_suit(self, card_num):
        self.validate_card_num(card_num)
        try:
            return self._cards["card{0}".format(card_num)]["suit"]
        except KeyError:
            print("Card {0} has no suit set".format(card_num))

    def get_ranks_and_suits(self):
        for i in range(1, 5):
            rank = self.determine_rank(i)
            self.set_card_rank(i, rank)
            suit = self.determine_suit(i)
            self.set_card_suit(i, suit)

    def determine_rank(self, card_num):
        """
        Uses tesseract OCR to detect the rank of a card. Retries if invalid detection.
        :param card_num: int, card number between 1-4 inclusive.
        :return: rank_str, a string of the rank.
        """
        self.validate_card_num(card_num)
        # Rank makes up about 27% of the card, suit makes up about 25%
        coords = self.get_card_coord(card_num)
        x1, y1, x2, y2 = coords
        rank_offset = int((coords[3] - coords[1]) * 0.27)
        rank = ImageGrab.grab((x1, y1, x1 + rank_offset, y1 + rank_offset))
        rank = rank.convert("1")  # Convert to black/white for better detection.
        rank_str = image_to_string(rank, config='-psm 10000 -c tessedit_char_whitelist=0123456789JQKA')
        if rank_str == "10":
            rank_str = "T"
        if rank_str == "0":
            rank_str = "Q"
        if len(rank_str) == 0 or len(rank_str) > 1:
            print("There was a problem detecting rank. Detected as {0}. Retrying".format(rank_str))
            time.sleep(1)
            return self.determine_rank(card_num)
        return rank_str

    def determine_suit(self, card_num):
        """
        Captures image of suit, resizes and compares filesize to predefined sizes to determine suit.
        :param card_num:  int, card number between 1-4 inclusive.
        :return: string character in [H,S,C,D] representing card suit.
        """
        self.validate_card_num(card_num)
        coords = self.get_card_coord(card_num)
        suit_offset = int((coords[3] - coords[1]) * 0.25)
        x1, y1, x2, y2 = coords
        suit = ImageGrab.grab((x1, y1 + suit_offset, x1 + suit_offset, y1 + (suit_offset * 2)))
        pixel_colour = suit.getpixel((suit_offset // 2, suit_offset // 2))
        suit = suit.convert("L")
        suit = suit.resize((30, 30))
        suit_filename = "screen" + str(self.screen.screen_num) + "_card" + str(card_num) + ".png"
        suit.save("detections/" + suit_filename)
        suit_filesize = os.stat("detections/" + suit_filename).st_size
        if pixel_colour[0] > 165:  # red suit
            abs_diff_diamond = abs(suit_filesize - self.suits["diamond"])
            abs_diff_heart = abs(suit_filesize - self.suits["heart"])
            return "D" if abs_diff_diamond < abs_diff_heart else "H"
        else:  # black suit
            abs_diff_spade = abs(suit_filesize - self.suits["spade"])
            abs_diff_club = abs(suit_filesize - self.suits["club"])
            if self.get_card_rank(card_num) == "Q":  # Bottom part of Queen clips into suit causing misdetection.
                abs_diff_spade = abs(suit_filesize - self.suits["q_spade"])
            return "C" if abs_diff_club < abs_diff_spade else "S"

    def get_cards_status(self):
        """
        Checks the pixel colour of the tops of all cards, if white and if no middle card then cards are ready.
        :param img: PIL image object containing entire screen.
        :return: ready, bool
        """
        img = ImageGrab.grab()
        ready = False
        for i in range(1, 5):
            coord = self.get_card_coord(i)
            pixel_colour = img.getpixel((coord[0] + 55, coord[1] + 2))
            if pixel_colour[0] > 240 and pixel_colour[1] > 240 and pixel_colour[2] > 240:
                ready = True
            else:
                ready = False
        if img.getpixel((self.get_card_coord(2)[2] + 50, self.get_card_coord(2)[1] + 50))[0] > 25:
            ready = False
        return ready