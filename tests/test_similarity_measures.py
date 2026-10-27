import pytest

from utils.similarity_measures import jaccard


def test_jaccard_similarity_is_symmetric_and_bounded():
    a = [0, 1, 2, 3, 0.25, 1, 2, 2.75, 0.5]
    b = [1, 2, 3, 4, 1.25, 2, 3, 3.75, 0.5]

    similarity = jaccard(a, b)

    assert 0 <= similarity <= 1
    assert jaccard(a, b) == pytest.approx(jaccard(b, a))


def test_jaccard_similarity_of_identical_sets_is_one():
    a = [0, 1, 2, 3, 0.25, 1, 2, 2.75, 0.5]

    assert jaccard(a, a) == pytest.approx(1)
