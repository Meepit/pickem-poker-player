from Hand import Hand
from Screen import Screen


class Bot(object):
    def __init__(self, hand, screen):
        self._screen = screen
        self._hand = hand
        self.deal_button = screen.get_deal_button(hand._cards)

    def build_url(self):
        ranks = '23456789tjqka'
        suits = 'hsdc'
        output = []
        url_suffix = '&game=0&payouts=1200%20239.8%20120%2018%2015%2011%205%203%202'
        for i in range(1, 5):
            prefix = str(ranks.index(self._hand.get_card_rank(i).lower()) + 13 * suits.index(self._hand.get_card_suit(i).lower()))
            output.append(prefix)
        return 'http://www.beatingbonuses.com/pick_exec.php?player=' + "%20".join(output) + url_suffix

screen = Screen(1)
hand = Hand(screen)
bot = Bot(hand, screen)
for i in range(1,5):
    rank = hand.determine_rank(i)
    hand.set_card_rank(i, rank)
    suit = hand.determine_suit(i)
    hand.set_card_suit(i, suit)
print(hand.get_hand())
print(bot.build_url())