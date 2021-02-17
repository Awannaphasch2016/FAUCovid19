from typing_extensions import Literal

Frequency = Literal["day"]
Sort = Literal["asc", "desc"]


def test(frequency: Frequency) -> None:
    pass


def test1(sort: Sort) -> None:
    pass


if __name__ == "__main__":
    test("day")
    test1("aasc")
