from io import TextIOWrapper

from result import Err, Ok, Result

from nocode.filem import strip_text


def format(file: TextIOWrapper, *, fd_close: bool) -> Result[None, Exception]:
    return strip_text(file, fd_close=fd_close)


def _format_wrapper(file: TextIOWrapper, *, fd_close: bool) -> int:
    match (r := format(file, fd_close=fd_close)):
        case Ok():
            print(f"    Successfully formatted {file.name!r}.")
            return 0
        case Err():
            print(f"    Failed to format {file.name!r}: {r.err()}.")
            return 1


def auto_format(file: TextIOWrapper) -> int:
    return _format_wrapper(file, fd_close=False)


def format_cli(file: TextIOWrapper) -> int:
    return _format_wrapper(file, fd_close=True)
