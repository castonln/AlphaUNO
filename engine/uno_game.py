from engine.deck import Deck
from engine.standard_uno_config import *
from engine.terminal_utils import COLORCODE
from engine.data_encoder import DataEncoder

class UnoGame:
    """
    Handles all game aspects.
    """
    def __init__(self, players):
        self._num_of_players = len(players)
        self._is_clockwise = True
        self._discard_top = None
        self.deck = Deck()
        self.winner = None

        self.de = DataEncoder()

        self.player_list = self._create_players(players)
        self.current_player = self.player_list[0]
        self._deal_cards()
        self._set_discard_top()

    @property
    def discard_top(self):
        return self._discard_top
    
    @discard_top.setter
    def discard_top(self, value):
        try:
            self.deck.append_discard(self._discard_top)
        except AttributeError: # occurs when trying to set the discard_top at the start of the game (None)
            pass
        self._discard_top = value
    
    def _create_players(self, players):
        """
        Creates the desired number of players for the game and returns them all in a list.
        """
        if self._num_of_players > 10:
            raise ValueError("When using a standard UNO deck, 10+ players leads to complications regarding the pool of cards.")

        player_list = players

        return player_list

    def _deal_cards(self):
        """
        Deals a specified amount of cards to each player in player_list.
        """
        for player in self.player_list:
            for _ in range(STARTINGHANDNUM):
                player.draw_card(self.deck)
            self.de.update_hand(player)

    def _set_discard_top(self):
        """
        Draws from the deck until the discard_top is a numbered card (see modern UNO rules for clarification).
        """
        while True:
            self.discard_top = self.deck.pop()
            if self.discard_top._value in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                break

    def play_turn(self):
        """
        Handles the logic for the current player to make their move.
        """
        self.de.add_new_move()
        self.de.add_move_aspect("moves_player", self.current_player)
        self.de.add_move_aspect("discard_top", self._discard_top)

        selection = self.current_player.select_card(self.discard_top)

        # Draw
        if selection == "d":
            drawn_card = self.current_player.draw_card(self.deck)
            print(f"{self.current_player} draws.")
            if drawn_card.playable_on(self.discard_top) and self.current_player.select_renege(drawn_card): # Want to play?
                new_top = self.current_player.play_card()  # Last item to be appended is the drawn_card
                print(f"{self.current_player} plays {COLORCODE[new_top.color]}{new_top}{COLORCODE['ENDC']}")
                self.de.add_move_aspect("played_card", new_top)
                self._activate_card(new_top)
                self.discard_top = new_top

        # Play
        else:
            new_top = selection
            print(f"{self.current_player} plays {COLORCODE[new_top.color]}{new_top}{COLORCODE['ENDC']}")
            self.de.add_move_aspect("played_card", new_top)
            self._activate_card(new_top)
            self.discard_top = new_top

        self.de.update_hand(self.current_player)
        self._check_win()
        self._next_player()

    def _activate_card(self, card):
        """
        Activates the given card.
        """
        if card._value == 'Reverse':
            self._is_clockwise = not self._is_clockwise
            print(f'Direction of play is reversed.')

        elif card._value == 'Skip':
            self._next_player()
            print(f'{self.current_player} is skipped.')

        elif card._value == '+2':
            self._next_player()
            print(f'{self.current_player} draws 2.')
            for _ in range(2):
                self.current_player.draw_card(self.deck)
            self.de.update_hand(self.current_player)

        elif card.color == 'Black':
            card.color = self.current_player.select_color()
            print(f"The color is switched to {COLORCODE[card.color]}{card.color}{COLORCODE['ENDC']}.")
            self.de.add_move_aspect("color_change", card.color)
                
            if card._value == 'Wild +4':
                if CHALLENGERULE:
                    self._challenge_rule()
                else:
                    self._next_player()
                    print(f'{self.current_player} draws 4.')
                    for _ in range(4):
                        self.current_player.draw_card(self.deck)
                    self.de.update_hand(self.current_player)
                    
        # Default for ordinary numbered cards
        else:
            pass

    def _challenge_rule(self):
        """
        Executes the necessary behavior for the challenge rule.
        """
        self._next_player()
        challenge_accepted = self.current_player.challenge_select()

        # Accept challenge
        if challenge_accepted:
            print(f'{self.current_player} accepts the challenge!')
            # We need to reverse back to the last player in order to check their hand / apply the punishment
            self._is_clockwise = not self._is_clockwise
            self._next_player()

            # Check the player's hand
            is_illegal = False
            for card_in_hand in self.current_player.hand:
                if card_in_hand.color == self.discard_top.color:
                    is_illegal = True
                    break

            if is_illegal:
                print(f'{self.current_player} played illegally!')
                self.de.add_move_aspect("challenge_won", True)
                for _ in range(4):
                    self.current_player.draw_card(self.deck)
                self.de.update_hand(self.current_player)
                print(f'{self.current_player} draws 4.')
                # Reverse the direction. No more block of next player
                self._is_clockwise = not self._is_clockwise
            else:
                print(f'{self.current_player} did not play illegally.')
                self.de.add_move_aspect("challenge_won", False)
                # Reverse the direction and head back to the challenger
                self._is_clockwise = not self._is_clockwise
                self._next_player()
                for _ in range(6):
                    self.current_player.draw_card(self.deck)
                self.de.update_hand(self.current_player)
                print(f'{self.current_player} draws 6.')

        # Decline challenge
        else:
            print(f'{self.current_player} declines the challenge.\n{self.current_player} draws 4.')
            for _ in range(4):
                self.current_player.draw_card(self.deck)
            self.de.update_hand(self.current_player)

    def _next_player(self):
        """
        Defines the index of the next player and sets them as the current player.
        """
        player_index = self.player_list.index(self.current_player)

        if self._is_clockwise:
            player_index = (player_index + 1) % self._num_of_players
        else:
            player_index = (player_index - 1) % self._num_of_players

        self.current_player = self.player_list[player_index]

    def total_cards_in_play(self):
        """
        A debugging function that returns the number of cards in all hands, decks, and discard_top.
        """
        sum = len(self.deck)
        for player in self.player_list:
            sum += len(player.hand)
        if self.discard_top:
            sum += 1

        return sum
    
    def _check_win(self):
        """
        Checks if any player has won.
        """
        for player in self.player_list:
            if len(player.hand) == 0:
                self.winner = player
                break

