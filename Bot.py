from Hand import Hand
from Screen import Screen
import requests
from PIL import ImageGrab
import time


class Bot(object):
    def __init__(self, hand, screen, q):
        self._screen = screen
        self._hand = hand
        self.deal_button = screen.get_deal_button(hand._cards)
        self._queue = q

    def build_url(self):
        """
        Return url using ranks and suits from self._hand
        :return: url, a string that can be used to make an API request
        """
        ranks = '23456789tjqka'
        suits = 'hsdc'
        output = []
        url_suffix = '&game=0&payouts=1200%20239.8%20120%2018%2015%2011%205%203%202'
        for i in range(1, 5):
            prefix = str(ranks.index(self._hand.get_card_rank(i).lower()) + 13 * suits.index(self._hand.get_card_suit(i).lower()))
            output.append(prefix)
        return 'http://www.beatingbonuses.com/pick_exec.php?player=' + "%20".join(output) + url_suffix

    def calculate_action(self):
        url = self.build_url()
        try:
            r = requests.get(url)
        except(requests.ConnectionError, requests.Timeout):
            print("Connection issue, retrying.")
            return self.calculate_action()
        evs = r.text.split(" ")
        return 3 if float(evs[0]) > float(evs[1]) else 4

    def add_to_queue(self, card=0, coord=()):
        """
        Adds a coordinate to the queue representing area to be clicked.
        :param coord: optional tuple of coordinates to add to queue.
        :param card: Card to add to queue [3,4]
        :return: None
        """
        if coord:
            self._queue.put(coord)
            return
        if card == 3:
            location = self.hand.get_card_coord(3)
            self._queue.put((location[0] + 20, location[1] + 20))
        elif card == 4:
            location = self.hand.get_card_coord(4)
            self._queue.put((location[0] + 20, location[1] + 20))

    def start(self):
        while True:
            # Get deal button
            deal_button_xy = self._screen.deal_button
            deal_button = ImageGrab.grab((deal_button_xy[0], deal_button_xy[1], deal_button_xy[0] + 3, deal_button_xy[1] +3))
            deal_button_pixel_colour = deal_button.getpixel((2, 2))[0]
            if deal_button_pixel_colour <= 250:
                print("\tWaiting for deal button..")
            while not deal_button.getpixel((2, 2))[0] >= 200:  # Deal button not ready
                deal_button = ImageGrab.grab((deal_button_xy[0], deal_button_xy[1], deal_button_xy[0] + 3, deal_button_xy[1] + 3))
            self.add_to_queue(coord=self._screen.deal_button)
            # end deal button section
            img = ImageGrab.grab()
            print("Waiting for cards")
            while not self._hand.get_cards_status():
                pass
            time.sleep(0.5)  # failsafe
            # get card ranks and suits
            for i in range(1, 5):
                rank = self._hand.determine_rank(i)
                self._hand.set_card_rank(i, rank)
                suit = self._hand.determine_suit(i)
                self._hand.set_card_suit(i, suit)
            print(self._hand.get_hand())
            action = self.calculate_action()
            self.add_to_queue(card=action)
            print("Choosing {0}".format(action))




screen = Screen(1)
hand = Hand(screen)
bot = Bot(hand, screen, "q")
