from engine.card import Card
from random import shuffle
from engine.exceptions import NotEnoughCardsException
from engine.standard_uno_config import *

class Deck:
    def __init__(self):
        self._build_deck()
        self.discard_deck = []

    def __len__(self):
        return len(self.cards) + len(self.discard_deck)

    def _build_deck(self):
        """
        Creates a standard 108 card UNO deck and returns it as a shuffled (random) list of card objects.
        """
        self.cards = []
        
        for current_color in COLORS:
            for _ in range(2):

                # 1-9 Numbered Cards
                for i in range(9):
                    self.cards.append(Card(color = current_color, value = f'{i + 1}'))

                # Action Cards
                for card_type in ACTIONCARDS:
                    self.cards.append(Card(color = current_color, value = card_type))

            # One 0 per color
            self.cards.append(Card(color = current_color, value = '0'))

        # Four Wilds, four Wild +4s
        for i in range(4):
            self.cards.append(Card(color = 'Black', value = 'Wild'))
            self.cards.append(Card(color = 'Black', value = 'Wild +4'))
        
        shuffle(self.cards)

    def append(self, value):
        self.cards.append(value)

    def extend(self, value):
        self.cards.extend(value)

    def append_discard(self, value):
        """
        Append the given card to the discard_deck.
        """
        # Reset black cards
        if value._value == 'Wild':
            value_copy = Card(value='Wild', color='Black')
        elif value._value == 'Wild +4':
            value_copy = Card(value='Wild +4', color='Black')
        else:
            value_copy = value
        self.discard_deck.append(value_copy)

    def pop(self, index=-1):
        """
        Tries to pop(index) and replaces with shuffled discard_deck if length is 0.
        If both lengths are 0, the game cannot be played with only one deck.
        """
        try:
            return self.cards.pop(index)
        except IndexError:
            self._swap_decks()
            try:
                return self.cards.pop(index)
            except IndexError:
                raise NotEnoughCardsException()

    def _swap_decks(self):
        """
        Replaces self.cards with the discard_deck.
        """
        self.cards.extend(self.discard_deck)
        shuffle(self.cards)
        self.discard_deck.clear()