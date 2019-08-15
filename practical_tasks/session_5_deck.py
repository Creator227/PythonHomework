import random
cards_set = {('Hearts', 'Six'), ('Hearts', 'Seven'), ('Hearts', 'Eight'), ('Hearts', 'Nine'), ('Hearts', 'Ten'),
             ('Hearts', 'Jack'), ('Hearts', 'Queen'), ('Hearts', 'King'), ('Hearts', 'Ace'),
             ('Diamonds', 'Six'), ('Diamonds', 'Seven'), ('Diamonds', 'Eight'), ('Diamonds', 'Nine'), ('Diamonds', 'Ten'),
             ('Diamonds', 'Jack'), ('Diamonds', 'Queen'), ('Diamonds', 'King'), ('Diamonds', 'Ace'),
             ('Spades', 'Six'), ('Spades', 'Seven'), ('Spades', 'Eight'), ('Spades', 'Nine'), ('Spades', 'Ten'),
             ('Spades', 'Jack'), ('Spades', 'Queen'), ('Spades', 'King'), ('Spades', 'Ace'),
             ('Clubs', 'Six'), ('Clubs', 'Seven'), ('Clubs', 'Eight'), ('Clubs', 'Nine'), ('Clubs', 'Ten'),
             ('Clubs', 'Jack'), ('Clubs', 'Queen'), ('Clubs', 'King'), ('Clubs', 'Ace')}


class Card:

    def __init__(self, card_type, card_value):
        if (card_type, card_value) not in cards_set:
            raise TypeError('Cards names must be standart!')
        self._card_type, self._card_value = card_type, card_value
        self._card_data = (self.card_type, self.card_value)

    @property
    def card_type(self):
        return self._card_type

    @property
    def card_value(self):
        return self._card_value

    def __repr__(self):
        return 'type: {0}, value: {1}'.format(self.card_type, self.card_value)


class Deck:

    def __init__(self):
        self.cards = list(cards_set)

    def add_card(self, card):
        if card not in self.cards:
            self.cards.append(card)

    def __contains__(self, item: Card):
        return True if item._card_data in self.cards else False

    def get_card(self, card: Card):
        return Card(*self.cards.pop(self.cards.index(card._card_data))) if card in self else None

    def shuffle_cards(self):
        n = len(self.cards) - 1
        for i in range(25):
            c = random.randint(0, n)
            self.cards[c], self.cards[-c] = self.cards[-c], self.cards[c]

    def __repr__(self):
        mess = 'Cards Deck: \n'
        j = 0
        for i in self.cards:
            mess += ' '.join(i)
            mess += '\t'
            j += 1
            if not j % 6:
                mess += '\n'
        return mess

    def cards_num(self):
        return len(self.cards)
