from getch_crossplatform import *
from maths_lib import Vector2
import random
import os
import subprocess
import sys


# Created by TheHerowither, based on (https://en.wikipedia.org/wiki/Minesweeper_(video_game))

class MinesweeperSquare:
    def __init__(self, value : int = 0) -> None:
        self.opened = False
        self.value = value
        self.is_bomb = False    # redundant field [Pickle]


def print_square(square : MinesweeperSquare, end : str = "\n", is_selected : bool = False):
    if square.opened:
        if square.is_bomb:
            if is_selected: print(f"\033[47m\033[30m▣\033[0m", end = end)
            else: print("▣", end = end)
        else:
            if is_selected: print(f"\033[47m\033[30m{square.value}\033[0m", end = end)
            else: print(square.value, end = end)
    else:
        if is_selected: print(f"\033[47m\033[30m■\033[0m", end = end)
        else: print("■", end = end)

class Minesweeper:
    def __init__(self, size : str | tuple[int, int] | Vector2 = "10x10") -> None:
        self.size : Vector2
        if type(size) == str:
            sz = size.split("x")
            self.size = Vector2(int(sz[0]), int(sz[1]))
        elif type(size) == tuple:
            self.size = Vector2(size[0], size[1])
        elif type(size) == Vector2:
            self.size = size
        else:
            raise TypeError("Please only use either string, tuple or Vector2 to set Minesweeper size")

        self.board : list[MinesweeperSquare] = []
        self.cursor : Vector2 = Vector2(0, 0)

    def generate_board(self, num_bombs : int):
        for x in range(0, self.size.x * self.size.y):
            self.board.append(MinesweeperSquare(0))

        bombs = 0
        for i in range(0, num_bombs):
            idx = random.randint(0, len(self.board)-1)
            while not self.board[idx].is_bomb:
                if not self.board[idx].is_bomb:
                    self.board[idx].is_bomb = True
                    bombs += 1
                    break
                idx = random.randint(0, len(self.board)-1)

    def update(self):
        for square_idx in range(1, len(self.board)+1):
            idx = self.cursor.y * self.size.y + self.cursor.x
            if square_idx % self.size.x == 0: print_square(self.board[square_idx-1], is_selected=square_idx-1 == idx)
            else: print_square(self.board[square_idx-1], end = "", is_selected=square_idx-1 == idx)

    def run(self):
        running = True
        while running:
            try:
                subprocess.call('clear' if os.name == 'posix' else 'cls')
                self.update()
                c = getch()
                if c == '\033':
                    getch()
                    match getch():
                        case 'A':
                            if self.cursor.y > 0: self.cursor.y -= 1
                        case 'B':
                            if self.cursor.y < self.size.y-1: self.cursor.y += 1

                        case 'C':
                            if self.cursor.x < self.size.x-1: self.cursor.x += 1
                        case 'D':
                            if self.cursor.x > 0: self.cursor.x -= 1
                elif (c == '\n' or c == '\n\r' or c == '\r'):
                    self.board[self.cursor.y * self.size.y + self.cursor.x].opened = True
            except KeyboardInterrupt:
                sys.exit(0)

# [Pickle]:
# comment this shit out before you commit.
# local testing code should always be removed or commented out
# if I import this lib, it will run and fuck shit up
if __name__ == "__main__":
    game = Minesweeper("9x9")
    game.generate_board(10)

    game.run()
