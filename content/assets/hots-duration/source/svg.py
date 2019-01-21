from dataclasses import dataclass
from geometry import CubicBezierCurve, Point
from os.path import dirname, join, realpath
from typing import Dict, List, Optional, Union

import colors


CURRENT_DIR = dirname(realpath(__file__))
DEFAULT_XML_DIR = join(CURRENT_DIR, 'renders')


class Element:
    Attributes = Dict[str, Union[str, float]]

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

    @property
    def attributes(self) -> Attributes:
        raise NotImplemented()

    def to_xml(self) -> str:
        raise NotImplemented()


class EmptyElement(Element):
    def to_xml(self) -> str:
        return ' '.join([f'<{self.name}'] + [f'{k}="{v}"' for k, v in sorted(self.attributes.items())] + ['/>'])


@dataclass
class SVG:
    elements: List[Element]
    width: float
    height: float

    def to_xml(self) -> str:
        prefix = f"""
<?xml version="1.0" standalone="no"?>
<svg width="{self.width}" height="{self.height}" version="1.1" xmlns="http://www.w3.org/2000/svg">
""".strip()
        suffix = '</svg>\n'
        return '\n'.join([prefix] + [e.to_xml() for e in self.elements] + [suffix])

    def write_xml(self, path: str) -> None:
        path_is_relative = not path.startswith('/')
        if path_is_relative:
            path = join(DEFAULT_XML_DIR, path)

        with open(path, 'w') as f:
            f.write(self.to_xml())


@dataclass
class Stroke:
    color: colors.Color
    width: float = 1
    dashes: Optional[List[float]] = None

    @property
    def attributes(self) -> Element.Attributes:
        attributes: Element.Attributes = {
            'stroke': self.color.to_svg_color(),
            'stroke-width': self.width,
            'stroke-linecap': 'butt',
            'fill': 'transparent',
        }

        if self.dashes is not None:
            attributes['stroke-dasharray'] = ' '.join(str(x) for x in self.dashes)

        return attributes


@dataclass
class Strokable(EmptyElement):
    stroke: Optional[Stroke]

    @property
    def attributes(self) -> Element.Attributes:
        if self.stroke is not None:
            return self.stroke.attributes
        else:
            return {}


@dataclass
class Fillable(Strokable):
    fill: Optional[colors.Color]

    @property
    def attributes(self) -> Element.Attributes:
        return {
            **super().attributes,
            'fill': self.fill.to_svg_color() if self.fill else 'transparent',
        }


@dataclass
class Polyline(Strokable):
    points: List[Point]

    @property
    def attributes(self) -> Element.Attributes:
        return {
            **super().attributes,
            'points': points_to_svg(self.points),
        }


@dataclass
class Circle(Fillable):
    position: Point
    radius: float

    @property
    def attributes(self) -> Element.Attributes:
        return {
            **super().attributes,
            'cx': self.position.x,
            'cy': self.position.y,
            'r': self.radius,
        }


@dataclass
class Polygon(Fillable):
    vertices: List[Point]

    @property
    def attributes(self) -> Element.Attributes:
        return {
            **super().attributes,
            'points': points_to_svg(self.vertices),
        }


@dataclass
class Path(Fillable):
    curves: List[CubicBezierCurve]
    mask_id: Optional[str]

    @property
    def attributes(self) -> Element.Attributes:
        attributes = {
            **super().attributes,
            'd': ' '.join(map(self._bezier_to_svg, self.curves)),
        }

        if self.mask_id is not None:
            attributes['mask'] = f'url(#{self.mask_id})'

        return attributes

    def _point_to_svg(self, point: Point) -> str:
        return f'{point.x} {point.y}'

    def _bezier_to_svg(self, bezier: CubicBezierCurve) -> str:
        p1, cp1, cp2, p2 = list(map(self._point_to_svg, bezier.points))
        return f'M {p1} C {cp1} {cp2} {p2}'


@dataclass
class Mask(Element):
    id: str
    elements: List[Element]

    @property
    def attributes(self) -> Element.Attributes:
        return {
            'id': self.id,
        }

    def to_xml(self) -> str:
        opening_tag = ' '.join([f'<{self.name}'] + [f'{k}="{v}"' for k, v in sorted(self.attributes.items())] + ['>'])
        closing_tag = f'</{self.name}>'
        return '\n'.join([opening_tag] + [e.to_xml() for e in self.elements] + [closing_tag])


def points_to_svg(points: List[Point]) -> str:
    return ' '.join(f'{p.x} {p.y}' for p in points)


def write_xml_with_test_elements():
    scale = 1
    w = h = 1280 * scale
    stroke_width = 4 * scale

    y = h / 2
    x1 = 1/3 * w
    x2 = 2/3 * w
    line = Polyline(stroke=Stroke(colors.black, stroke_width), points=[
        Point(x1, y),
        Point(x2, y),
    ])

    r = 0.13 * w
    circle = Circle(
        position=Point(x2, y),
        radius=r,
        stroke=Stroke(colors.black, stroke_width),
        fill=colors.blue,
    )

    square = Polygon(
        vertices=[
            Point(x1 - r, y - r),
            Point(x1 + r, y - r),
            Point(x1 + r, y + r),
            Point(x1 - r, y + r),
        ],
        stroke=Stroke(colors.black, stroke_width),
        fill=colors.red,
    )

    margin = 80
    background = Polygon(
        vertices=[
            Point(margin, margin),
            Point(w - margin, margin),
            Point(w - margin, h - margin),
            Point(margin, h - margin),
        ],
        fill=colors.grey,
        stroke=None,
    )

    elements: List[Element] = [
        background,
        square,
        circle,
        line,
    ]

    svg = SVG(width=w, height=h, elements=elements)
    svg.write_xml('test.svg')
