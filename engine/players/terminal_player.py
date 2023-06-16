from engine.players.player import Player
from engine.standard_uno_config import COLORS
from engine.terminal_utils import *

class TerminalPlayer(Player):
    """
    A human player who plays with a terminal interface.
    """
    def __init__(self, name):
        Player.__init__(self, name)

    def select_card(self, discard_top):
        """
        Returns the player's selected card or 'd' for draw.
        """
        print(f"\n{STYLE['BOLD']}******* {self}'s Hand *******{STYLE['ENDS']}\n")

        for option, card in enumerate(self.hand):
            print(f"{STYLE['BOLD']} {option:>1d}) {STYLE['ENDS']}" f"{COLORCODE[card.color]}{f'{card}':<20s}{COLORCODE['ENDC']}", end = '')
            if card.playable_on(discard_top):
                print(f"{COLORCODE['MAGENTA']}{'* Valid *'}{COLORCODE['ENDC']}")
            else:
                print(end = '\n')

        print(f"\nEnter {COLORCODE['MAGENTA']}'d'{COLORCODE['ENDC']} to draw.")

        while True:
            selection = input('\nSelect an option: ')
            if selection == 'd':
                break

            try:
                selection = int(selection)
            except (ValueError, TypeError):
                print('Invalid selection.')
                continue

            else:
                if selection < 0 or selection > (len(self.hand) - 1):
                    print('Selection out of range.')
                    continue
                elif self.hand[selection].playable_on(discard_top):
                    selection = self.play_card(selection)
                    break
                else:
                    print('Selection not playable.')
                    continue

        return selection
    
    def select_color(self):
        """
        Returns the player's selected color for a wild card.
        """
        print(f'\n{STYLE["BOLD"]}++++++++++{COLORCODE["Black"]} Wild Card {COLORCODE["ENDC"]}{STYLE["BOLD"]}++++++++++{STYLE["ENDS"]}\n')
        for option, color in enumerate(COLORS):
            print(f'{STYLE["BOLD"]} {option}){STYLE["ENDS"]} {COLORCODE[color]}{color:<9}{COLORCODE["ENDC"]}')

        selection = select_option(0, len(COLORS) - 1)

        return COLORS[selection]
    
    def select_renege(self, drawn_card):
        """
        Returns if the player would like to play the valid card they just drew.
        """
        print(f'\nWould you like to play {COLORCODE[drawn_card.color]}{drawn_card}{COLORCODE["ENDC"]}?\n0) No\n1) Yes')
        
        selection = select_option(0,1)

        return selection
    
    def challenge_select(self):
        """
        Returns a boolean corresponding to if the player accepts the challenge.
        """
        print(f"\n{STYLE['BOLD']}*******************************\n\n{self}'s turn\n\n*******************************{STYLE['ENDS']}\n\n {STYLE['BOLD']}0){STYLE['ENDS']} Decline Challenge\n {STYLE['BOLD']}1){STYLE['ENDS']} Accept Challenge")

        return select_option(0,1)