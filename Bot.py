from Hand import Hand
from Screen import Screen
import requests


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

    def add_to_queue(self, card):
        """
        Adds a coordinate to the queue representing card to be picked.
        :param card: Card to add to queue [3,4]
        :return: None
        """
        if card == 3:
            location = self.hand.get_card_coord(3)
            self._queue.put((location[0] + 20, location[1] + 20))
        else:
            location = self.hand.get_card_coord(4)
            self._queue.put((location[0] + 20, location[1] + 20))


screen = Screen(1)
hand = Hand(screen)
bot = Bot(hand, screen, "q")
#for i in range(1,5):
#    rank = hand.determine_rank(i)
#    hand.set_card_rank(i, rank)
#    suit = hand.determine_suit(i)
#    hand.set_card_suit(i, suit)
#print(hand.get_hand())
#print(bot.calculate_action())
print(hand.get_cards_status())