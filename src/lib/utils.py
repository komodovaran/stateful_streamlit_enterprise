import time
from functools import wraps
from typing import Any, Callable, TypeVar

from core.core import SessionState
from pages.app_page import AppPage


def timeit(f: Callable) -> Callable:
    """Decorator to time functions and methods for optimization"""

    def _print_elapsed(start: float, end: float, name: str = "") -> None:
        print("'{}' {:.2f} ms".format(name, (end - start) * 1e3))

    @wraps(f)
    def _timed(*args: Any, **kwargs: Any) -> Any:
        ts = time.time()
        result = f(*args, **kwargs)
        te = time.time()
        _print_elapsed(name=f.__name__, start=ts, end=te)
        return result

    return _timed


# equivalent to C# TPage where TPage : AppPage
TPage = TypeVar("TPage", bound=AppPage)


def sync_state_after(
    f: Callable[[TPage, SessionState], None]
) -> Callable[[TPage, SessionState], None]:
    """
    Synchronizes state after a page's __call__ method has been invoked
    """

    def decorated(self: TPage, sess: SessionState) -> None:
        f(self, sess)
        sess.sync()

    return decorated
