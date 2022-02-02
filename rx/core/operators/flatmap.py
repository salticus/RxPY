import collections
from typing import Callable, Optional, TypeVar

from rx import from_, from_future
from rx import operators as ops
from rx.core import Observable
from rx.core.typing import Mapper, MapperIndexed
from rx.internal.utils import is_future

_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")


def _flat_map_internal(
    source: Observable[_T1],
    mapper: Optional[Mapper[_T1, Observable[_T2]]] = None,
    mapper_indexed: Optional[MapperIndexed[_T1, Observable[_T2]]] = None,
) -> Observable[_T2]:
    def projection(x: _T1, i: int):
        mapper_result = mapper(x) if mapper else mapper_indexed(x, i) if mapper_indexed else None
        if is_future(mapper_result):
            result = from_future(mapper_result)
        elif isinstance(mapper_result, collections.abc.Iterable):
            result = from_(mapper_result)
        else:
            result = mapper_result
        return result

    return source.pipe(ops.map_indexed(projection), ops.merge_all())


def _flat_map(mapper: Optional[Mapper[_T1, Observable[_T2]]] = None) -> Callable[[Observable[_T1]], Observable[_T2]]:
    def flat_map(source: Observable[_T1]) -> Observable[_T2]:
        """One of the Following:
        Projects each element of an observable sequence to an observable
        sequence and merges the resulting observable sequences into one
        observable sequence.

        Example:
            >>> flat_map(source)

        Args:
            source: Source observable to flat map.

        Returns:
            An operator function that takes a source observable and returns
            an observable sequence whose elements are the result of invoking
            the one-to-many transform function on each element of the
            input sequence .
        """

        if callable(mapper):
            ret = _flat_map_internal(source, mapper=mapper)
        else:
            ret = _flat_map_internal(source, mapper=lambda _: mapper)

        return ret

    return flat_map


def _flat_map_indexed(
    mapper_indexed: Optional[MapperIndexed[_T1, Observable[_T2]]] = None,
) -> Callable[[Observable[_T1]], Observable[_T2]]:
    def flat_map_indexed(source: Observable[_T1]) -> Observable[_T2]:
        """One of the Following:
        Projects each element of an observable sequence to an observable
        sequence and merges the resulting observable sequences into one
        observable sequence.

        Example:
            >>> flat_map_indexed(source)

        Args:
            source: Source observable to flat map.

        Returns:
            An observable sequence whose elements are the result of invoking
            the one-to-many transform function on each element of the input
            sequence.
        """

        if callable(mapper_indexed):
            ret = _flat_map_internal(source, mapper_indexed=mapper_indexed)
        else:
            ret = _flat_map_internal(source, mapper=lambda _: mapper_indexed)
        return ret

    return flat_map_indexed


def _flat_map_latest(mapper: Mapper[_T1, Observable[_T2]]) -> Callable[[Observable[_T1]], Observable[_T2]]:
    def flat_map_latest(source: Observable[_T1]) -> Observable[_T2]:
        """Projects each element of an observable sequence into a new
        sequence of observable sequences by incorporating the element's
        index and then transforms an observable sequence of observable
        sequences into an observable sequence producing values only
        from the most recent observable sequence.

        Args:
            source: Source observable to flat map latest.

        Returns:
            An observable sequence whose elements are the result of
            invoking the transform function on each element of source
            producing an observable of Observable sequences and that at
            any point in time produces the elements of the most recent
            inner observable sequence that has been received.
        """

        return source.pipe(ops.map(mapper), ops.switch_latest())

    return flat_map_latest


__all__ = ["_flat_map", "_flat_map_latest", "_flat_map_indexed"]
