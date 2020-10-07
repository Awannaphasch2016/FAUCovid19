from typing import Any

from typing_extensions import TypedDict


class InputRequestsParameters(TypedDict):
    _crawlers: Any
    _since: Any
    _until: Any
    _aspects: Any
    _search_types: Any
    _frequency: Any
    _fields: Any
    _total_count: Any
    _top_amount: Any
    _limit: Any
    _page: Any


if __name__ == '__main__':
    from typing import NamedTuple


    class Point(NamedTuple):
        x: int
        y: int


    Point(3, 3)  # -> Point(x=3, y=1)
