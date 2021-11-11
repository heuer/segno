from typing import Any, AnyStr, Callable, Optional, Tuple, Union, IO, TextIO, Iterator, Iterable
from .encoder import DataOverflowError as DataOverflowError

__version__ : str

def make(content: Union[int, str, bytes],
         error: Optional[str] = None,
         version: Optional[Union[int, str]] = None,
         mode: Optional[str] = None,
         mask: Optional[int] = None,
         encoding: Optional[str] = None,
         eci: bool = False,
         micro: Optional[bool] = None,
         boost_error: bool = True) -> QRCode: ...


def make_qr(content: Union[int, str, bytes],
            error: Optional[str] = None,
            version: Optional[Union[int, str]] = None,
            mode: Optional[str] = None,
            mask: Optional[int] = None,
            encoding: Optional[str] = None,
            eci: bool = False, boost_error: bool = True) -> QRCode: ...


def make_micro(content: Union[int, str, bytes],
               error: Optional[str] = None,
               version: Optional[Union[int, str]] = None,
               mode: Optional[str] = None,
               mask: Optional[int] = None,
               encoding: Optional[str] = None,
               boost_error: bool = True) -> QRCode: ...


def make_sequence(content: Union[int, str, bytes],
                  error: Optional[str] = None,
                  version: Optional[Union[int, str]] = None,
                  mode: Optional[str] = None,
                  mask: Optional[int] = None,
                  encoding: Optional[str] = None,
                  boost_error: bool = True,
                  symbol_count: Optional[int] = None) -> QRCodeSequence: ...

class QRCode:
    matrix: Tuple[bytearray, ...]
    mask: int

    @property
    def version(self) -> Union[int, str]: ...

    @property
    def error(self) -> str: ...

    @property
    def mode(self) -> Optional[str]: ...

    @property
    def designator(self) -> str: ...

    @property
    def default_border_size(self) -> int: ...

    @property
    def is_micro(self) -> bool: ...

    def symbol_size(self, scale: Union[int, float] = 1,
                    border: Optional[int] = None) -> Tuple[Union[int, float], Union[int, float]]: ...

    def matrix_iter(self, scale: Union[int, float] = 1,
                    border: Optional[int] = None,
                    verbose: bool = False) -> Iterator[Iterable[int]]: ...

    def show(self, delete_after: Union[int, float] = 20, scale: Union[int, float] = 10,
             border: Optional[int] = None, dark: Union[tuple, str] = '#000',
             light: Union[tuple, str] = '#fff') -> None: ...

    def svg_data_uri(self, xmldecl: bool = False, encode_minimal: bool = False,
                     omit_charset: bool = False, nl: bool = False,
                     **kw: Any) -> str: ...

    def svg_inline(self, **kw: Any) -> str: ...

    def png_data_uri(self, **kw: Any) -> str: ...

    def terminal(self, out: Optional[Union[TextIO, str]] = None,
                border: Optional[int] = None, compact: bool = False) -> None: ...

    def save(self, out: Union[IO[AnyStr], str], kind: Optional[str] = None,
             **kw: Any) -> None: ...

    def __getattr__(self, name: Any) -> Optional[Callable]: ...

    def __eq__(self, other: Any) -> bool: ...

    __hash__: Any = None


class QRCodeSequence(tuple):
    def terminal(self, out: Optional[Union[TextIO, str]] = None,
                 border: Optional[int] = None, compact: bool = False) -> None: ...

    def save(self, out: Union[IO[AnyStr], str], kind: Optional[str] = None,
             **kw: Any) -> None: ...

    def __getattr__(self, name: Any) -> Optional[Callable]: ...
