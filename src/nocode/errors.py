from sys import stderr
from typing import Literal, Never


Event = Literal["compilation", "execution", "formatting"]


def _prettyline(line: str, spos: int, epos: int) -> str:
    return f"{line[:spos]}\x1b[41m{line[spos:epos]}\x1b[49m{line[epos:]}"


def _prettypos(spos: int, epos: int) -> str:
    return f"{'' * spos}\x1b[31m{'^' * (epos - spos)}\x1b[39m"


def error(
    event: Event,
    file_name: str,
    line: str,
    line_no: int,
    spos: int,
    epos: int,
    kind: str,
    details: str,
    note: str | None = None,
    *,
    error_code: int,
) -> Never:
    print(
        f"""
        \r\x1b[31m[ERROR]\x1b[39m An error occured on {event}:
        \r  File \x1b[34m"{file_name}"\x1b[39m, line {line_no + 1}
        \r    {_prettyline(line, spos, epos)}
        \r    {_prettypos(spos, epos)}
        \r{kind}: {details}. {note if note is not None else ""}""",
        file=stderr,
    )
    raise SystemExit(error_code)


def compile_error(
    file_name: str,
    line: str,
    line_no: int,
    spos: int,
    epos: int,
    kind: str,
    details: str,
    note: str | None = None,
    *,
    error_code: int,
) -> Never:
    error(
        "compilation",
        file_name,
        line,
        line_no,
        spos,
        epos,
        kind,
        details,
        note,
        error_code=error_code,
    )


def syntax_error_known_location(
    file_name: str,
    line: str,
    line_no: int,
    spos: int,
    epos: int,
    details: str,
) -> Never:
    compile_error(
        file_name,
        line,
        line_no,
        spos,
        epos,
        "SyntaxError",
        details,
        "Have you written actual code?",
        error_code=1,
    )


def format_error(
    formatted_file_name: str,
    kind: str,
    details: str,
    *,
    error_code: int,
) -> Never:
    cli_line = f"nocode format --file {formatted_file_name}"
    error(
        "formatting", "<stdin>", cli_line, 1, 0, 0, kind, details, error_code=error_code
    )


def format_permission_error(formatted_file_name: str, details: str) -> Never:
    format_error(formatted_file_name, "PermissionError", details, error_code=127)
