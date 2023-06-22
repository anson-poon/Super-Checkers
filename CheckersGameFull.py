# Author: Anson Poon
# GitHub username: anson-poon
# Description: Super-Checkers
import numpy as np


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


class Checkers:
    """
    Represents a modified checkers game as played.
    """

    def __init__(self):
        self._board = []
        self._player = {}
        self._player_turn = "Black"
        self._prev_player = None
        self._prev_piece_coord = None
        self._prev_move = False
        self._prev_jump = False
        self.create_board()

    def create_player(self, player_name, piece_color):
        """Create a player object and assigns it with a piece color"""
        self._player[player_name] = Player(player_name, piece_color)
        return self._player[player_name]

    def play_game(self, player_name, starting_sq_loc, destination_sq_loc):
        """"""
        start_piece = None
        des_piece = None  # IS DES PIECE NECESSARY?
        piece_color = None
        opponent_player_name = ""

        # Get the opponent player's name
        for player in self._player:
            if player != player_name:
                opponent_player_name = player

        # Validate player name and assign piece color
        if self.validate_player_name(player_name):
            piece_color = self._player[player_name].get_piece_color()
            print(f"Player piece color is: {piece_color}")

        # Validate square location exist, then retrieve starting/destination piece symbol
        if self.validate_square_location(starting_sq_loc) and self.validate_square_location(destination_sq_loc):
            start_piece = self.get_piece_symbol(starting_sq_loc)
            des_piece = self.get_piece_symbol(destination_sq_loc)

        # print(f"Starting position is: {start_piece}")
        # print(f"Destination position is: {des_piece}")

        # Validate square location piece belongs to current player
        self.validate_square_location_ownership(start_piece, piece_color)

        # Validate if the operation is a move or a regular/king/triple king jump
        if self.validate_move(starting_sq_loc, destination_sq_loc, start_piece):
            # Validate if the player is playing out of turn
            self.validate_out_of_turn(player_name, starting_sq_loc, move_or_jump="move")
            print("This is a move")
            self.set_move(starting_sq_loc, destination_sq_loc, start_piece)
            self.flip_turn(player_name)

        # Validate the jump according to piece type, validate if out of turn, if not then jump piece to new location,
        # After that, validate jump opportunity, if no opportunity, flip turn
        elif self.validate_regular_jump(starting_sq_loc, destination_sq_loc, start_piece):
            self.validate_out_of_turn(player_name, starting_sq_loc, move_or_jump="jump")
            print("This is a regular jump")
            self.set_regular_jump(player_name, opponent_player_name, starting_sq_loc, destination_sq_loc, start_piece)
            if not self.validate_regular_jump_opportunity(destination_sq_loc, start_piece):
                print("FLIP REGULAR")
                self.flip_turn(player_name)

        elif self.validate_king_jump(starting_sq_loc, destination_sq_loc, start_piece):
            self.validate_out_of_turn(player_name, starting_sq_loc, move_or_jump="jump")
            print("This is a king jump")
            self.set_king_jump(player_name, opponent_player_name, starting_sq_loc, destination_sq_loc, start_piece)
            if not self.validate_king_jump_opportunity(destination_sq_loc, start_piece):
                print("FLIP KING")
                self.flip_turn(player_name)

        elif self.validate_triple_king_jump(starting_sq_loc, destination_sq_loc, start_piece):
            self.validate_out_of_turn(player_name, starting_sq_loc, move_or_jump="jump")
            print("This is a triple king jump")
            self.set_triple_king_jump(player_name, opponent_player_name, starting_sq_loc, destination_sq_loc,
                                      start_piece)
            if not self.validate_triple_king_jump_opportunity(destination_sq_loc, start_piece):
                self.flip_turn(player_name)

        else:  # Starting piece is None or Invalid move
            raise InvalidSquare("This is an invalid move")

        new_start_piece = self.get_piece_symbol(starting_sq_loc)
        new_des_piece = self.get_piece_symbol(destination_sq_loc)

        # print(f"Now starting position is: {start_piece}")
        # print(f"Now destination position is: {des_piece}")

        if new_des_piece == " B " or new_des_piece == " W ":
            if self.validate_regular_promotion(destination_sq_loc, new_des_piece):
                self.promote_regular_piece(player_name, destination_sq_loc)
        elif new_des_piece == "B K" or new_des_piece == "W K":
            if self.validate_king_promotion(destination_sq_loc, new_des_piece):
                self.promote_king_piece(player_name, destination_sq_loc)

        return self._player[player_name].get_captured_pieces_count()

    def validate_out_of_turn(self, player_name, square_location, move_or_jump):
        """Validate if a player attempts to move a piece out of turn"""
        print(self._player_turn)
        print(self._player[player_name].get_piece_color())
        # print(self._prev_piece_coord)
        # print(self._prev_move)
        # print(self._prev_jump)

        # If this is not the player's turn
        if self._player_turn != self._player[player_name].get_piece_color():
            raise OutofTurn(f"This is not {player_name}'s turn.")

        # If the same player is attempting an action
        if self._player[player_name] == self._prev_player:
            # If previous is a jump, but currently is a move
            if self._prev_jump is True and move_or_jump == "move":
                raise OutofTurn("Previously is a jump, this action cannot be a move.")
            # If previously is a move, and the same player attempt any action
            if self._prev_move:
                raise OutofTurn("Previously is a move, same player cannot move/jump again.")
            # If previously is a jump but player is attempting to jump a different piece
            if self._prev_jump is True and self._prev_piece_coord != square_location:
                raise OutofTurn("Cannot jump a different piece.")

    def validate_player_name(self, player_name):
        """Validate if the player exists in the player dictionary,
        if exist return True, else raise an InvalidPlayer exception"""
        if player_name in self._player:
            return True
        else:
            raise InvalidPlayer("Player not found")

    def validate_square_location(self, square_location):
        """Validate if square location exist on the board,
        if exist return True, else raise InvalidSquare exception"""
        if 0 <= square_location[0] <= 7 and 0 <= square_location[1] <= 7:
            return True
        else:
            raise InvalidSquare("Square location does not exist on the board.")

    def get_piece_symbol(self, square_location):
        """Return the piece symbol present in the square_location of the board"""
        return self._board[square_location[0]][square_location[1]]

    def validate_square_location_ownership(self, start_piece, piece_color):
        """Validate the ownership of the starting and destination square location"""
        black_pieces = [" B ", "B K", "BTK"]
        white_pieces = [" W ", "W K", "WTK"]

        # Check is starting square location belongs to current player
        if piece_color == "Black" and start_piece in black_pieces:
            return True
        elif piece_color == "White" and start_piece in white_pieces:
            return True
        else:
            raise InvalidSquare("Player does not own the piece on the starting square location.")

    def get_checker_details(self, square_location):
        """Convert the symbol present in the square_location of the board into a readable format."""
        if 0 <= square_location[0] <= 7 and 0 <= square_location[1] <= 7:
            square = self._board[square_location[0]][square_location[1]]
            if square == "   ":
                return None
            elif square == " B ":
                return "Black"
            elif square == " W ":
                return "White"
            elif square == "B K":
                return "Black_king"
            elif square == "W K":
                return "White_king"
            elif square == "BTK":
                return "Black_Triple_King"
            elif square == "WTK":
                return "White_Triple_King"
            else:
                return None
        else:
            raise InvalidSquare("Square location does not exist on the board.")

    def validate_move(self, starting_sq_loc, destination_sq_loc, checker_piece):
        """Validate if the piece move is valid"""
        horizontal_flag = False
        vertical_flag = False

        # For any piece, +1 or -1 diagonal horizontal moves are allowed
        if destination_sq_loc[1] == starting_sq_loc[1] + 1 or destination_sq_loc[1] == starting_sq_loc[1] - 1:
            horizontal_flag = True

        # For Black piece, -1 vertical moves are allowed
        if checker_piece == " B ":
            if destination_sq_loc[0] == starting_sq_loc[0] - 1:
                vertical_flag = True
        # For White piece, +1 vertical moves are allowed
        elif checker_piece == " W ":
            if destination_sq_loc[0] == starting_sq_loc[0] + 1:
                vertical_flag = True

        elif checker_piece == "B K" or checker_piece == "BTK" or checker_piece == "W K" or checker_piece == "WTK":
            if destination_sq_loc[0] == starting_sq_loc[0] - 1 or destination_sq_loc[0] == starting_sq_loc[0] + 1:
                vertical_flag = True

        return horizontal_flag and vertical_flag

    def validate_regular_jump(self, starting_sq_loc, destination_sq_loc, checker_piece):
        """Validate if the regular piece jump is valid"""
        horizontal_flag = False
        vertical_flag = False

        # For any checker, +2 or -2 diagonal horizontal moves are allowed
        if destination_sq_loc[1] == starting_sq_loc[1] + 2 or destination_sq_loc[1] == starting_sq_loc[1] - 2:
            horizontal_flag = True
        # For Black checker, -2 vertical moves are allowed
        if checker_piece == " B ":
            if destination_sq_loc[0] == starting_sq_loc[0] - 2:
                vertical_flag = True
        # For White checker, +2 vertical moves are allowed
        elif checker_piece == " W ":
            if destination_sq_loc[0] == starting_sq_loc[0] + 2:
                vertical_flag = True

        return horizontal_flag and vertical_flag

    def validate_king_jump(self, starting_sq_loc, destination_sq_loc, checker_piece):
        """Validate if the king piece jump is valid"""
        if checker_piece == "B K" or checker_piece == "W K":
            np_board = np.array(self._board)
            x, y = starting_sq_loc
            start_pos = None
            des_pos = None
            capture_count = 0

            # Set the destination square location to " D " as placeholder for the list search operation
            self._board[destination_sq_loc[0]][destination_sq_loc[1]] = " D "

            # Find the diagonal list from top left and top right
            diagonal_list_from_top_left = np.diagonal(np_board, offset=(y - x))
            print(diagonal_list_from_top_left)
            diagonal_list_from_top_right = np.diagonal(np.rot90(np_board), offset=-np_board.shape[0] + (y + x) + 1)
            print(diagonal_list_from_top_right)

            # If jumping from top left to bottom right
            if starting_sq_loc[0] < destination_sq_loc[0] and starting_sq_loc[1] < destination_sq_loc[1]:
                diagonal_list = diagonal_list_from_top_left
            # If jumping from top right to bottom left
            elif starting_sq_loc[0] < destination_sq_loc[0] and starting_sq_loc[1] > destination_sq_loc[1]:
                diagonal_list = diagonal_list_from_top_right
            # If jumping from bottom left to top right
            elif starting_sq_loc[0] > destination_sq_loc[0] and starting_sq_loc[1] < destination_sq_loc[1]:
                diagonal_list = np.flip(diagonal_list_from_top_right)
            # If jumping from bottom right to top left
            elif starting_sq_loc[0] > destination_sq_loc[0] and starting_sq_loc[1] > destination_sq_loc[1]:
                diagonal_list = np.flip(diagonal_list_from_top_left)
            else:
                raise InvalidSquare

            print(f"decided diagonal list: {diagonal_list}")

            # Locate the index of the player's piece and destination square location
            for index, piece in enumerate(diagonal_list):
                if piece == checker_piece:
                    start_pos = index
                if piece == " D ":
                    des_pos = index

            print(f"From: {start_pos}")
            print(f"To: {des_pos}")

            # Slice the diagonal list to include just the square locations in between player's piece and destination
            diagonal_list = diagonal_list[start_pos + 1:des_pos]
            print(f"new diagonal list: {diagonal_list}")

            # Count the number of opponent pieces that the player jumped
            if checker_piece == "B K":
                for piece in diagonal_list:
                    if piece == " W " or piece == "W K" or piece == "WTK":
                        capture_count += 1

            elif checker_piece == "W K":
                for piece in diagonal_list:
                    if piece == " B " or piece == "B K" or piece == "BTK":
                        capture_count += 1

            # Reset " D " placeholder
            self._board[destination_sq_loc[0]][destination_sq_loc[1]] = "   "

            print(capture_count)
            if capture_count == 1:
                return True

    def validate_triple_king_jump(self, starting_sq_loc, destination_sq_loc, checker_piece):
        """Validate if the triple king piece jump is valid"""
        if checker_piece == "BTK" or checker_piece == "WTK":
            np_board = np.array(self._board)
            x, y = starting_sq_loc
            start_pos = None
            des_pos = None
            capture_count = 0

            # Set the destination square location to " D " as placeholder for the list search operation
            self._board[destination_sq_loc[0]][destination_sq_loc[1]] = " D "

            # Find the diagonal list from top left and top right
            diagonal_list_from_top_left = np.diagonal(np_board, offset=(y - x))
            print(diagonal_list_from_top_left)
            diagonal_list_from_top_right = np.diagonal(np.rot90(np_board), offset=-np_board.shape[0] + (y + x) + 1)
            print(diagonal_list_from_top_right)

            # If jumping from top left to bottom right
            if starting_sq_loc[0] < destination_sq_loc[0] and starting_sq_loc[1] < destination_sq_loc[1]:
                diagonal_list = diagonal_list_from_top_left
            # If jumping from top right to bottom left
            elif starting_sq_loc[0] < destination_sq_loc[0] and starting_sq_loc[1] > destination_sq_loc[1]:
                diagonal_list = diagonal_list_from_top_right
            # If jumping from bottom left to top right
            elif starting_sq_loc[0] > destination_sq_loc[0] and starting_sq_loc[1] < destination_sq_loc[1]:
                diagonal_list = np.flip(diagonal_list_from_top_right)
            # If jumping from bottom right to top left
            elif starting_sq_loc[0] > destination_sq_loc[0] and starting_sq_loc[1] > destination_sq_loc[1]:
                diagonal_list = np.flip(diagonal_list_from_top_left)
            else:
                raise InvalidSquare

            print(f"decided diagonal list: {diagonal_list}")

            # Locate the index of the player's piece and destination square location
            for index, piece in enumerate(diagonal_list):
                if piece == checker_piece:
                    start_pos = index
                if piece == " D ":
                    des_pos = index

            print(f"From: {start_pos}")
            print(f"To: {des_pos}")

            # Slice the diagonal list to include just the square locations in between player's piece and destination
            diagonal_list = diagonal_list[start_pos + 1:des_pos]
            print(f"new diagonal list: {diagonal_list}")

            # Count the number of opponent pieces that the player jumped
            if checker_piece == "BTK":
                for piece in diagonal_list:
                    if piece == " W " or piece == "W K" or piece == "WTK":
                        capture_count += 1

            elif checker_piece == "WTK":
                for piece in diagonal_list:
                    if piece == " B " or piece == "B K" or piece == "BTK":
                        capture_count += 1

            # Triple king can either jump friendly piece, or jump 1 or 2 opponent pieces
            if 0 <= capture_count <= 2:
                return True

    def set_move(self, starting_sq_loc, destination_sq_loc, checker_piece):
        """Move the checker"""
        self._board[starting_sq_loc[0]][starting_sq_loc[1]] = "   "
        self._board[destination_sq_loc[0]][destination_sq_loc[1]] = checker_piece

        self._prev_move = True
        self._prev_jump = False

    def set_regular_jump(self, player_name, opponent_player_name, starting_sq_loc, destination_sq_loc, checker_piece):
        """Jump the regular checker and keep track of the captured opponent pieces count during the jump"""

        # Set initial location to blank and new location to checker
        self._board[starting_sq_loc[0]][starting_sq_loc[1]] = "   "
        self._board[destination_sq_loc[0]][destination_sq_loc[1]] = checker_piece

        # Find the coordinate of the piece in between the jump
        mid_piece_x_coord = int((destination_sq_loc[0] + starting_sq_loc[0]) / 2)
        mid_piece_y_coord = int((destination_sq_loc[1] + starting_sq_loc[1]) / 2)

        # Set that piece to blank
        captured_piece = self._board[mid_piece_x_coord][mid_piece_y_coord]
        self._board[mid_piece_x_coord][mid_piece_y_coord] = "   "

        # Increment the player's piece
        self._player[player_name].increment_captured_pieces_count(1)

        # Decrement the opponent's king or triple king piece (if any)
        if self._player[player_name].get_piece_color() == "Black":
            if captured_piece == "W K":
                self._player[opponent_player_name].decrement_king_count()
            elif captured_piece == "WTK":
                self._player[opponent_player_name].decrement_triple_king_count()
        elif self._player[player_name].get_piece_color() == "White":
            if captured_piece == "B K":
                self._player[opponent_player_name].decrement_king_count()
            elif captured_piece == "BTK":
                self._player[opponent_player_name].decrement_triple_king_count()

        self._prev_piece_coord = destination_sq_loc
        self._prev_move = False
        self._prev_jump = True

    def set_king_jump(self, player_name, opponent_player_name, starting_sq_loc, destination_sq_loc, checker_piece):
        """Jump the king checker and keep track of the captured opponent pieces count during the jump"""
        black_pieces = [" B ", "B K", "BTK"]
        white_pieces = [" W ", "W K", "WTK"]
        x_coord_arr, y_coord_arr = [], []

        # Set initial location to blank and new location to checker
        self._board[starting_sq_loc[0]][starting_sq_loc[1]] = "   "
        self._board[destination_sq_loc[0]][destination_sq_loc[1]] = checker_piece

        # If a checker within the diagonal line of jump is an opponent checker, capture it
        # If the jump is from top left to bottom right
        if starting_sq_loc[0] < destination_sq_loc[0] and starting_sq_loc[1] < destination_sq_loc[1]:
            # increment x/y coord to the next square location diagonally
            y_coord = starting_sq_loc[0] + 1
            x_coord = starting_sq_loc[1] + 1

            while starting_sq_loc[0] < y_coord < destination_sq_loc[0]:
                print(y_coord)
                y_coord_arr.append(y_coord)
                y_coord += 1
            while starting_sq_loc[1] < x_coord < destination_sq_loc[1]:
                print(x_coord)
                x_coord_arr.append(x_coord)
                x_coord += 1

            print((y_coord_arr, x_coord_arr))

        # If the jump is from top right to bottom left
        elif starting_sq_loc[0] < destination_sq_loc[0] and starting_sq_loc[1] > destination_sq_loc[1]:
            # increment x/y coord to the next square location diagonally
            y_coord = starting_sq_loc[0] + 1
            x_coord = starting_sq_loc[1] - 1

            while starting_sq_loc[0] < y_coord < destination_sq_loc[0]:
                print(y_coord)
                y_coord_arr.append(y_coord)
                y_coord += 1
            while starting_sq_loc[1] > x_coord > destination_sq_loc[1]:
                print(x_coord)
                x_coord_arr.append(x_coord)
                x_coord -= 1

            print((y_coord_arr, x_coord_arr))

        # If the jump is from bottom left to top right
        elif starting_sq_loc[0] > destination_sq_loc[0] and starting_sq_loc[1] < destination_sq_loc[1]:
            # increment x/y coord to the next square location diagonally
            y_coord = starting_sq_loc[0] - 1
            x_coord = starting_sq_loc[1] + 1

            while starting_sq_loc[0] > y_coord > destination_sq_loc[0]:
                print(y_coord)
                y_coord_arr.append(y_coord)
                y_coord -= 1
            while starting_sq_loc[1] < x_coord < destination_sq_loc[1]:
                print(x_coord)
                x_coord_arr.append(x_coord)
                x_coord += 1

            print((y_coord_arr, x_coord_arr))

        # If the jump is from bottom right to top left
        elif starting_sq_loc[0] > destination_sq_loc[0] and starting_sq_loc[1] > destination_sq_loc[1]:
            # increment x/y coord to the next square location diagonally
            y_coord = starting_sq_loc[0] - 1
            x_coord = starting_sq_loc[1] - 1

            while starting_sq_loc[0] > y_coord > destination_sq_loc[0]:
                print(y_coord)
                y_coord_arr.append(y_coord)
                y_coord -= 1
            while starting_sq_loc[1] > x_coord > destination_sq_loc[1]:
                print(x_coord)
                x_coord_arr.append(x_coord)
                x_coord -= 1

            print((y_coord_arr, x_coord_arr))

        else:
            raise InvalidSquare("The square location the player is jumping to is not valid")

        # Decrement opponent's king/triple king piece (if any), capturing opponent pieces, increment captured count
        if checker_piece == "B K":
            for coord in range(len(y_coord_arr)):
                if self._board[y_coord_arr[coord]][x_coord_arr[coord]] in white_pieces:
                    if self._board[y_coord_arr[coord]][x_coord_arr[coord]] == "W K":
                        self._player[opponent_player_name].decrement_king_count()
                    elif self._board[y_coord_arr[coord]][x_coord_arr[coord]] == "WTK":
                        self._player[opponent_player_name].decrement_triple_king_count()

                    self._board[y_coord_arr[coord]][x_coord_arr[coord]] = "   "
                    self._player[player_name].increment_captured_pieces_count(1)

        elif checker_piece == "W K":
            for coord in range(len(y_coord_arr)):
                if self._board[y_coord_arr[coord]][x_coord_arr[coord]] in black_pieces:
                    if self._board[y_coord_arr[coord]][x_coord_arr[coord]] == "B K":
                        self._player[opponent_player_name].decrement_king_count()
                    elif self._board[y_coord_arr[coord]][x_coord_arr[coord]] == "BTK":
                        self._player[opponent_player_name].decrement_triple_king_count()

                    self._board[y_coord_arr[coord]][x_coord_arr[coord]] = "   "
                    self._player[player_name].increment_captured_pieces_count(1)

        self._prev_piece_coord = destination_sq_loc
        self._prev_move = False
        self._prev_jump = True

    def set_triple_king_jump(self, player_name, opponent_player_name, starting_sq_loc, destination_sq_loc, checker_piece):
        """Jump the triple king checker and keep track of the captured opponent pieces count during the jump"""
        black_pieces = [" B ", "B K", "BTK"]
        white_pieces = [" W ", "W K", "WTK"]
        x_coord_arr, y_coord_arr = [], []

        # Set initial location to blank and new location to checker
        self._board[starting_sq_loc[0]][starting_sq_loc[1]] = "   "
        self._board[destination_sq_loc[0]][destination_sq_loc[1]] = checker_piece

        # If a checker within the diagonal line of jump is an opponent checker, capture it
        # If the jump is from top left to bottom right
        if starting_sq_loc[0] < destination_sq_loc[0] and starting_sq_loc[1] < destination_sq_loc[1]:
            # increment x/y coord to the next square location diagonally
            y_coord = starting_sq_loc[0] + 1
            x_coord = starting_sq_loc[1] + 1

            while starting_sq_loc[0] < y_coord < destination_sq_loc[0]:
                print(y_coord)
                y_coord_arr.append(y_coord)
                y_coord += 1
            while starting_sq_loc[1] < x_coord < destination_sq_loc[1]:
                print(x_coord)
                x_coord_arr.append(x_coord)
                x_coord += 1

            print((y_coord_arr, x_coord_arr))

        # If the jump is from top right to bottom left
        elif starting_sq_loc[0] < destination_sq_loc[0] and starting_sq_loc[1] > destination_sq_loc[1]:
            # increment x/y coord to the next square location diagonally
            y_coord = starting_sq_loc[0] + 1
            x_coord = starting_sq_loc[1] - 1

            while starting_sq_loc[0] < y_coord < destination_sq_loc[0]:
                print(y_coord)
                y_coord_arr.append(y_coord)
                y_coord += 1
            while starting_sq_loc[1] > x_coord > destination_sq_loc[1]:
                print(x_coord)
                x_coord_arr.append(x_coord)
                x_coord -= 1

            print((y_coord_arr, x_coord_arr))

        # If the jump is from bottom left to top right
        elif starting_sq_loc[0] > destination_sq_loc[0] and starting_sq_loc[1] < destination_sq_loc[1]:
            # increment x/y coord to the next square location diagonally
            y_coord = starting_sq_loc[0] - 1
            x_coord = starting_sq_loc[1] + 1

            while starting_sq_loc[0] > y_coord > destination_sq_loc[0]:
                print(y_coord)
                y_coord_arr.append(y_coord)
                y_coord -= 1
            while starting_sq_loc[1] < x_coord < destination_sq_loc[1]:
                print(x_coord)
                x_coord_arr.append(x_coord)
                x_coord += 1

            print((y_coord_arr, x_coord_arr))

        # If the jump is from bottom right to top left
        elif starting_sq_loc[0] > destination_sq_loc[0] and starting_sq_loc[1] > destination_sq_loc[1]:
            # increment x/y coord to the next square location diagonally
            y_coord = starting_sq_loc[0] - 1
            x_coord = starting_sq_loc[1] - 1

            while starting_sq_loc[0] > y_coord > destination_sq_loc[0]:
                print(y_coord)
                y_coord_arr.append(y_coord)
                y_coord -= 1
            while starting_sq_loc[1] > x_coord > destination_sq_loc[1]:
                print(x_coord)
                x_coord_arr.append(x_coord)
                x_coord -= 1

            print((y_coord_arr, x_coord_arr))

        else:
            raise InvalidSquare("The square location the player is jumping to is not valid")

        # Capturing opponent pieces
        if checker_piece == "BTK":
            for coord in range(len(y_coord_arr)):
                if self._board[y_coord_arr[coord]][x_coord_arr[coord]] in white_pieces:
                    if self._board[y_coord_arr[coord]][x_coord_arr[coord]] == "W K":
                        self._player[opponent_player_name].decrement_king_count()
                    elif self._board[y_coord_arr[coord]][x_coord_arr[coord]] == "WTK":
                        self._player[opponent_player_name].decrement_triple_king_count()

                    self._board[y_coord_arr[coord]][x_coord_arr[coord]] = "   "
                    self._player[player_name].increment_captured_pieces_count(1)

        elif checker_piece == "WTK":
            for coord in range(len(y_coord_arr)):
                if self._board[y_coord_arr[coord]][x_coord_arr[coord]] in black_pieces:
                    if self._board[y_coord_arr[coord]][x_coord_arr[coord]] == "B K":
                        self._player[opponent_player_name].decrement_king_count()
                    elif self._board[y_coord_arr[coord]][x_coord_arr[coord]] == "BTK":
                        self._player[opponent_player_name].decrement_triple_king_count()

                    self._board[y_coord_arr[coord]][x_coord_arr[coord]] = "   "
                    self._player[player_name].increment_captured_pieces_count(1)

        self._prev_piece_coord = destination_sq_loc
        self._prev_move = False
        self._prev_jump = True

    def validate_regular_jump_opportunity(self, current_sq_loc, checker_piece):
        """Validate if the regular checker has the opportunity to jump an opponent's checker"""
        black_pieces = [" B ", "B K", "BTK"]
        white_pieces = [" W ", "W K", "WTK"]

        # print(self._prev_piece_coord)
        # print(checker_symbol)
        # if self._prev_piece_coord == current_sq_loc:

        print(f"current location: {current_sq_loc}")

        # If a diagonal square location is an opponent piece and the square location after is blank
        if checker_piece == " B ":
            if 0 <= current_sq_loc[0] - 2 <= 7 and 0 <= current_sq_loc[1] - 2 <= 7:
                if self._board[current_sq_loc[0] - 2][current_sq_loc[1] - 2] == "   " and self._board[current_sq_loc[0] - 1][current_sq_loc[1] - 1] in white_pieces:
                    return True
            if 0 <= current_sq_loc[0] - 2 <= 7 and 0 <= current_sq_loc[1] + 2 <= 7:
                if self._board[current_sq_loc[0] - 2][current_sq_loc[1] + 2 == "   " and self._board[current_sq_loc[0] - 1][current_sq_loc[1] + 1] in white_pieces]:
                    return True

        elif checker_piece == " W ":
            if 0 <= current_sq_loc[0] + 2 <= 7 and 0 <= current_sq_loc[1] - 2 <= 7:
                if self._board[current_sq_loc[0] + 2][current_sq_loc[1] - 2] == "   " and self._board[current_sq_loc[0] + 1][current_sq_loc[1] - 1] in black_pieces:
                    return True
            if 0 <= current_sq_loc[0] + 2 <= 7 and 0 <= current_sq_loc[1] + 2 <= 7:
                if self._board[current_sq_loc[0] + 2][current_sq_loc[1] + 2] == "   " and self._board[current_sq_loc[0] + 1][current_sq_loc[1] + 1] in black_pieces:
                    return True

    def validate_king_jump_opportunity(self, current_sq_loc, checker_piece):
        """Validate if the king checker has the opportunity to jump an opponent's checker"""
        black_pieces = [" B ", "B K", "BTK"]
        white_pieces = [" W ", "W K", "WTK"]

        more_jump = False

        np_board = np.array(self._board)
        x, y = current_sq_loc

        # Find the diagonal list from top left and top right
        diagonal_list_from_top_left = np.diagonal(np_board, offset=(y - x))
        print(diagonal_list_from_top_left)
        diagonal_list_from_top_right = np.diagonal(np.rot90(np_board), offset=-np_board.shape[0] + (y + x) + 1)
        print(diagonal_list_from_top_right)

        diagonal_list_to_bottom_right = []
        diagonal_list_to_bottom_left = []
        diagonal_list_to_top_right = []
        diagonal_list_to_top_left = []

        # Find list from current square location to bottom right
        for index, piece in enumerate(diagonal_list_from_top_left):
            if piece == checker_piece:
                diagonal_list_to_bottom_right = diagonal_list_from_top_left[index:].tolist()

        # Find list from current square location to bottom left
        for index, piece in enumerate(diagonal_list_from_top_right):
            if piece == checker_piece:
                diagonal_list_to_bottom_left = diagonal_list_from_top_right[index:].tolist()

        # Find list from current square location to top right
        for index, piece in enumerate(np.flip(diagonal_list_from_top_right)):
            if piece == checker_piece:
                diagonal_list_to_top_right = np.flip(diagonal_list_from_top_right)[index:].tolist()

        # Find list from current square location to top right
        for index, piece in enumerate(np.flip(diagonal_list_from_top_left)):
            if piece == checker_piece:
                diagonal_list_to_top_left = np.flip(diagonal_list_from_top_left)[index:].tolist()

        # Change all opponent pieces to " O "
        if checker_piece == "B K":
            for index, square in enumerate(diagonal_list_to_bottom_right):
                if square == " W " or square == "W K" or square == "WTK":
                    diagonal_list_to_bottom_right[index] = " O "
            for index, square in enumerate(diagonal_list_to_bottom_left):
                if square == " W " or square == "W K" or square == "WTK":
                    diagonal_list_to_bottom_left[index] = " O "
            for index, square in enumerate(diagonal_list_to_top_right):
                if square == " W " or square == "W K" or square == "WTK":
                    diagonal_list_to_top_right[index] = " O "
            for index, square in enumerate(diagonal_list_to_top_left):
                if square == " W " or square == "W K" or square == "WTK":
                    diagonal_list_to_top_left[index] = " O "

        elif checker_piece == "W K":
            for index, square in enumerate(diagonal_list_to_bottom_right):
                if square == " B " or square == "B K" or square == "BTK":
                    diagonal_list_to_bottom_right[index] = " O "
            for index, square in enumerate(diagonal_list_to_bottom_left):
                if square == " B " or square == "B K" or square == "BTK":
                    diagonal_list_to_bottom_left[index] = " O "
            for index, square in enumerate(diagonal_list_to_top_right):
                if square == " B " or square == "B K" or square == "BTK":
                    diagonal_list_to_top_right[index] = " O "
            for index, square in enumerate(diagonal_list_to_top_left):
                if square == " B " or square == "B K" or square == "BTK":
                    diagonal_list_to_top_left[index] = " O "

        print("++++++++++++++++++")
        print(diagonal_list_to_bottom_right)
        print(diagonal_list_to_bottom_left)
        print(diagonal_list_to_top_right)
        print(diagonal_list_to_top_left)
        print("++++++++++++++++++")

        # Method to compare the valid jump sequence to the diagonal list,
        # if the valid jump sequence is subsequence of diagonal list, then the jump is valid
        def rec_is_valid_jump(valid_jump_seq, diagonal_list, seq_to_compare, pos1, pos2):
            if pos1 >= len(valid_jump_seq) or pos2 >= len(diagonal_list):  # base case: if pos1/pos2 index out of range
                if seq_to_compare == valid_jump_seq:  # then do the comparison
                    return True
                else:
                    return False

            if valid_jump_seq[pos1] == diagonal_list[pos2]:  # if str1 in index [pos1] equals str2 in index [pos2]
                seq_to_compare.append(diagonal_list[pos2])  # append the character to str_to_compare
                pos1 += 1  # increment index for str1

            pos2 += 1  # increment index for str2 (regardless of matching)
            return rec_is_valid_jump(valid_jump_seq, diagonal_list, seq_to_compare, pos1, pos2)

        def is_valid_jump(valid_jump_seq, diagonal_list):
            """Helper method to initialize seq_to_compare, pos1, pos2"""
            return rec_is_valid_jump(valid_jump_seq, diagonal_list, [], 0, 0)

        all_diagonal_lists = [diagonal_list_to_bottom_right, diagonal_list_to_bottom_left, diagonal_list_to_top_right,
                              diagonal_list_to_top_left]

        # Declare all possible valid jump sequences, and check recursively if any diagonal lists have matching sequences
        valid_jump_seqs = [["   ", " O ", "   "], [" O ", "   "]]  # O is opponent piece
        for valid_jump_seq in valid_jump_seqs:
            for diagonal_list in all_diagonal_lists:
                if is_valid_jump(valid_jump_seq, diagonal_list):
                    print("OKKKKKKKKK")
                    return True

    def validate_triple_king_jump_opportunity(self, current_sq_loc, checker_piece):
        """Validate if the triple king checker has the opportunity to jump an opponent's checker"""
        # for x_coord in range

        # TODO
        pass

    def flip_turn(self, player_name):
        """Flip the turn to the opponent player"""
        if self._player[player_name].get_piece_color() == "Black":
            self._player_turn = "White"
        elif self._player[player_name].get_piece_color() == "White":
            self._player_turn = "Black"

    def validate_regular_promotion(self, square_location, checker_piece):
        """Validate if a regular checker has reached the end of opponent's side and can be promoted to king"""
        if checker_piece == " B " and square_location[0] == 0:
            return True
        elif checker_piece == " W " and square_location[0] == 7:
            return True

    def validate_king_promotion(self, square_location, checker_piece):
        """Validate if a king checker has reached the end of opponent's side again and can be promoted to triple king"""
        if checker_piece == "B K" and square_location[0] == 7:
            return True
        elif checker_piece == "W K" and square_location[0] == 0:
            return True

    def promote_regular_piece(self, player_name, square_location):
        """Promote a regular piece to king"""
        if self._board[square_location[0]][square_location[1]] == " B ":
            self._board[square_location[0]][square_location[1]] = "B K"
        elif self._board[square_location[0]][square_location[1]] == " W ":
            self._board[square_location[0]][square_location[1]] = "W K"

        self._player[player_name].increment_king_count()

    def promote_king_piece(self, player_name, square_location):
        """Promote a king piece to triple king"""
        if self._board[square_location[0]][square_location[1]] == "B K":
            self._board[square_location[0]][square_location[1]] = "BTK"
        elif self._board[square_location[0]][square_location[1]] == "W K":
            self._board[square_location[0]][square_location[1]] = "WTK"

        self._player[player_name].decrement_king_count()
        self._player[player_name].increment_triple_king_count()

    def game_winner(self):
        """Check to see if a player has won the game"""
        for player in self._player:
            if self._player[player].get_captured_pieces_count() == 12:
                # print(f"{self._player[player].get_player_name()} won!")
                return self._player[player].get_player_name()
        else:
            return "Game has not ended"

    def create_board(self):
        """Create each row of the board as an array and append it to self._board"""
        self._board.append([None, " W ", None, " W ", None, " W ", None, " W "])
        self._board.append([" W ", None, " W ", None, " W ", None, " W ", None])
        self._board.append([None, " W ", None, " W ", None, " W ", None, " W "])
        self._board.append(["   ", None, "   ", None, "   ", None, "   ", None])
        self._board.append([None, "   ", None, "   ", None, "   ", None, "   "])
        self._board.append([" B ", None, " B ", None, " B ", None, " B ", None])
        self._board.append([None, " B ", None, " B ", None, " B ", None, " B "])
        self._board.append([" B ", None, " B ", None, " B ", None, " B ", None])

    def print_board(self):
        """Print the current board in the form of 2D list"""
        for row in self._board:
            print(row)


