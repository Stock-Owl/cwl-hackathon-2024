# static data and functions
class Typer:
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

# methods
class Typer:
    def __init__(self, text: str, path: bool = False):
        self.text: list[str]
        if path:
            with open(path, mode='r', encoding='utf-8') as f:
                self.text = f.read().split('\n')
        else:
            self.text = text.split('\n')

    def Start(self):
        pass

    def __str__(self):
        pass

print("\x1B[41;36m stuff")
