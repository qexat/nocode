import os
import subprocess
from io import TextIOWrapper
from typing import Literal

from nocode.compiler import compile


PS1 = "\x1b[1m>>\x1b[22m "


def run(file: TextIOWrapper, *, cli_mode: bool = True) -> int:
    TMP_FILE = "/tmp/_nocode_out.py"
    try:
        compile(file, output=TMP_FILE, target="py")
    except SystemExit:
        return 1
    else:
        if cli_mode:
            print(f"Running: {file.name}")
        subprocess.run(["python", "-B", TMP_FILE])
        os.unlink(TMP_FILE)

    return 0


def _clear_repl() -> Literal[False]:
    print("\r\x1b[0;0H\x1b[2J")
    return False


def _pretty_command(name: str, description: str) -> str:
    return f"\r    \x1b[35m{name}\x1b[39m: {description}"


def _print_help() -> None:
    print(
        f"""Available commands:
        {_pretty_command("clear", "clears the screen.")}
        {_pretty_command("exit", "exits the console.")}"""
    )


def _print_incipit() -> Literal[True]:
    print("\x1b[34mType 'help' to get available commands.\x1b[39m")
    return True


def repl() -> int:
    visible_incipit = _print_incipit()
    try:
        while (user_input := input(PS1)) != "exit":
            if user_input == "help":
                _print_help()
            elif user_input == "clear":
                print("\r\x1b[0;0H\x1b[2J")
                visible_incipit = _clear_repl()
            elif user_input:
                print(
                    f"\x1b[31mSyntaxError: unexpected character '{user_input[0]}' at pos 1\x1b[39m"
                )
            if not visible_incipit:
                visible_incipit = _print_incipit()
    except KeyboardInterrupt:
        print()
    except Exception:
        return 1
    return 0
