class Player:
    """
    Handles a player's actions.
    """
    def __init__(self, name):
        self._name = name
        self.hand = []

    def __str__(self):
        return self._name

    def draw_card(self, deck):
        """
        Draws one card and returns it.
        """
        drawn_card = deck.pop()
        self.hand.append(drawn_card)
        return drawn_card

    def play_card(self, index = -1):
        """
        Plays card from hand given its index. If no index is given, the last card appended is played.
        """
        return self.hand.pop(index)