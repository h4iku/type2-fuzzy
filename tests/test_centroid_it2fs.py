import pytest

from utils.centroid_it2fs import ekm, mg


@pytest.mark.parametrize(
    "x_point, w_upper, max_flag, expected",
    [
        ([1, 100], [1, 0], 1, 1),
        ([1, 100], [0, 1], -1, 100),
    ],
)
def test_ekm_zero_lower_weights_ignore_points_without_upper_support(
    x_point, w_upper, max_flag, expected
):
    assert ekm(x_point, [0, 0], w_upper, max_flag) == expected


def test_mg_rejects_mismatched_knot_and_grade_lengths():
    with pytest.raises(ValueError, match="same length"):
        mg([0.5], [0, 1, 2, 3], [0, 1])
