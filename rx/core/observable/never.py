from typing import Any, Optional

from rx.core import Observable, abc
from rx.disposable import Disposable


def _never() -> Observable[Any]:
    """Returns a non-terminating observable sequence, which can be used
    to denote an infinite duration (e.g. when using reactive joins).

    Returns:
        An observable sequence whose observers will never get called.
    """

    def subscribe(observer: abc.ObserverBase[Any], scheduler: Optional[abc.SchedulerBase] = None) -> abc.DisposableBase:
        return Disposable()

    return Observable(subscribe)


__all__ = ["_never"]
