from getch_crossplatform import *
from typing_interface import Typer
import random
import os
import subprocess
import sys
import time


########
# DISCLAMER!!!!!!
# I know this code is shit
# i am going to do a refactor as soon as i find time
########

# Created by TheHerowither, based on (https://en.wikipedia.org/wiki/Minesweeper_(video_game))
# TODO: Win condition
# TODO: Point system
# TODO: Major refactor


class GridPos:
    def __init__(self, x : int | float, y : int | float):
        self.x = x
        self.y = y

class MinesweeperSquare:
    def __init__(self, value : int = 0) -> None:
        self.opened = False
        self.value = value
        self.flag = False


def print_square(square : MinesweeperSquare, end : str = "\n", is_selected : bool = False):
    if square.opened:
        if square.value == -1:
            if is_selected: print(Typer.Color_16.SetBackground(Typer.Color_16.White)+Typer.Color_16.SetForeground(Typer.Color_16.Black)+"▣\033[0m", end = end)
            else: print("▣", end = end)
        else:
            if is_selected: print(Typer.Color_16.SetBackground(Typer.Color_16.White)+Typer.Color_16.SetForeground(Typer.Color_16.Black)+f"{square.value}\033[0m", end = end)
            else: print(square.value, end = end)
    else:
        if square.flag:
            if is_selected: print(Typer.Color_16.SetBackground(Typer.Color_16.White)+Typer.Color_16.SetForeground(Typer.Color_16.Black)+"⚑\033[0m", end = end)
            else: print("⚑", end = end)
        else:
            if is_selected: print(Typer.Color_16.SetBackground(Typer.Color_16.White)+Typer.Color_16.SetForeground(Typer.Color_16.Black)+f"■\033[0m", end = end)
            else: print("■", end = end)

class Minesweeper:
    def __init__(self, size : str | tuple[int, int] | GridPos = "10x10") -> None:
        self.size : GridPos
        if type(size) == str:
            sz = size.split("x")
            self.size = GridPos(int(sz[0]), int(sz[1]))
        elif type(size) == tuple:
            self.size = GridPos(size[0], size[1])
        elif type(size) == GridPos:
            self.size = size
        else:
            raise TypeError("Please only use either string, tuple or Vector2 to set Minesweeper size")

        self.board : list[MinesweeperSquare] = []
        self.cursor : GridPos = GridPos(0, 0)

    def generate_board(self, num_bombs : int):
        for x in range(0, self.size.x * self.size.y):
            self.board.append(MinesweeperSquare(0))

        for i in range(0, num_bombs):
            idx = random.randint(0, len(self.board)-1)
            while self.board[idx].value != -1:
                if self.board[idx].value != -1:
                    self.board[idx].value = -1
                    break
                idx = random.randint(0, len(self.board)-1)

        for x in range(0, self.size.x):
            for y in range(0, self.size.y):
                # This is a very dirty solution!
                # TODO: Find a better way of doing this
                if self.board[self.get_idx(x, y)].value != -1:
                    bombs = 0
                    
                    if y >> 0:
                        if self.board[self.get_idx(x,   y-1)].value == -1: bombs += 1
                        if self.board[self.get_idx(x+1, y-1)].value == -1: bombs += 1

                    if x >> 0:
                        if self.board[self.get_idx(x-1, y+1)].value == -1: bombs += 1
                        if self.board[self.get_idx(x-1, y)].value == -1: bombs += 1
    
                    if (x >> 0 and y >> 0):
                        if self.board[self.get_idx(x-1, y-1)].value == -1: bombs += 1

                    if self.board[self.get_idx(x,   y)].value == -1: bombs += 1
                    if self.board[self.get_idx(x+1, y)].value == -1: bombs += 1

                    if self.board[self.get_idx(x,   y+1)].value == -1: bombs += 1
                    if self.board[self.get_idx(x+1, y+1)].value == -1: bombs += 1


                    self.board[self.get_idx(x, y)].value = bombs

                    

                
    def get_idx(self, x : int, y : int) -> int:
        return min(y, self.size.y - 1) * self.size.y + min(x, self.size.x - 1)

    def update(self):
        subprocess.call('clear' if os.name == 'posix' else 'cls')
        for square_idx in range(1, len(self.board)+1):
            idx = self.cursor.y * self.size.y + self.cursor.x
            if square_idx % self.size.x == 0: print_square(self.board[square_idx-1], is_selected=square_idx-1 == idx)
            else: print_square(self.board[square_idx-1], end = "", is_selected=square_idx-1 == idx)

    def board_at(self, x : int, y : int) -> GridPos:
        return self.board[self.get_idx(x, y)]

    def uncover_all(self):
        for i in range(0, len(self.board)):
            self.board[i].opened = True
            time.sleep(0.01)
            self.update()

    def uncover_around(self, pos : GridPos) -> list[GridPos]:
        x = pos.x
        y = pos.y
        ret = []
        if y >> 0:
            if (self.board_at(x,   y-1).value == 0 and not self.board_at(x, y-1).opened):
                ret.append(GridPos(x,   y-1))
                self.board[self.get_idx(x,   y-1)].opened = True

        if x >> 0:
            if (self.board_at(x-1,   y).value == 0 and not self.board_at(x-1, y).opened):
                ret.append(GridPos(x-1,   y))
                self.board[self.get_idx(x-1,   y)].opened = True


        if (self.board_at(x+1, y).value == 0 and not self.board_at(x+1, y).opened):
            ret.append(GridPos(x+1, y))
            self.board[self.get_idx(x+1, y)].opened = True

        if (self.board_at(x,   y+1).value == 0 and not self.board_at(x, y+1).opened):
            ret.append(GridPos(x, y+1))
            self.board[self.get_idx(x,   y+1)].opened = True


        return ret

    def uncover_0s(self):
        lst = self.uncover_around(self.cursor)
        def rec_uncover(lst : list):
            self.update()
            time.sleep(0.01)
            print(len(lst))
            if len(lst) == 0: return
            for q in lst:
                rec_uncover(self.uncover_around(q))
        rec_uncover(lst)

    def run(self):
        running = True
        while running:
            try:
                self.update()
                print(f"Cursor: {self.cursor.x}, {self.cursor.y}")
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
                    if self.board[self.get_idx(self.cursor.x, self.cursor.y)].value == -1:
                        self.uncover_all()
                        self.update()
                        print("GAME OVER!!")
                        running = False;
                    if self.board[self.get_idx(self.cursor.x, self.cursor.y)].value == 0:
                        self.uncover_0s();
                elif c == 'f': 
                    self.board[self.get_idx(self.cursor.x, self.cursor.y)].flag = True
            except KeyboardInterrupt:
                sys.exit(0)



if __name__ == "__main__":
    game = Minesweeper("9x9")
    game.generate_board(10)

    game.run()
