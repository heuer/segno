from typing import Any, AnyStr, Callable, IO, TextIO, Iterator, Iterable
from .encoder import DataOverflowError as DataOverflowError

__version__ : str


def make(content: int | str | bytes,
         error: str | None = None,
         version: int | str | None = None,
         mode: str | None = None,
         mask: int | None = None,
         encoding: str | None = None,
         eci: bool = False,
         micro: bool | None = None,
         boost_error: bool = True) -> QRCode: ...


def make_qr(content: int | str | bytes,
            error: str | None = None,
            version: int | str | None = None,
            mode: str | None = None,
            mask: int | None = None,
            encoding: str | None = None,
            eci: bool = False, boost_error: bool = True) -> QRCode: ...


def make_micro(content: int | str | bytes,
               error: str | None = None,
               version: int | str | None = None,
               mode: str | None = None,
               mask: int | None = None,
               encoding: str | None = None,
               boost_error: bool = True) -> QRCode: ...


def make_sequence(content: int | str | bytes,
                  error: str | None = None,
                  version: int | str | None = None,
                  mode: str | None = None,
                  mask: int | None = None,
                  encoding: str | None = None,
                  boost_error: bool = True,
                  symbol_count: int | None = None) -> QRCodeSequence: ...


class QRCode:
    matrix: tuple[bytearray, ...]
    mask: int

    @property
    def version(self) -> int | str: ...

    @property
    def error(self) -> str: ...

    @property
    def mode(self) -> str | None: ...

    @property
    def designator(self) -> str: ...

    @property
    def default_border_size(self) -> int: ...

    @property
    def is_micro(self) -> bool: ...

    def symbol_size(self, scale: int | float = 1,
                    border: int | None = None) -> tuple[int | float, int | float]: ...

    def matrix_iter(self, scale: int | float = 1,
                    border: int | None = None,
                    verbose: bool = False) -> Iterator[Iterable[int]]: ...

    def show(self, delete_after: int | float = 20, scale: int | float = 10,
             border: int | None = None, dark: tuple | str = '#000',
             light: tuple | str = '#fff') -> None: ...

    def svg_data_uri(self, xmldecl: bool = False, encode_minimal: bool = False,
                     omit_charset: bool = False, nl: bool = False,
                     **kw: Any) -> str: ...

    def svg_inline(self, **kw: Any) -> str: ...

    def png_data_uri(self, **kw: Any) -> str: ...

    def terminal(self, out: TextIO | str | None = None,
                 border: int | None = None, compact: bool = False) -> None: ...

    def save(self, out: IO[AnyStr] | str, kind: str | None = None,
             **kw: Any) -> None: ...

    def __getattr__(self, name: Any) -> Callable | None: ...

    def __eq__(self, other: Any) -> bool: ...

    __hash__: Any = None


class QRCodeSequence(tuple):
    def terminal(self, out: TextIO | str | None = None,
                 border: int | None = None, compact: bool = False) -> None: ...

    def save(self, out: IO[AnyStr] | str, kind: str | None = None,
             **kw: Any) -> None: ...

    def __getattr__(self, name: Any) -> Callable | None: ...
