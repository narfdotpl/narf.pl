from dataclasses import dataclass
from typing import List

import math
import os
import statistics

from geometry import Point
from svg import Circle, Polygon, Polyline, Stroke, SVG

import colors


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
GRAPHS_DIR = os.path.join(CURRENT_DIR, 'graphs')



@dataclass
class Match:
    after_xp_changes: bool
    mode: str
    duration: float


@dataclass
class Histogram:
    title: str
    filename: str
    bin_width: float
    counts: List[int]
    total_count: int
    median: float


def read_csv(path='data.csv') -> List[Match]:
    return list(_read_csv(path))

def _read_csv(path):
    with open(path) as f:
        # skip header
        for line in f:
            break

        for line in f:
            time, version, after_xp_changes, mode, duration, replay = line.split(',')
            yield Match(
                after_xp_changes=after_xp_changes == 'True',
                mode=mode,
                duration=float(duration)
            )


def make_histogram(title: str, filename: str, matches: List[Match], bin_width: float) -> Histogram:
    durations = [m.duration for m in matches]
    to_index = lambda duration: int(math.floor(duration / bin_width))
    # max_index = to_index(max(durations))
    max_index = to_index(40 * 60 - 1)  # force 40 min as max
    counts = [0] * (max_index + 1)

    for match in matches:
        counts[to_index(match.duration)] += 1

    return Histogram(
        title=title,
        filename=filename,
        bin_width=bin_width,
        counts=counts,
        total_count=len(matches),
        median=statistics.median(durations),
    )


def make_histograms(matches: List[Match], bin_width: float = 2 * 60) -> List[Histogram]:
    before = [m for m in matches if not m.after_xp_changes]
    after = [m for m in matches if m.after_xp_changes]

    tl_before = [m for m in before if m.mode == 'TL']
    tl_after = [m for m in after if m.mode == 'TL']
    qm_before = [m for m in before if m.mode == 'QM']
    qm_after = [m for m in after if m.mode == 'QM']

    return [
        make_histogram('TL before XP changes', 'tl_before.svg', tl_before, bin_width),
        make_histogram('TL after XP changes', 'tl_after.svg', tl_after, bin_width),
        make_histogram('QM before XP changes', 'qm_before.svg', qm_before, bin_width),
        make_histogram('QM after XP changes', 'qm_after.svg', qm_after, bin_width),
    ]


def save_graph(histogram: Histogram, bin_color: colors.Color):
    scale = 1
    w = h = 1024 / 2 * scale
    stroke_width = 2

    left_margin = 0.075 * w
    right_margin = left_margin
    top_margin = 0.4 * h
    bottom_margin = 0.1 * h

    x_min = left_margin
    x_max = w - right_margin
    y_min = top_margin
    y_max = h - bottom_margin

    time_min = 0
    time_max = histogram.bin_width * len(histogram.counts)
    time_to_x = lambda t: (t - time_min) / (time_max - time_min) * (x_max - x_min) + x_min

    percentage_min = 0
    percentage_max = 0.3
    percentage_to_y = lambda p: (1 - (p - percentage_min) / (percentage_max - percentage_min)) * \
                                (y_max - y_min) + y_min

    # draw background
    elements: List[Element] = []
    margin = 0
    elements.append(Polygon(
        vertices=[
            Point(margin, margin),
            Point(w - margin, margin),
            Point(w - margin, h - margin),
            Point(margin, h - margin),
        ],
        fill=colors.white,
        stroke=None,
    ))

    # draw bins
    percentages = [count / histogram.total_count for count in histogram.counts]
    for (i, percentage) in enumerate(percentages):
        t1 = i * histogram.bin_width
        t2 = (i + 1) * histogram.bin_width
        x1 = time_to_x(t1) - 0.5
        x2 = time_to_x(t2) + 0.5
        y1 = percentage_to_y(0)
        y2 = percentage_to_y(percentage)

        elements.append(Polygon(
            vertices=[
                Point(x1, y1),
                Point(x2, y1),
                Point(x2, y2),
                Point(x1, y2),
            ],
            fill=bin_color,
            stroke=None,
        ))

    # draw x axis
    elements.append(Polyline(stroke=Stroke(colors.black, stroke_width), points=[
        Point(x_min - 0.5, y_max),
        Point(x_max + 0.5, y_max),
    ]))

    # draw x axis ticks
    for i in range(len(histogram.counts) + 1):
        t = i * histogram.bin_width
        x = time_to_x(t)
        elements.append(Polyline(
            stroke=Stroke(colors.black, 1),
            points=[
                Point(x, y_max),
                Point(x, y_max - 5),
            ],
        ))

    # TODO: draw x axis labels

    # draw median line
    x_median = time_to_x(histogram.median)
    elements.append(Polyline(stroke=Stroke(colors.black, 1.25), points=[
        Point(x_median, y_min),
        Point(x_median, y_max),
    ]))

    # TODO: draw median text
    # TODO: title
    # TODO: subtitle

    svg = SVG(width=w, height=h, elements=elements)
    path = os.path.join(GRAPHS_DIR, histogram.filename)
    svg.write_xml(path)


def print_ascii_histogram(histogram: Histogram):
    print(f'{histogram.title} ({histogram.total_count} games)')
    print('Median:', histogram.median / 60.0)

    for (i, count) in enumerate(histogram.counts):
        minute = i * (histogram.bin_width / 60.0)
        print(str(minute).zfill(4), end=' ')
        print('#' * count)

    print()


def format_seconds(seconds: float) -> str:
    seconds = round(seconds)
    just_minutes = int(seconds / 60)
    just_seconds = int(round(seconds - 60 * just_minutes))

    return str(just_minutes) + ':' + str(just_seconds).zfill(2)



matches = read_csv()
histograms = make_histograms(matches)

for (histogram, color) in zip(histograms, [colors.blue, colors.red, colors.blue, colors.red]):
    save_graph(histogram, color)
    print(histogram.title)
    print(histogram.total_count, 'games')
    print(format_seconds(histogram.median), 'median')
    print()

# refresh chrome
os.system("osascript -e 'tell application \"Google Chrome\" to tell the active tab of its first window to reload'")
