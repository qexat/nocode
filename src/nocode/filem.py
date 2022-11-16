from collections.abc import Callable
from io import TextIOWrapper
from typing import Concatenate, ParamSpec, TypeVar

from result import Err, Ok, Result

P = ParamSpec("P")
R = TypeVar("R")

# *- LOW LEVEL API -* #

# TODO: improve error | custom error system?
_ClosedFileErr = RuntimeError("closed file")
_UnreadableFileErr = RuntimeError("file cannot be read")
_UnwritableFileErr = RuntimeError("file cannot be written")


class FileWrapper:
    @property
    def file(self) -> TextIOWrapper:
        return self._io_wrapper

    def __init__(self, io_wrapper: TextIOWrapper, *, fd_close: bool) -> None:
        self._io_wrapper = io_wrapper
        self._fd_close = fd_close

    def __enter__(self):
        return self

    def __exit__(self, *_):
        if self._fd_close:
            self._io_wrapper.close()

    def read(self, size: int | None = None, /) -> Result[str, Exception]:
        """
        Read the file contents and return them as a string.

        Args:
            size (int | None, optional): the number of bytes to read. Defaults to None.

        """

        if self.file.closed:
            return Err(_ClosedFileErr)
        if not self.file.readable():
            return Err(_UnreadableFileErr)
        return Ok(self.file.read(size))

    def write(self, contents: str, /) -> Result[None, Exception]:
        """
        Write to the file, overwriting existing contents.

        Args:
            contents (str): the contents to write to the file.
        """

        if self.file.closed:
            return Err(_ClosedFileErr)
        if not self.file.writable():
            return Err(_UnwritableFileErr)
        self.file.write(contents)
        return Ok(None)

    def append(self, contents: str, /) -> Result[None, Exception]:
        """
        Append contents to the end of the file.

        Args:
            contents (str): the contents to append to the file.
        """

        match (r := self.read()):
            case Ok():
                new_contents = r.unwrap() + contents
            case Err():
                return r

        return self.write(new_contents)

    def strip(self) -> Result[None, Exception]:
        """
        Strip file contents, i.e. remove any surronding space or newline.
        """

        match (r := self.read()):
            case Ok():
                new_contents = r.unwrap().strip()
            case Err():
                return r

        return self.write(new_contents)

    def erase(self) -> Result[None, Exception]:
        """
        Erase file contents.
        """

        return self.write("")

    def cut(self) -> Result[str, Exception]:
        """
        Erase file contents, but return them as a string.
        """

        match (r := self.read()):
            case Ok():
                contents = r.unwrap()
            case Err():
                return r

        match (e := self.erase()):
            case Ok():
                return Ok(contents)
            case Err():
                return e


def _do_text(
    file: TextIOWrapper,
    op: Callable[Concatenate[FileWrapper, P], R],
    fd_close: bool,
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    with FileWrapper(file, fd_close=fd_close) as filew:
        result = op(filew, *args, **kwargs)
    return result


# *- HIGH LEVEL API -* #


def read_text(
    file: TextIOWrapper, size: int | None = None, *, fd_close: bool
) -> Result[str, Exception]:
    """
    Read the file contents and return them as a string.

    Args:
        file (TextIOWrapper): the file to read.
        size (int | None, optional): the number of bytes to read. Defaults to None.

    Kwargs:
        fd_close (bool): whether the file gets closed after operation or not.
    """

    return _do_text(file, FileWrapper.read, fd_close, size)


def write_text(
    file: TextIOWrapper,
    contents: str,
    *,
    fd_close: bool,
) -> Result[None, Exception]:
    return _do_text(file, FileWrapper.write, fd_close, contents)


def strip_text(file: TextIOWrapper, *, fd_close: bool) -> Result[None, Exception]:
    return _do_text(file, FileWrapper.strip, fd_close)


def erase_text(file: TextIOWrapper, *, fd_close: bool) -> Result[None, Exception]:
    return _do_text(file, FileWrapper.erase, fd_close)


def cut_text(file: TextIOWrapper, *, fd_close: bool) -> Result[str, Exception]:
    return _do_text(file, FileWrapper.cut, fd_close)
