import sys

# we will need to rename this [Pickle]

# Windows
if sys.platform == "win32":
    import msvcrt
    def _Getch() -> str:
        return str(msvcrt.getch())
    
    def _Getch_Bytes() -> bytes:
        return msvcrt.getch()

# Unix
else:
    import sys, tty, termios
    def _Getch() -> str:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x03': raise KeyboardInterrupt
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
    def _Getch_Bytes() -> bytes:
        return bytes(_Getch(), encoding = "utf-8")

getch = _Getch
getch_bytes = _Getch_Bytes
