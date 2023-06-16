class NotEnoughCardsException(Exception):
    """
    When there are too few cards to continue play.
    """
    def __init__(self, message="Not enough cards to continue play. Game has ended."):
        super().__init__(message)