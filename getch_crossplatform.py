import sys

# we will need to rename this [Pickle]

def _Getch() -> str:
    if sys.platform == "win32":
       return _GetchWindows()
    else:
        return _GetchUnix()


def _GetchUnix() -> str:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
       termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def _GetchWindows():
    import msvcrt
    return msvcrt.getch()


getch = _Getch
