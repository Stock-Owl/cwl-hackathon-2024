import sys
import re
from arguments_class import Arguments
import defaults

_internal_arguments: str = sys.argv

def process_args(args: list[str]) -> Arguments:
    returned_arguments: Arguments = Arguments()

    # I fucked up the original implementation but I have no time so this is the fix I have for it
    args = " ".join(args)

    split_args: list[str] = args.split(' ')
    returned_arguments.directory = split_args[0]
    split_args.pop(0)
    args = " ".join(split_args)

    regex_return: list[str] = re.findall("[-]. [^-]*", args)
    for each in regex_return:
        pair: str = each.strip()
        flag: str = pair.removeprefix('-')[0]
        value: str = pair.removeprefix('-')[2:]
        match flag:
            case "p":
                if value == "":
                    print("Path wasn't specified after -p argument")
                    exit(0)
                returned_arguments.path_specified = value.strip("\"")
            case "t":
                returned_arguments.text_specified = value.strip()
            case "w":
                try:
                    i_val: int = int(value)
                    if i_val < 44:
                        returned_arguments.max_line_width = "60"
                    else:
                        returned_arguments.max_line_width = value
                except ValueError:
                    returned_arguments.max_line_width = "60"
            case "l":
                try:
                    i_val: int = int(value)
                    if i_val < 0:
                        returned_arguments.trim_text = "0"
                    else:
                        returned_arguments.trim_text = value
                except ValueError:
                    returned_arguments.trim_text = "0"
            case "m":
                returned_arguments.mode = "mine"
                if value == "":
                    returned_arguments.mode_init_value = "easy"
                else:
                    returned_arguments.mode_init_value = value
            case "s":
                returned_arguments.mode = "score"
                try:
                    i_val: int = int(value)
                    if i_val < 100:
                        returned_arguments.mode_init_value = "200"
                    else:
                        returned_arguments.mode_init_value = value
                except ValueError:
                    returned_arguments.mode_init_value = "1000"
            case "b":
                returned_arguments.mdoe = "bin"
                if value.upper() in defaults.binary_operations:
                        returned_arguments.mode_init_value = value.upper()
                else:
                    returned_arguments.mode_init_value = "XOR"
            case _:
                print(f"Invalid flag: -{flag}")
                exit(0)

    if returned_arguments.mode is None:
        modes: list[str] = ["score", "bin", "mine"]
        init_vals: list[str] = ["1000", "XOR", "easy"]
        from random import randint
        rand: int = randint(0, 3)
        returned_arguments.mode = modes[rand]
        returned_arguments.mode_init_value = init_vals[rand]

    if returned_arguments.text_specified is None and returned_arguments.path_specified is None:
        returned_arguments.text_specified = defaults.bee_movie_script

    del regex_return
    return returned_arguments

if __name__ == "__main__":
    arguments: Arguments = process_args(_internal_arguments)
    print()
