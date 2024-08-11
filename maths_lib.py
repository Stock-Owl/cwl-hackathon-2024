import typing   # WHY?! [Pickle]

# Why couldn't this be called GridPos or smth and merged into minesweeper.py? [Pickle]
class Vector2:
    def __init__(self, x : int | float, y : int | float):
        self.x = x
        self.y = y
