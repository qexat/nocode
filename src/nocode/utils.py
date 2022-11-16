from sys import stderr


DEFAULT_OUTPUT_NAME = "output"
DEFAULT_OUTPUT_EXT_IF_BIN = "bin"


def determine_output_file(path: str, output_lang: str | None = None) -> str:
    """
    Given an input file path and an output lang, determine the name of the output file.

    Performs some checks to prevent file conflicts, i.e. when the input and the output files share the same path.

    Args:
        path (str): the path of the input file.
        output_lang (str | None, optional): the stem corresponding to the output file lang. Defaults to None.

    Returns:
        str: name of output file.
    """

    _, name, _ = split_path(path)
    output_name = name or DEFAULT_OUTPUT_NAME

    if path == output_name:
        output_lang = output_lang or DEFAULT_OUTPUT_EXT_IF_BIN
    elif output_lang is None:
        return output_name
    return f"{output_name}.{output_lang}"


def split_path(path: str) -> tuple[list[str], str | None, str | None]:
    """
    Split a path between the folders, the file name and the stem (the file extension).

    Note: This function does NOT handle paths that end with a forward slash (e.g. directories) and is prone to erroring.

    Args:
        path (str): the path to split.

    Returns:
        tuple[list[str], str | None, str | None]: the list of folders, the file name if any and the stem if any.
    """

    *folders, file = path.split("/")
    *name_parts, stem = file.split(".")

    # If the file ends with a dot, we add it to its name
    if not stem:  # not stem <=> stem == "" (empty string)
        name_parts.append(stem)

    return (
        folders,
        ".".join(name_parts) if name_parts else stem if "." not in file else None,
        stem
        if "." in file[:-1]  # little trick in case if the file name ends with a period
        else None,
    )


def summary(exit_code: int) -> None:
    message = f"%sExited.\x1b[39m"
    if not exit_code:
        print(message % "\x1b[32m")
    else:
        print(message % "\x1b[31m", file=stderr)
