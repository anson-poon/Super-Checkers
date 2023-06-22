# Author: Anson Poon
# GitHub username: anson-poon
# Description: Super-Checkers
from Checkers import *


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
    print(game.get_current_player_name())
    # game.play_game("Adam", (2, 5), (3, 6))
    # game.play_game("Lucy", (2, 7), (6, 3))  # Triple king jump (two pieces)

    game.print_board()

    print("Lucy captured: " + str(player_2.get_captured_pieces_count()))
    print("Lucy king count: " + str(player_2.get_king_count()))
    print("Lucy tripe king count: " + str(player_2.get_triple_king_count()))
    print("Adam captured: " + str(player_1.get_captured_pieces_count()))
    print("Adam king count: " + str(player_1.get_king_count()))
    print("Adam triple king count: " + str(player_1.get_triple_king_count()))

    print(game.game_winner())

    # while game.game_winner() is False:
    #     try:
    #         start_coord = input("Please enter starting coordinate (x,y): ").split(",")
    #         dest_coord = input("Please enter destination coordinate (x,y): ").split(",")
    #         start_x, start_y = start_coord[0], start_coord[1]
    #         dest_x, dest_y = dest_coord[0], dest_coord[1]
    #         game.play_game(player_name, (start_x, start_y), (dest_x, dest_y))
    #     except:
    #         print("This is an invalid move, please re-enter")
    #         starting_coord = input("Please enter starting coordinate (x,y): ").split(",")
    #         dest_coord = input("Please enter destination coordinate (x,y): ").split(",")



if __name__ == "__main__":
    main()