class OutofTurn(Exception):
    """Exception for when a player attempts to move a piece out of turn"""
    pass


class InvalidPlayer(Exception):
    """Exception for when the player does not exist"""
    pass


class InvalidSquare(Exception):
    """Exception for when a player attempts to move to an invalid square"""
    pass

def main():
    game = Checkers()
    player_1 = game.create_player("Adam", "White")
    player_2 = game.create_player("Lucy", "Black")

    game.play_game("Lucy", (5, 6), (4, 7))
    game.play_game("Adam", (2, 1), (3, 0))
    game.play_game("Lucy", (5, 2), (4, 3))
    game.play_game("Adam", (1, 0), (2, 1))
    game.play_game("Lucy", (5, 0), (4, 1))
    game.play_game("Adam", (3, 0), (5, 2))  # Regular Jump
    game.play_game("Lucy", (6, 3), (4, 1))  # Regular Jump
    game.play_game("Adam", (0, 1), (1, 0))
    game.play_game("Lucy", (6, 5), (5, 6))
    game.play_game("Adam", (2, 3), (3, 2))
    game.play_game("Lucy", (4, 1), (2, 3))  # Regular Jump
    game.play_game("Lucy", (2, 3), (0, 1))  # Regular Jump (dbl, become king)
    game.play_game("Adam", (2, 1), (3, 0))
    game.play_game("Lucy", (5, 6), (4, 5))
    game.play_game("Adam", (0, 3), (1, 2))
    game.play_game("Lucy", (0, 1), (3, 4))  # King jump
    game.play_game("Adam", (3, 0), (4, 1))
    game.play_game("Lucy", (4, 3), (3, 2))
    game.play_game("Adam", (2, 5), (3, 6))
    game.play_game("Lucy", (4, 7), (2, 5))  # Regular Jump
    game.play_game("Lucy", (2, 5), (0, 3))  # Regular Jump (dbl, become king)
    game.play_game("Adam", (1, 6), (2, 5))
    game.play_game("Lucy", (6, 1), (5, 0))
    game.play_game("Adam", (4, 1), (5, 2))
    game.play_game("Lucy", (5, 0), (4, 1))
    game.play_game("Adam", (2, 5), (4, 3))  # Regular Jump (captured a king)
    game.play_game("Adam", (4, 3), (6, 5))  # Regular Jump
    game.play_game("Lucy", (7, 4), (5, 6))  # Regular Jump
    game.play_game("Adam", (0, 7), (1, 6))
    game.play_game("Lucy", (7, 2), (6, 1))
    game.play_game("Adam", (5, 2), (6, 3))
    game.play_game("Lucy", (0, 3), (1, 2))
    game.play_game("Adam", (6, 3), (7, 4))  # become king
    game.play_game("Lucy", (4, 1), (3, 0))
    game.play_game("Adam", (7, 4), (4, 7))  # King jump
    game.play_game("Lucy", (1, 2), (2, 3))
    game.play_game("Adam", (4, 7), (3, 6))
    game.play_game("Lucy", (2, 3), (3, 4))
    game.play_game("Adam", (0, 5), (1, 4))
    game.play_game("Lucy", (3, 4), (0, 7))  # King jump
    game.play_game("Adam", (3, 6), (7, 2))  # King jump
    game.play_game("Adam", (7, 2), (5, 0))  # King jump (dbl)
    game.play_game("Adam", (5, 0), (2, 3))  # King jump (tpl)
    game.play_game("Lucy", (0, 7), (1, 6))
    game.play_game("Adam", (2, 3), (3, 2))
    game.play_game("Lucy", (7, 0), (6, 1))
    game.play_game("Adam", (1, 4), (2, 3))
    game.play_game("Lucy", (7, 6), (6, 5))
    game.play_game("Adam", (3, 2), (7, 6))  # King jump
    game.play_game("Lucy", (1, 6), (2, 5))
    game.play_game("Adam", (2, 3), (3, 2))
    game.play_game("Lucy", (2, 5), (3, 4))
    game.play_game("Adam", (7, 6), (6, 5))
    game.play_game("Lucy", (3, 4), (4, 5))
    game.play_game("Adam", (3, 2), (4, 3))
    game.play_game("Lucy", (4, 5), (5, 4))
    game.play_game("Adam", (6, 5), (5, 6))
    game.play_game("Lucy", (5, 4), (6, 3))
    game.play_game("Adam", (5, 6), (4, 5))
    game.play_game("Lucy", (6, 3), (7, 4))  # become triple king
    game.play_game("Adam", (4, 5), (3, 6))
    game.play_game("Lucy", (7, 4), (6, 3))
    game.play_game("Adam", (3, 6), (2, 5))
    game.play_game("Lucy", (6, 1), (5, 2))
    game.play_game("Adam", (4, 3), (5, 4))
    game.play_game("Lucy", (5, 2), (4, 3))
    game.play_game("Adam", (2, 7), (3, 6))
    game.play_game("Lucy", (6, 3), (2, 7))  # Triple king jump
    game.play_game("Adam", (2, 5), (1, 4))
    game.play_game("Lucy", (3, 0), (2, 1))
    game.play_game("Adam", (1, 0), (3, 2))  # Regular Jump
    game.play_game("Adam", (3, 2), (5, 4))  # Regular Jump (dbl)
    game.play_game("Lucy", (6, 7), (5, 6))
    game.play_game("Adam", (1, 4), (2, 5))
    game.play_game("Lucy", (5, 6), (4, 7))
    game.play_game("Adam", (2, 5), (3, 6))
    game.play_game("Lucy", (2, 7), (6, 3))  # Triple king jump (two pieces)

    # print(game._player_turn)
    game.print_board()

    print("Lucy captured: " + str(player_2.get_captured_pieces_count()))
    print("Lucy king count: " + str(player_2.get_king_count()))
    print("Lucy tripe king count: " + str(player_2.get_triple_king_count()))
    print("Adam captured: " + str(player_1.get_captured_pieces_count()))
    print("Adam king count: " + str(player_1.get_king_count()))
    print("Adam triple king count: " + str(player_1.get_triple_king_count()))

    print(game.game_winner())

if __name__ == "__main__":
    main()