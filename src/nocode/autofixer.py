from io import TextIOWrapper

from result import Err, Ok, Result

from nocode.filem import cut_text


def print_diff(diff: int, /) -> None:
    message = f"Removed {diff} byte(s)." if diff else "File remained unchanged."
    print(f"    {message}")


def autofix(file: TextIOWrapper, *, fd_close: bool) -> Result[int, Exception]:
    """
    Autofixes a NoCode script.

    Args:
        file (TextIOWrapper): the file to autofix.
        fd_close (bool): whether the file should be closed or not.

    Returns:
        Result[int, Exception]
    """

    match (r := cut_text(file, fd_close=fd_close)):
        case Ok():
            return Ok(len(r.unwrap()))
        case Err():
            return r


def autofix_cli(file: TextIOWrapper) -> int:
    """
    Provides an interface for the CLI to the autofixer.

    Args:
        file (TextIOWrapper): the file to autofix.

    Returns:
        int: exit code.
    """

    print(f"Autofixing: {file.name}")
    match (r := autofix(file, fd_close=True)):
        case Ok():
            print(f"    Removed {r.unwrap()} bytes.")
            return 0
        case Err():
            return 1
