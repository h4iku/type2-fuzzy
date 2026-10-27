from utils.ranking_methods import centroid_rank


def test_centroid_rank_returns_indices_in_ascending_centroid_order():
    mfs = [
        [[4, 5, 5, 6, 1], [4, 5, 5, 6]],
        [[0, 1, 1, 2, 1], [0, 1, 1, 2]],
        [[2, 3, 3, 4, 1], [2, 3, 3, 4]],
    ]

    assert centroid_rank(mfs).tolist() == [1, 2, 0]
