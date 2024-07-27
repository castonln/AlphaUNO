from players.player import Player
from random import randint, getrandbits
from engine.standard_uno_config import COLORS

class WildLastBot(Player):
    """
    A bot that saves its wild cards for last, granting them freedom in the late game.
    """
    def __init__(self, name):
        Player.__init__(self, name)

    def select_card(self, discard_top):
        """
        Returns a valid card or 'd' for draw. Excludes wild cards unless player has "UNO."
        """
        has_uno = len(self.hand) == 1
        
        # Create a list, valid_selections, of tuples.
        # Tuples are (index, card), so that tuple[0] gives the self.hand index of tuple[1]
        # Tuples are only appended if they are playable.
        valid_selections = []
        for index, card in enumerate(self.hand):
            if card.playable_on(discard_top):
                valid_selections.append((index, card))

        if valid_selections and has_uno:
            # Special case where we play the valid card no matter what.
            selection = self.play_card(valid_selections[0][0]) # first (and only) tuple in valid_selections - first index of the tuple is the index of the card

        elif valid_selections:
            # Count our normal cards.
            non_wilds = [selection for selection in valid_selections if selection[1].color != 'Black']

            # Did we count any?
            if non_wilds:
                selection = self.play_card(non_wilds[randint(0, len(non_wilds) - 1)][0]) # random tuple in non_wilds - first index of the tuple is the index of the card

            # We have no non-wilds available. How many wild cards do we have?
            # Do we have more than one? We can still save one for later.
            elif len(valid_selections) > 1:
                selection = self.play_card(valid_selections[randint(0, len(valid_selections) - 1)][0]) # random tuple in valid_selections - first index of the tuple is the index of the card
            # If we only have one wild or no wilds, there's nothing to do but draw.
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
        If the drawn card is wild, return false. Otherwise, return true.
        """
        return not drawn_card.color == 'Black'
    
    def challenge_select(self):
        """
        Returns a random boolean to decide if the player accepts the challenge.
        """
        return not getrandbits(1)