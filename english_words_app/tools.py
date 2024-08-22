from typing import Iterable, TypeVar, List

T = TypeVar("T")


def shred(size: int, items: Iterable[T]) -> List[List[T]]:
    lines = []
    line = []
    for item in items:
        if len(line) == size:
            lines.append(line)
            line = []
        line.append(item)
    lines.append(line)
    return lines
