from players.player import Player
from random import getrandbits, choice
from engine.standard_uno_config import COLORS

class WildFirstBot(Player):
    """
    A bot that plays its wild cards first.
    """
    def __init__(self, name):
        Player.__init__(self, name)

    def select_card(self, discard_top):
        """
        Returns a valid card or 'd' for draw. Favors wild cards first.
        """
        # Create a list, valid_selections, of tuples.
        # Tuples are (index, card), so that tuple[0] gives the self.hand index of tuple[1]
        # Tuples are only appended if they are playable.
        valid_selections = []
        for index, card in enumerate(self.hand):
            if card.playable_on(discard_top):
                valid_selections.append((index, card))

        if valid_selections:
            wilds = [selection for selection in valid_selections if selection[1].color == 'Black']

            if wilds:
                selection = self.play_card(wilds[0][0])

            elif len(valid_selections) > 0:
                selection = self.play_card(choice(valid_selections)[0])

            else:
                selection = 'd'
            
        else:
            selection = 'd'
            
        return selection
    
    def select_color(self):
        """
        Returns an advantageous color for a wild card.
        """
        color_counts = {color : 0 for color in COLORS}
        for card in self.hand:
            if card.color != 'Black':
                color_counts[card.color] += 1

        selection = max(color_counts, key=color_counts.get)

        return selection
    
    def select_renege(self, drawn_card):
        """
        Renege if possible.
        """
        return True
    
    def challenge_select(self):
        """
        Returns a random boolean to decide if the player accepts the challenge.
        """
        return not getrandbits(1)