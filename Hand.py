from Screen import Screen


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
        if card_num not in range(1,5):
            raise ValueError('card_num must be an integer between 1-4 inclusive')
        self._cards["card{0}".format(card_num)]["rank"] = rank
        self._cards["card{0}".format(card_num)]["suit"] = suit
