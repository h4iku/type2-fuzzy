import pytest

from utils.linguistic_weighted_average import fwa, lwa


def test_fwa_with_one_input_and_unit_weight_preserves_trapezoid():
    result, y_coordinates, mu_coordinates = fwa(
        [[0, 1, 2, 3]],
        [[1, 1, 1, 1]],
    )

    assert result == pytest.approx([0, 1, 2, 3, 1])
    assert y_coordinates == pytest.approx([0, 1, 2, 3])
    assert mu_coordinates == pytest.approx([0, 1, 1, 0])


def test_fwa_requires_at_least_two_alpha_cuts():
    with pytest.raises(ValueError, match="at least 2"):
        fwa([[0, 1, 2, 3]], [[1, 1, 1, 1]], n=1)


def test_fwa_rejects_different_numbers_of_inputs_and_weights():
    with pytest.raises(ValueError, match="same number of sets"):
        fwa([[0, 1, 2, 3]], [[1, 1, 1, 1], [1, 1, 1, 1]])


def test_fwa_does_not_modify_inputs_when_adding_default_heights():
    x = [[0, 1, 2, 3]]
    w = [[1, 1, 1, 1]]

    fwa(x, w)

    assert x == [[0, 1, 2, 3]]
    assert w == [[1, 1, 1, 1]]


def test_lwa_does_not_modify_inputs_when_adding_default_heights():
    x = [[0, 1, 2, 3, 0, 1, 2, 3]]
    w = [[0, 1, 1, 0, 0, 1, 1, 0]]

    lwa(x, w)

    assert x == [[0, 1, 2, 3, 0, 1, 2, 3]]
    assert w == [[0, 1, 1, 0, 0, 1, 1, 0]]


def test_lwa_rejects_different_numbers_of_inputs_and_weights():
    with pytest.raises(ValueError, match="same number of sets"):
        lwa(
            [[0, 1, 2, 3, 0, 1, 2, 3]],
            [
                [0, 1, 1, 0, 0, 1, 1, 0],
                [0, 1, 1, 0, 0, 1, 1, 0],
            ],
        )
