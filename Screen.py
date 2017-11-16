import win32api
from PIL import ImageGrab
import pytesseract


class Screen(object):
    def __init__(self, number, path=""):
        self.number = number
        self._res = (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
        self._x_offset = 0
        self._y_offset = 0
        if path:
            pytesseract.pytesseract.tesseract_cmd = path
        else:
            pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

    def get_screen(self, section):
        """
        :param section: Integer 1-4 representing section of screen (top left, top right, bottom left, bottom right)
        :return: image object
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




