from argparse import ArgumentParser, FileType, Namespace

from nocode.autofixer import autofix_cli
from nocode.compiler import compile, SUPPORTED_TARGETS
from nocode.formatter import auto_format, format_cli
from nocode.interpreter import repl, run
from nocode.utils import summary


def init(*, argv: list[str] | None = None) -> Namespace:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")

    # *- COMPILE -* #
    parser_compile = subparsers.add_parser(
        "compile", description="Compile a NoCode script."
    )
    parser_compile.add_argument("file", type=FileType("r+"))
    parser_compile.add_argument("--output", "-o", required=False, default=None)
    parser_compile.add_argument(
        "--target", "-t", choices=SUPPORTED_TARGETS, required=False, default=None
    )
    parser_compile.add_argument(
        "--auto-format", "-af", action="store_true", required=False
    )

    # *- RUN -* #
    parser_run = subparsers.add_parser("run", description="Run a NoCode script.")
    parser_run.add_argument("file", type=FileType("r+"))

    # *- DEPLOY -* #
    parser_deploy = subparsers.add_parser(
        "deploy", description="Deploy your NoCode project."
    )
    parser_deploy.add_argument("--port", type=int, default=8080)

    # *- FORMAT -* #
    parser_format = subparsers.add_parser(
        "format", description="Format your NoCode script to make it more readable."
    )
    parser_format.add_argument("--file", type=FileType("r+"))

    # *- AUTOFIX -* #
    parser_autofix = subparsers.add_parser(
        "autofix",
        aliases=["fix"],
        description="Fix automatically your NoCode script using the power of AI.",
    )
    parser_autofix.add_argument("file", type=FileType("r+"))

    return parser.parse_args(argv)


def main() -> int:
    args = init()

    exit_code = 0

    match args.subcommand:
        case "run":
            exit_code = run(args.file)
        case "compile":
            if not args.auto_format or (exit_code := auto_format(args.file)):
                target = None if args.target == "bin" else args.target
                exit_code = compile(
                    args.file,
                    output=args.output,
                    target=target,
                    cli_mode=True,
                )
        case "deploy":
            return temp_coming_soon("Deploy")
        case "format":
            if args.file is None:
                print("Error: Recursive project formatting is not implemented.")
                exit_code = 1
            else:
                exit_code = format_cli(args.file)
        case "fix" | "autofix":
            exit_code = autofix_cli(args.file)
        case _:  # REPL
            exit_code = repl()

    summary(exit_code)
    return exit_code


def temp_coming_soon(feature: str) -> int:
    print(f"This feature ({feature}) is not ready for the moment.")
    return 1
