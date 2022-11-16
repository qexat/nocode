import ast
from io import TextIOWrapper
from typing import Literal

from result import Err, Ok, Result

from nocode.errors import syntax_error_known_location
from nocode.filem import read_text
from nocode.utils import determine_output_file


SUPPORTED_TARGETS = ("bin", "c", "cpp", "py")
CompilerTarget = Literal["bin", "c", "cpp", "py"] | None


def parse(file: TextIOWrapper) -> Result[ast.Module, Exception]:
    match (r := read_text(file, fd_close=True)):
        case Ok():
            source = r.unwrap()
        case Err():
            return r

    return Ok(parse_source(source, file_name=file.name))


def parse_source(source: str, *, file_name: str = "<string>") -> ast.Module:
    sourcelines = source.splitlines(keepends=True)

    if source:
        syntax_error_known_location(
            file_name, sourcelines[0], 0, 0, 1, f"unexpected character {source[0]!r}"
        )

    return ast.parse(source)


def compile(
    file: TextIOWrapper,
    *,
    output: str | None,
    target: CompilerTarget,
    cli_mode: bool = False,
) -> int:
    output_file_name = output or determine_output_file(file.name, target)

    if cli_mode:
        print(f"Compiling:\n    {file.name} -> {output_file_name}")

    match (result := parse(file)):
        case Ok():
            tree = result.unwrap()
        case Err():
            print(result)
            return 1

    with open(output_file_name, "w") as output_file:
        contents: str = ""
        match target:
            case "bin" | None:  # TODO
                ...
            case "c":
                contents = generate_c_code(tree)
            case "cpp":
                contents = generate_c_code(tree)
            case "py":
                contents = ast.unparse(tree)
        output_file.write(contents)

    return 0


def generate_c_code(tree: ast.Module) -> str:
    return f"int main(void) {{return 0;}}\n"
