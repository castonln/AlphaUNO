class Card:
    def __init__(self, color, value):
        self.color = color
        self._value = value

    def __str__(self):
        return self.color + ' ' + self._value
    
    def playable_on(self, other_card):
        """
        Returns if card can be played on top of other_card.
        """
        return self.color == other_card.color or self._value == other_card._value or self.color == 'Black' or other_card.color == 'Black'
        # final statement is added for flexibility (shouldn't be possible)
