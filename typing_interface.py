# Made by [Pickle]
# Baseclass and interface for the typing UI

# shit's about to get real when you see this crap
import re

class Typer:
    
    # __init__ at line: 226
    #methods from line: 305

    # static data and functions, static member classes
    ESC: str = '\x1B'

    # ColorContainer is for readability
    # Effect on performance is negligeable
    class ColorContainer:
        def __init__(self, foreground_color: str = "", background_color: str = ""):
            self.foreground_color = foreground_color
            self.background_color = background_color

        def __str__(self):
            return f"{self.foreground}{self.background}"

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
        
        # original colors (original_colors) should always be passed from parent Typer object
        def ChangeColor(
                string: str,
                colors: tuple[str | None, str | None],
                original_colors: tuple[str, str]
            ) -> str:

            if colors == original_colors:
                return string
            if colors[0] is None:
                colors[0] = original_colors[0]
            if colors[1] is None:
                colors[1] = original_colors[1]

            # second one is always the background color, so we add 10
            colors[1] += 10
            original_colors[1] += 10

            set_colors: Typer.ColorContainer = Typer.ColorContainer(
                foreground_color = f"{Typer.ESC}[38;5;{colors[0]}m",
                background_color = f"{Typer.ESC}[48;5;{colors[1]}m"
                )
            restore_colors: Typer.ColorContainer = Typer.ColorContainer(
                foreground_color = f"{Typer.ESC}[38;5;{original_colors[0]}m",
                background_color = f"{Typer.ESC}[48;5;{original_colors[1]}m"
                )
            return f"{str(set_colors)}{string}{str(restore_colors)}"
        
    class Color_16:
        def SetForeground(color_code: int) -> str:
            return f"{Typer.ESC}[{str(color_code)}m"

        def SetBackground(color_code: tuple[str, str]) -> str:
            return f"{Typer.ESC}[{str(color_code + 10)}m"
        
        def ChangeColor(
                string: str,
                colors: tuple[int | None, int | None],
                original_colors: tuple[int, int]
            ) -> str:

            if colors == original_colors:
                return string
            if colors[0] is None:
                colors[0] = original_colors[0]
            if colors[1] is None:
                colors[1] = original_colors[1]

            # second one is always the background color, so we add 10
            colors[1] += 10
            original_colors[1] += 10

            set_colors: Typer.ColorContainer = Typer.ColorContainer(
                foreground = f"{Typer.ESC}[{str(colors[0])}m",
                background = f"{Typer.ESC}[{str(colors[1])}m"
                )
            restore_colors: Typer.ColorContainer = Typer.ColorContainer(
                foreground = f"{Typer.ESC}[{str(original_colors[0])}m",
                background = f"{Typer.ESC}[{str(original_colors[1])}m"
                )
            
            return f"{str(set_colors)}{string}{str(restore_colors)}"

        Black: int = 30
        Red: int = 31
        Green: int = 32
        Yellow: int = 33
        Blue: int = 34
        Magenta: int = 35
        Cyan: int = 36
        White: int = 37

        class Bright:
            # first num is foreground, second is background
            Black: int = 90
            Red: int = 91
            Green: int = 92
            Yellow: int = 93
            Blue: int = 94
            Magenta: int = 95
            Cyan: int = 96
            White: int = 97

    # methods and instanciated member classes
    class State:
        def __init__(self, text: list[str], current_line_idx: int = 0):     # -> State
            self.text = text
            self.text_length = len(text)
            if current_line_idx >= self.text_length:
                current_line_idx = 0
            self.current_line_idx = current_line_idx
            self.current_line = text[current_line_idx]

        # -> str, a shocker, right?
        def __str__(self) -> str:
            # the class itself shouldn't be accessed by anything other than a Typer owner
            # so we're not giving a damn about ouputting self.text

            return_string: str = f"State object at <{hex(id(self))}> | Memory allocated: {self.__sizeof__()} bytes\n" + \
                f"Length: {self.text_length} lines\n" + \
                f"Current line:\n\"{self.text[self.current_line_idx]}\" # {self.current_line_idx}"
            
            before_refresh_line: str = self.text[self.current_line_idx]
            self.RefreshCurrentLine() # refresh just in case
            if self.text[self.current_line_idx] == before_refresh_line:
                return_string += \
                    f"\nCurrent line after refreshing:\n\"{self.text[self.current_line_idx]}\" # {self.current_line_idx}"

            return return_string

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
                self.current_line_idx = None
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

    def __init__(
            self,
            text: str,
            path: bool = False,
            trim_text: int = 0,
            max_line_width: int = 60
        ):
        
        processed_text: list[str]
        
        self.path_to_source_file: str | None
        self.buffer: list[str] = []
        self.displayed_lines: int   # should we cap this at 10?
        self.max_line_width: int
        self.state: Typer.State     # State is read-only
        
        # ONLY used for the formatting process
        def split_long_lines(string: str, max_length: int) -> list[str]:
            out: list[str] = []
            idx: int = max_length - 1 # we start at the exact position we need to start at
            while True:
                if len(string) < max_length:
                    out.append(string)
                    break
                if string[idx] == " ":
                    out.append(string[:idx])
                    string = string[idx:]
                    idx = max_length - 1
                idx -= 1
            return out

        def enforce_line_width(text: list[str], max_length: int) -> list[str]:
            if not isinstance(text, list):
                return split_long_lines(text, max_length)
            output_list: list[str] = []
            previous_line: str = ""
            for current_line in text:
                current_line = " " + current_line.strip()
                if len(current_line) > max_length:
                    output_list.append(previous_line)
                    enforced_output: list[str] = split_long_lines(current_line, max_length)
                    for enforced_line in enforced_output:
                        output_list.append(enforced_line)
                    previous_line = ""
                    continue
                if (len(previous_line) + len(current_line)) > max_length:
                    output_list.append(previous_line)
                    previous_line = ""
                previous_line += current_line
            return output_list

        # we'll format the separated lines

        if path:
            try:
                with open(text, mode='r', encoding='utf-8') as f:
                    content: str = f.read()
                    # splits at any punctuation (,.?!:;)
                    post_regex_text = re.findall("[^,.?!:;]*[,.?!:;]", content)
                    # if there isn't any punctuation, then regex will return []
                    if post_regex_text == []:
                        processed_text = enforce_line_width(content, max_line_width)
                    else:
                        processed_text = enforce_line_width(post_regex_text, max_line_width)
                    self.path_to_source_file = text
            except FileNotFoundError:
                print(f"File wasn't found. Path: \"{text}\"")
                exit(0)
            except:
                print(f"File found but it couldn't be opened. Path: \"{text}\"")
                exit(0)
        else:
            post_regex_text = re.findall("[^,.?!:;]*[,.?!:;]", text)
            # if there isn't any punctuation, then regex will return []
            if post_regex_text == []:
                processed_text = enforce_line_width(text, max_line_width)
            else:
                processed_text = enforce_line_width(post_regex_text, max_line_width)
            self.path_to_source_file = None
        
        if trim_text > 0 and trim_text < len(processed_text - 1):
            processed_text = processed_text[:trim_text]

        self.displayed_lines = 3

        self.max_line_width = max_line_width

        self.state = Typer.State(processed_text)

    def __str__(self) -> str:
        # hacks to modify the str() return for self.state
        state_split: list[str] = str(self.state).split("\n")
        state_str: str = ""
        for i in range(len(state_split)):
            line: str = state_split[i]
            if i == 0:
                # this is dirty as hell
                state_str += f"\t{line}\n\tProperty of Typer object at <{hex(id(self))}>\n"
                continue
            if i == 1:
                if self.path_to_source_file is None:
                    # the text isn't from a file then
                    continuation: str = "[...]" if self.state.text_length > 0 else ""   # this is disgusting as well
                    state_str += f"\t\"{self.state.text[0]} {continuation}\"\n"
                else:
                    state_str += f"\tPath of text source file: \"{self.path_to_source_file}\"\n"
                state_str += f"\t{line}\n"
                continue
            state_str += f"\t{line}\n"
        
        del line    # to prevent accidental accesses, just in case

        displayed_str: str = "\n".join(self.Refresh())

        return_string: str = f"Typer object at <{hex(id(self))}> | Memory allocated: {self.__sizeof__()} bytes\n" + \
        f"Maximum line widht: {self.max_line_width} characters | {self.displayed_lines} lines displayed\n" + \
        f"Currently displayed lines (not centered):\n\"{displayed_str}\"\n" + \
        f"State:\n{state_str}" 
        
        return return_string

    def Refresh(self) -> list[str]:
        displayed: list[str] = []
        line_idx: int | None = self.state.current_line_idx
        if line_idx is None:
            displayed = self.state.text[len(self.state.text_length) - 3:]
        if line_idx == 0:
            displayed = self.state.text[0:3]
        elif line_idx >= self.state.text_length - 1:
            displayed = self.state.text[len(self.state.text_length) - 3:]
        else:
            displayed = self.state.text[line_idx-2 : line_idx+1]

        return displayed

    def Forward(self) -> list[str]:
        self.state.Next()
        return self.Refresh()
    
    def Back(self) -> list[str]:
        self.state.Previous()
        return self.Refresh()

    def ReachedEndOfText(self) -> bool:
        return (self.state.current_line_idx is None)

if __name__ == "__main__":
    t = Typer("Árvíztűrő tükörfúró gép. Hósszú utca girbe gurba minden sarkon áll egy [redacted]. Egy vekni kenyér, egy üveg tej és egy kocka vaj. Egy vekni tej, egy üveg kenyér és egy kismocsok DVD. Egy kismocsok DVD és a kincs az antikváriumból.")
    # print(t)
    for j in t.Forward():
        print(j)
