from typing import Callable, Optional, TypeVar

from rx import operators as ops
from rx.core import Observable, abc
from rx.core.typing import Predicate

_T = TypeVar("_T")


def _some(predicate: Optional[Predicate[_T]] = None) -> Callable[[Observable[_T]], Observable[bool]]:
    def some(source: Observable[_T]) -> Observable[bool]:
        """Partially applied operator.

        Determines whether some element of an observable sequence satisfies a
        condition if present, else if some items are in the sequence.

        Example:
            >>> obs = some(source)

        Args:
            predicate -- A function to test each element for a condition.

        Returns:
            An observable sequence containing a single element
            determining whether some elements in the source sequence
            pass the test in the specified predicate if given, else if
            some items are in the sequence.
        """

        def subscribe(observer: abc.ObserverBase[bool], scheduler: Optional[abc.SchedulerBase] = None):
            def on_next(_: _T):
                observer.on_next(True)
                observer.on_completed()

            def on_error():
                observer.on_next(False)
                observer.on_completed()

            return source.subscribe_(on_next, observer.on_error, on_error, scheduler)

        if predicate:
            return source.pipe(
                ops.filter(predicate),
                _some(),
            )

        return Observable(subscribe)

    return some
