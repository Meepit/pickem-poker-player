import win32api
from PIL import ImageGrab
import pytesseract
import cv2
import numpy as np


class Screen(object):
    def __init__(self, number, path=""):
        self.screen_num = number
        self._res = (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
        self._x_offset = 0  # Half the horizontal res
        self._y_offset = 0  # Half the vertical res
        self.screen = self.get_screen(number)
        self.deal_button = ()
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
        if path:
            pytesseract.pytesseract.tesseract_cmd = path

    def get_screen(self, section):
        """
        Sets self.image to a PIL Image object of the screen section.
        :param section: Integer 1-4 representing section of screen (top left, top right, bottom left, bottom right)
        :return: None
        """
        if section == 1:
            img = ImageGrab.grab((0, 0, self._res[0] // 2, self._res[1] // 2))
        elif section == 2:
            self._x_offset = self._res[0] // 2
            img = ImageGrab.grab((self._x_offset, 0, self._res[0], self._res[1] // 2))
        elif section == 3:
            self._y_offset = self._res[1] // 2
            img = ImageGrab.grab((0, self._y_offset, self._res[0] // 2, self._res[1]))
        elif section == 4:
            self._x_offset = self._res[0] // 2
            self._y_offset = self._res[1] // 2
            img = ImageGrab.grab((self._x_offset, self._y_offset, self._res[0], self._res[1]))
        return img

    def get_card_locations(self, img):
        """
        :param img: PIL image object
        Convert to cv2 image, using image contours find coordinates of 4 cards and set them.
        :return: Dist of
        """
        print("Getting locations")
        im = np.array(img)
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        card_boxes = []
        for i in contours:
            if cv2.contourArea(i) > 8000:  # TODO: Change this to be dynamic
                card_boxes.append([cv2.contourArea(i), cv2.boundingRect(i)])
                x, y, w, h = cv2.boundingRect(i)
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Card boxes should be the 4 smallest boxes by area, sort by area first then sort by x1 coord
        # Giving coordinates of cards in order.
        card_boxes = sorted(card_boxes)[:4]
        card_boxes = sorted([i[1] for i in card_boxes])
        coords = dict()
        coords["card1"] = {"coord": (self._x_offset + card_boxes[0][0],
                                     self._y_offset + card_boxes[0][1],
                                     self._x_offset + card_boxes[0][0] + card_boxes[0][2],
                                     self._y_offset + card_boxes[0][1] + card_boxes[0][3])}
        coords["card2"] = {"coord": (self._x_offset + card_boxes[1][0],
                                     self._y_offset + card_boxes[1][1],
                                     self._x_offset + card_boxes[1][0] + card_boxes[1][2],
                                     self._y_offset + card_boxes[1][1] + card_boxes[1][3])}
        coords["card3"] = {"coord": (self._x_offset + card_boxes[2][0],
                                     self._y_offset + card_boxes[2][1],
                                     self._x_offset + card_boxes[2][0] + card_boxes[2][2],
                                     self._y_offset + card_boxes[2][1] + card_boxes[2][3])}
        coords["card4"] = {"coord": (self._x_offset + card_boxes[3][0],
                                     self._y_offset + card_boxes[3][1],
                                     self._x_offset + card_boxes[3][0] + card_boxes[3][2],
                                     self._y_offset + card_boxes[3][1] + card_boxes[3][3])}
        self.get_deal_button(coords)
        return coords

    def get_deal_button(self, coords):
        """
        :param coords: Dict, Card coordinates
        :return: Tuple, dealbutton coordinates.
        """
        coord = coords["card3"]["coord"]
        self.deal_button = (coord[0], coord[3] + ((coord[3] - coord[1]) // 3))
