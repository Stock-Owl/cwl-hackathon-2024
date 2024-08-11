# Baseclass and interface for the typing UI

class Typer:
    # __init__ at line: 161
    #methods and constructor from line: 74

    # static data and functions, static member classes
    ESC: str = '\x1B'
    class Color_256:
        """
        Refer to
        [this site](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#256-colors)
        for color codes
        """
        def SetForeground(color_code: str | int) -> str:
            if type(color_code) is int:
                color_code = str(color_code)
            return f"{Typer.ESC}[38;5;{color_code}m"
    
        def SetBackground(color_code: str | int) -> str:
            if type(color_code) is int:
                color_code = str(color_code)
            return f"{Typer.ESC}[48;5;{color_code}m"
        
        # original colors (root_colors) should always be passed from parent Typer object
        def ChangeColor(
                string: str,
                foreground_color: str | None,
                background_color: str | None,
                root_colors: tuple[str, str]
            ) -> str:

            if foreground_color is None:
                foreground_color = root_colors[0]
            if background_color is None:
                foreground_color = root_colors[1]

            set_colors: str = f"{Typer.ESC}[38;5;{foreground_color}m{Typer.ESC}[48;5;{background_color}m"
            restore_colors: str = f"{Typer.ESC}[38;5;{root_colors[0]}m{Typer.ESC}[48;5;{root_colors[1]}m"
            return f"{set_colors}{string}{restore_colors}"
        
    class Color_16:
        def SetForeground(color_code: tuple[str, str]) -> str:
            return f"{Typer.ESC}[{color_code[0]}m"

        def SetBackground(color_code: tuple[str, str]) -> str:
            return f"{Typer.ESC}[{color_code[1]}m"
    
        # note: we could just store the codes as ints for the foregound and
        # just add 10 for background codes and then convert them to strings
        # went with this for now

        # first num is foreground, second is background
        Black: tuple[str, str] = ('30', '40')
        Red: tuple[str, str] = ('31', '41')
        Green: tuple[str, str] = ('32', '42')
        Yellow: tuple[str, str] = ('33', '43')
        Blue: tuple[str, str] = ('34', '44')
        Magenta: tuple[str, str] = ('35', '45')
        Cyan: tuple[str, str] = ('36', '46')
        White: tuple[str, str] = ('37', '47')

        class Bright:
            # first num is foreground, second is background
            Black: tuple[str, str] = ('90', '100')
            Red: tuple[str, str] = ('91', '101')
            Green: tuple[str, str] = ('92', '102')
            Yellow: tuple[str, str] = ('93', '103')
            Blue: tuple[str, str] = ('94', '104')
            Magenta: tuple[str, str] = ('95', '105')
            Cyan: tuple[str, str] = ('96', '106')
            White: tuple[str, str] = ('97', '107')

    # methods and instanciated member classes
    class State:
        def __init__(self, text: list[str], current_line_idx: int = 0):     # -> State
            self.text = text
            self.text_length = len(text)
            if current_line_idx >= self.text_length:
                current_line_idx = 0
            self.current_line_idx = current_line_idx
            self.current_line = text[current_line_idx]

        def RefreshCurrentLine(self) -> None:
            # this shouldn't ever need to be ran, but just in case
            if self.current_line_idx >= self.text_length:
                self.current_line_idx = None
                return
            self.current_line = self.text[self.current_line_idx]

        def GetCurrentLine(self) -> str | None:
            if self.current_line_idx >= self.text_length:
                return None
            return self.current_line

        # next lines
        def Next(self) -> int | None:
            # we could instead return None by default
            # and return an Exception if the end of text is reached
            # I did it like this to differentiate the
            # end of text from a succesfull operation by return type
            if self.current_line_idx >= self.text_length:
                self.current_line = None
                return None
            self.current_line_idx += 1
            # refresh current line
            self.current_line = self.text[self.current_line_idx]
            return self.current_line_idx

        def GetNextLine(self) -> str | None:
            """
            Gets the next line as a string.\n
            **Does not switch to the next line in the State instance**\n
            Returns None if there's no next line.
            """
            if self.current_line_idx >= self.text_length:
                return None
            return self.text[self.current_line_idx + 1]

        def GetNextNLines(self, number_of_lines: int) -> list[str | None]:
            # returns None at the position the text ends
            next_lines: list[str | None] = []
            for i in range(1, number_of_lines + 1):
                if (self.current_line_idx + i) >= self.text_length:
                    next_lines.append(None)
                    return next_lines
                next_lines.append(self.text[self.current_line_idx + i])
            return next_lines

        # previous lines
        def Previous(self) -> int:
            """Returns 0 if out of bounds"""
            if self.current_line_idx < 1:
                self.current_line = self.text[0]
                self.current_line_idx = 0
                return 0
            self.current_line_idx -= 1
            # refresh current line
            self.current_line = self.text[self.current_line_idx]
            return self.current_line_idx

        def GetPreviousLine(self) -> str | None:
            """
            Gets the previous line as a string.\n
            **Does not switch to the previous line in the State instance**\n
            Returns None if there's no previous line.
            """
            if self.current_line_idx < 1:
                return None
            return self.text[self.current_line_idx - 1]

        def GetpreviousNLines(self, number_of_lines: int) -> list[str | None]:
            # returns None at the position the text ends
            prev_lines: list[str | None] = []
            for i in range(1, number_of_lines + 1):
                if (self.current_line_idx - i) < 0:
                    prev_lines.append(None)
                    return prev_lines
                prev_lines.append(self.text[self.current_line_idx - i])
            return prev_lines

    def __init__(self, text: str, path: bool = False, displayed_lines: int = 3):
        self.text: list[str]
        self.num_lines: int
        self.displayed_lines: int   # should we cap this at 10?
        self.current_line: list[str] # length should be between 1 and 3

        if path:
            with open(path, mode='r', encoding='utf-8') as f:
                self.text = f.read().split('\n')
        else:
            self.text = text.split('\n')
        
        self.num_lines = len(self.text)
        if displayed_lines < 1:
            self.displayed_lines = 1
        else:
            self.displayed_lines = displayed_lines
        self.current_line = self.text[0]

    def Start(self):
        pass

    def __str__(self):
        pass
