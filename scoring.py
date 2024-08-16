from typing_interface import Typer
from arguments_class import Arguments

def Scoring(args: Arguments):
    t. Typer
    if args.path_specified is not None:
        t = Typer(args.path_specified, path = True, trim_text=args.trim_text, max_line_width=args.max_line_width)
    else:
        t = Typer(args.text, trim_text=args.trim_text, max_line_width=args.max_line_width)

    starting_score: int = int(args.mode_init_value)
    
