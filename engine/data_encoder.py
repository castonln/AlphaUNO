class DataEncoder:
    """
    Takes in round data from UnoGame to ultimately return a dict that AIs can use as their knowledge base.
    """

    def __init__(self):
        self.encoded_data = {}

        self.encoded_data["cards_in_hands"] = {}
        self.encoded_data["last_moves"] = []

        self._current_move = {}

        self._move_storage_threshold = 5     # number of past moves to hold in data
        self._move_counter = 1   # once this reaches the move storage threshold, it's irrelevant

    def add_new_move(self):
        """
        Append move built to the queue, release a move from the queue (if applicable), and make space for a new one.
        """
        # Add last move
        self.encoded_data["last_moves"].append(self._current_move)

        # Dequeue if over capacity
        if self._move_counter > self._move_storage_threshold:
            self.encoded_data["last_moves"].pop(0)

        # Start building a new move
        self._current_move = {}

        self._move_counter += 1
        
    def add_move_aspect(self, key, value):
        """
        Takes key and value of move and adds it to the _current_move.

        Possible keys:

        moves_player - name of player

        discard_top - discard_top at time of move

        played_card - card played during move

        challenge_won - bool for if challenge is won

        color_change - color changed if wild card is played
        """
        self._current_move[key] = value

    def update_hand(self, player):
        """
        Update the recorded amount of cards in a player's hand.
        """
        self.encoded_data["cards_in_hands"][player] = len(player.hand)