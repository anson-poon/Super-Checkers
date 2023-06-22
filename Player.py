class Player:
    """
    Represent a player in the game, with the player's name, piece color, king/triple king count,
    and captured pieces count.
    """

    def __init__(self, player_name, piece_color):
        self._player_name = player_name
        self._piece_color = piece_color
        self._king_count = 0
        self._triple_king_count = 0
        self._captured_pieces_count = 0

    def get_player_name(self):
        """Retrieve the player's name"""
        return self._player_name

    def get_piece_color(self):
        """Retrieve the player's piece color"""
        return self._piece_color

    def get_king_count(self):
        """Retrieve the number of king the player owns"""
        return self._king_count

    def increment_king_count(self):
        """Increment the number of king the player owns by 1"""
        self._king_count += 1

    def decrement_king_count(self):
        """Decrement the number of king the player owns by 1"""
        self._king_count -= 1

    def get_triple_king_count(self):
        """Retrieve the number of triple king the player owns"""
        return self._triple_king_count

    def increment_triple_king_count(self):
        """Increment the number of triple king the player owns by 1"""
        self._triple_king_count += 1

    def decrement_triple_king_count(self):
        """Decrement the number of triple king the player owns by 1"""
        self._triple_king_count -= 1

    def get_captured_pieces_count(self):
        """Retrieve the number of opponent pieces the player captured"""
        return self._captured_pieces_count

    def increment_captured_pieces_count(self, num):
        """Increment the number of captured piece by the number of pieces captured at one round"""
        self._captured_pieces_count += num
