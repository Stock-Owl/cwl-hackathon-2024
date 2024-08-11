from getch_crossplatform import *




class TypingBuffer:
    def __init__(self, target_text : str = "The quick brown fox jumps over the lazy dog") -> None:
        self.buffer : str = ""
        self.target_text : str = target_text
        self.cursor_pos : int = 0;

    def update(self):
        print(self.buffer+"\033[1;30m"+self.target_text[self.cursor_pos:]+"\033[0m")

    def add_char(self, c : str):
        self.buffer += c
        self.cursor_pos += 1


if __name__ == "__main__":
    buf : TypingBuffer = TypingBuffer()

    while True:
        buf.update()
        c = getch()
        buf.add_char(c)
