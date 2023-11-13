"""
Prenom:<Konstantinos>
Nom: <Vanakas>
Matricule: <000565802>
Date: 15/11/2023
Gaol: Create a minesweeper game with a GUI and adapting difficulty by the use of a class
!!!Most part of the code's logic and structure was reused from a last year project of the same game but without the
difficulty choice and the bombs position changes and with the system of flags. So most of the code was adapted to the
new requirements.
The previous project was the first required in the course of INFO-F-106 of the academic year 2022/2023!!!
"""
import string as s
from random import *


class Minesweeper:
    def __init__(self, difficulty):
        """this function allows to initialize the game with the difficulty chosen by the player
         creating also the board and the reference board which will be used to check the number
         of mines around a case"""
        self.in_game = True
        self.diff = difficulty
        if self.diff == 0:
            self.size = 9
        else:
            self.size = int(input("Enter the size of the board: "))
        self.board = [['*' for i in range(self.size)] for j in range(self.size)]
        self.ref_board = [[0 for i in range(self.size)] for j in range(self.size)]
        self.nbombs = 0
        self.place_mines()
        self.fill_in_board()

    def print_board(self):
        """this function  allow us to print the board while cycling at every move of the player  with the frame and the
        number representing the dimensions, also those numbers allow to write the coordinate which will
        be defined later on this code."""
        board = self.board
        alphabet = list(list(s.ascii_uppercase))
        print(' ' * 44, end='')  # spaces needed for the dozens to start at the right place
        for i in range(len(board[0])):  # we calculate the dozens if there's a need and print them on the right place
            if i >= 10:
                if i // 10 != 0:
                    print(' ', i // 10, end=' ')
        print((' ' * 24))
        print(' ' * 4, end='')
        for k in range(len(board[0])):  # we calculate the units with a modulo and print them
            print(' ', k % 10, end=' ')
        print('\n', ' ' * 2, "—" * (len(board[0]) * 4 + 1))
        for j in range(len(board)):
            if j < 26:
                ltr = alphabet[j]
                print(" ", ltr, '|', end=' ')
                for l in range(len(board[j])):
                    print((board[j][l]), "|", end=' ')
                print()
            else:
                ltr = alphabet[j // 26 - 1]
                ltr1 = alphabet[j % 26]
                print(ltr1, ltr, '|', end=' ')
                for l in range(len(board[j])):
                    print((board[j][l]), "|", end=' ')
                print()
        print(' ' * 3, "—" * ((len(board[0])) * 4 + 1))

    def get_neighbors(self, board, pos_x, pos_y):
        """this function allows to get the neighbors of a case and return them into a list"""
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (pos_x + i >= 0 and pos_y + j >= 0) and (pos_x + i <= len(board) and pos_y + j <= len(board[0])) or (
                        pos_x + i
                        <= 0 and pos_y + j <= len(board[0])) and (pos_x + i <= len(board) and pos_y + j < 0):
                    pos = (pos_x + i, pos_y + j)
                    neighbors.append(pos)
                    if pos == (pos_x, pos_y) or (pos_x + i < 0) or (pos_y + j < 0) or (pos_x + i == self.size) or (
                            pos_y + j == self.size):
                        neighbors.remove(pos)
        return neighbors

    def generate_random_pos(self):
        """this function allows to generate random positions for the mines return them into a dictionary
        and the requierd number of mines depends on the difficulty"""
        nb_bombs = (self.size ** 2) // 5
        corners = {(self.size-1, self.size-1), (0, 0), (0, self.size-1), (self.size-1, 0)}
        li = []
        for i in range(nb_bombs):
            pos = (randint(0, self.size-1), randint(0, self.size-1))
            while pos in corners or pos in li:
                pos = (randint(0, self.size-1), randint(0, self.size-1))
            li.append(pos)
        return li

    def place_mines(self):
        difficulty = self.diff
        ref_board = self.ref_board
        if difficulty == 0:
            self.nbombs = 0
            with open('bombes.txt', 'r') as f:
                for line in f:
                    line = line.split(',')
                    ref_board[int(line[0])][int(line[1])] = 'B'
                    self.nbombs += 1
        elif difficulty == 1 or difficulty == 2:
            bombs = self.generate_random_pos()
            self.nbombs = len(bombs)
            for pos in bombs:
                ref_board[pos[0]][pos[1]] = 'B'
        self.ref_board = ref_board
        return ref_board

    def count_mine(self, ref_board, pos_x, pos_y):
        """this function calculates the number of mine around a case and return the number into a string"""
        nbr = 0
        for i in self.get_neighbors(ref_board, pos_x, pos_y):
            if ref_board[i[0]][i[1]] == 'B':
                nbr += 1
        return str(nbr)

    def fill_in_board(self):
        """this function print the mines and the values of each case into the reference_board"""
        ref_board = self.ref_board
        for i in range(len(ref_board)):
            for j in range(len(ref_board[0])):
                if ref_board[i][j] != 'B':
                    ref_board[i][j] = self.count_mine(ref_board, i, j)
        self.ref_board = ref_board
        return ref_board

    def parse_input(self, col, line):
        """this function allows to convert the input of the player into a tuple of int"""
        alphabet = list(s.ascii_uppercase)
        if line in alphabet:
            line = alphabet.index(line)
        else:
            col = int(col)
        col = int(col)
        return line, col

    def propagate_click(self, pos_x, pos_y):
        """this function allows to open a case and all the 8 cases around it if there's no mine around it"""
        board= self.board
        ref_board = self.ref_board
        if ref_board[pos_x][pos_y] == 'B':
            return board
        elif ref_board[pos_x][pos_y] != 'B':
            board[pos_x][pos_y] = ref_board[pos_x][pos_y]
            if ref_board[pos_x][pos_y] == '0':
                for i in self.get_neighbors(ref_board, pos_x, pos_y):
                    if board[i[0]][i[1]] == '*' and ref_board[i[0]][i[1]] != 'B':
                        self.propagate_click(i[0], i[1])
        return board

    def check_win(self):
        """this function checks if the player has won the game"""
        board, ref_board = self.board, self.ref_board
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == '*' and ref_board[i][j] != 'B':
                    return False
        return True

    def move_bombs(self, col,line):
        """this function allows to move the bombs if the player clicks on a bomb at the first move"""
        corners = {(self.size - 1, self.size - 1), (0, 0), (0, self.size - 1), (self.size - 1, 0)}
        li = {}
        for i in range(self.nbombs):
            pos = (randint(0, self.size - 1), randint(0, self.size - 1))
            while pos in corners or pos in li or self.board[pos[0]][pos[1]] != '*' or pos == (col, line):
                pos = (randint(0, self.size - 1), randint(0, self.size - 1))
            li[pos] = 'B'
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.ref_board[i][j] == 'B':
                    self.board[i][j] = '*'
                    self.ref_board[i][j] = 0
        for pos in li:
            self.ref_board[pos[0]][pos[1]] = li[pos]
        self.fill_in_board()
        return li

    def continue_game(self):
        """this function allows to continue the game if the player wants to play again"""
        answer = input("Do you want to play again? (y/n): ")
        if answer == 'yes' or answer == 'y' or answer == 'Y' or answer == 'Yes':
            return True
        else:
            return False


def main(difficulty):
    """this function allows to play the game"""
    alphabet = list(s.ascii_uppercase)
    game = Minesweeper(difficulty)

    print('we planted {} bombs'.format(game.nbombs))
    game.print_board()
    while not game.check_win() and game.in_game:
        col = int(input("Choose your column (0 to {}): ".format(game.size -1)))
        line = input("Choose your line (A to {}): ".format(alphabet[game.size - 1])).upper()
        col, line = game.parse_input(col, line)
        if game.ref_board[col][line] == 'B':
            game.in_game = False
        else:
            if difficulty == 2:
                game.move_bombs(col, line)
                game.fill_in_board()
            game.propagate_click(col, line)
            game.fill_in_board()
            game.win = game.check_win()
            game.print_board()
    if game.check_win():
        print("#######################")
        print("You won! Congratulation")
        print("#######################")
    else:
        print("###################")
        print("You lost! Try again")
        print("###################")
    if game.continue_game():
        difficulty = int(input("Choose your difficulty (0 = easy , 1 = normal, 2 = hard): "))
        main(difficulty)
    else:
        print("####################################")
        print("Thank you for playing! See you soon!")
        print("####################################")


if __name__ == '__main__':
    """allow to launch the game by calling the main function and allowing the player to choose the difficulty"""
    print("#######################")
    print("Welcome to Minesweeper!")
    print("#######################")
    diff = int(input("Choose your difficulty (0 = easy , 1 = normal, 2 = hard): "))
    main(diff)