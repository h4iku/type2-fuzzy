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


def test_mg_interpolates_membership_and_returns_zero_outside_support():
    x = [-1, 0, 0.5, 1, 2, 2.5, 3, 4]

    grades = mg(x, [0, 1, 2, 3])

    assert len(grades) == len(x)
    assert grades == pytest.approx([0, 0, 0.5, 1, 1, 0.5, 0, 0])


@pytest.mark.parametrize(
    "x_point, w_lower, w_upper",
    [
        ([1, 2], [0], [1, 1]),
        ([1, 2], [0, 0], [1]),
    ],
)
def test_ekm_rejects_mismatched_point_and_weight_lengths(x_point, w_lower, w_upper):
    with pytest.raises(ValueError, match="same length"):
        ekm(x_point, w_lower, w_upper, 1)


def test_ekm_returns_weighted_mean_for_crisp_memberships():
    x_point = [1, 3, 7]
    weights = [1, 2, 1]

    left = ekm(x_point, weights, weights, -1)
    right = ekm(x_point, weights, weights, 1)

    assert left == pytest.approx(3.5)
    assert right == pytest.approx(3.5)


@pytest.mark.parametrize(
    "x_point, w_lower, w_upper",
    [
        ([1, 3, 7], [0.2, 0.5, 0.4], [0.8, 0.9, 0.7]),
        ([2, 5, 9], [0.1, 0.4, 0.3], [0.6, 0.8, 0.9]),
    ],
)
def test_ekm_centroid_bounds_are_ordered_and_within_support(
    x_point, w_lower, w_upper
):
    left = ekm(x_point, w_lower, w_upper, -1)
    right = ekm(x_point, w_lower, w_upper, 1)

    assert min(x_point) <= left <= right <= max(x_point)
