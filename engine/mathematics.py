from decimal import Decimal
import typing


class Vec2:
    x: Decimal
    y: Decimal

    def __init__(self, x: Decimal = Decimal(0), y: Decimal = Decimal(0)) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: typing.Union[Decimal, "Vec2"]) -> "Vec2":
        is_dec: bool = isinstance(other, Decimal)
        other_x: Decimal = other if is_dec else other.x
        other_y: Decimal = other if is_dec else other.y

        return Vec2(self.x + other_x, self.y + other_y)

    def __sub__(self, other: typing.Union[Decimal, "Vec2"]) -> "Vec2":
        is_dec: bool = isinstance(other, Decimal)
        other_x: Decimal = other if is_dec else other.x
        other_y: Decimal = other if is_dec else other.y

        return Vec2(self.x - other_x, self.y - other_y)
