import pytest
from openpyxl import Workbook

from eia.data_part import (
    _read_intervals,
    bad_data_processing,
    outlier_processing,
    tolerance_limit_processing,
)

valid_intervals = [
    ([0, 5], True),
    ([3, 7], True),
]

invalid_intervals = [
    ([-1, 2], False),
    ([5, 4], False),
    ([7, 17], False),
    ([0, 10], False),
    ([10, 10], False),
]


@pytest.mark.parametrize("interval, expected", valid_intervals + invalid_intervals)
def test_bad_data_check(interval, expected):
    assert bad_data_processing(interval) == expected


test_cases = [
    # Input, expected output
    ([(1, 2), (3, 4), (5, 6), (7, 8)], [(1, 2), (3, 4), (5, 6), (7, 8)]),  # No outliers
    (
        [(1, 2), (3, 4), (5, 6), (7, 8), (10, 20)],
        [(1, 2), (3, 4), (5, 6), (7, 8)],
    ),  # Outlier on right end
    (
        [(1, 2), (3, 4), (5, 6), (7, 8), (-10, -5)],
        [(1, 2), (3, 4), (5, 6), (7, 8)],
    ),  # Outlier on left end
    (
        [(1, 2), (3, 4), (5, 6), (7, 8), (9, 15)],
        [(1, 2), (3, 4), (5, 6), (7, 8)],
    ),  # Outlier on interval length
    ([], []),  # Empty input
    ([(1, 2)], [(1, 2)]),  # Single input
]


@pytest.mark.parametrize("input, expected", test_cases)
def test_outlier_processing(input, expected):
    output = outlier_processing(input)
    assert output == expected


def test_tolerance_limit_respects_interval_length_domain():
    intervals = [(0.1, 0.6), (0.1, 2.1), (0.1, 9.6), (0.1, 9.6)]

    assert tolerance_limit_processing(intervals) == intervals[1:]


def test_read_intervals_keeps_endpoints_from_the_same_row():
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(["word", "example"])
    for row in [(1, 2), (1, 2), (None, 9), (1, 2), (1, 2)]:
        worksheet.append(row)

    assert _read_intervals(worksheet) == {"word": [(1, 2)] * 4}
