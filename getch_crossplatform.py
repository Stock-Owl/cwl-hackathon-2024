import sys

# we will need to rename this [Pickle]
# btw very fucking clean code, very based (:

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
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x03': raise KeyboardInterrupt
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def _GetchWindows():
    import msvcrt
    return msvcrt.getch()


getch = _Getch
