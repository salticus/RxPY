from typing import Callable, Iterable, List, Optional, TypeVar

from rx.core import Observable, abc


_T = TypeVar("_T")


def _to_iterable() -> Callable[[Observable[_T]], Observable[Iterable[_T]]]:
    def to_iterable(source: Observable[_T]) -> Observable[Iterable[_T]]:
        """Creates an iterable from an observable sequence.

        Returns:
            An observable sequence containing a single element with an
            iterable containing all the elements of the source
            sequence.
        """

        def subscribe(
            observer: abc.ObserverBase[Iterable[_T]],
            scheduler: Optional[abc.SchedulerBase] = None,
        ):
            nonlocal source

            queue: List[_T] = []

            def on_next(item: _T):
                queue.append(item)

            def on_completed():
                nonlocal queue
                observer.on_next(queue)
                queue = []
                observer.on_completed()

            return source.subscribe_(
                on_next, observer.on_error, on_completed, scheduler
            )

        return Observable(subscribe)

    return to_iterable


__all__ = ["_to_iterable"]
