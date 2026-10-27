import pytest

from utils.linguistic_weighted_average import fwa


def test_fwa_with_one_input_and_unit_weight_preserves_trapezoid():
    result, y_coordinates, mu_coordinates = fwa(
        [[0, 1, 2, 3]],
        [[1, 1, 1, 1]],
    )

    assert result == pytest.approx([0, 1, 2, 3, 1])
    assert y_coordinates == pytest.approx([0, 1, 2, 3])
    assert mu_coordinates == pytest.approx([0, 1, 1, 0])
