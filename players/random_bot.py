from players.player import Player
from random import randint, getrandbits
from engine.standard_uno_config import COLORS

class RandomBot(Player):
    """
    An extremely rudimentary bot that makes a random move each turn.
    """
    def __init__(self, name):
        Player.__init__(self, name)

    def select_card(self, discard_top):
        """
        Returns a random card or 'd' for draw.
        """
        while True:
            selection = randint(0, len(self.hand))

            if selection == len(self.hand):
                selection = 'd'
                break
            elif self.hand[selection].playable_on(discard_top):
                selection = self.play_card(selection)
                break
            else:
                continue
            
        return selection
    
    def select_color(self):
        """
        Returns a random color for a wild card.
        """
        selection = randint(0, len(COLORS) - 1)

        return COLORS[selection]
    
    def select_renege(self, drawn_card):
        """
        Returns a random response to decide if the player would like to play the valid card they just drew.
        """
        return not getrandbits(1)
    
    def challenge_select(self):
        """
        Returns a random boolean to decide if the player accepts the challenge.
        """
        return not getrandbits(1)