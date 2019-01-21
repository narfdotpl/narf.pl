from __future__ import annotations
from dataclasses import dataclass


class Color:
    def to_svg_color(self) -> str:
        raise NotImplemented()


@dataclass
class RGBA(Color):
    red: float        # 0–255
    green: float      # 0–255
    blue: float       # 0–255
    alpha: float = 1  # 0–1

    def to_svg_color(self) -> str:
        return 'rgba({red}, {green}, {blue}, {alpha})'.format(**vars(self))


@dataclass
class HSLA(Color):
    hue: float         # 0–360
    saturation: float  # 0–1
    lightness: float   # 0–1
    alpha: float = 1   # 0–1

    def copy(self) -> HSLA:
        return HSLA(
            self.hue,
            self.saturation,
            self.lightness,
            self.alpha,
        )

    def to_svg_color(self) -> str:
        return 'hsla({h}, {s}%, {l}%, {a})'.format(
            h=self.hue,
            s=100 * self.saturation,
            l=100 * self.lightness,
            a=self.alpha,
        )


black = RGBA(40, 40, 40)
white = HSLA(0, 0, 1)
grey = RGBA(220, 220, 220)

# red = HSLA(5, 1, 0.5)
red = RGBA(217,72,1)  # http://colorbrewer2.org/#type=sequential&scheme=Oranges&n=9
blue = RGBA(33, 113, 181)  # http://colorbrewer2.org/#type=sequential&scheme=Blues&n=9


def blue_and_red_cycle():
    while True:
        # yield blue
        # yield red
        yield white
