import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from eia.plot_it2f import WordStatus, plot_it2f
from utils.centroid_it2fs import centroid_it2

STATUSES: dict[str, WordStatus] = {
    "Interior": {
        "shape": "interior",
        "MF": [[2, 3, 3, 4, 0.4], [1, 2, 4, 5]],
        "ET1FS": [[2.0, 4.0]],
    },
    "Little": {
        "shape": "left-shoulder",
        "MF": [[0, 0, 1, 2, 1], [0, 0, 3, 4]],
        "ET1FS": [[0.0, 2.0]],
    },
    "Large": {
        "shape": "right-shoulder",
        "MF": [[6, 8, 10, 10, 1], [4, 7, 10, 10]],
        "ET1FS": [[6.0, 10.0]],
    },
}


@pytest.fixture(autouse=True)
def close_figures_after_test():
    yield
    plt.close("all")


@pytest.mark.parametrize("word", ["Interior", "Little", "Large"])
def test_plot_it2f_draws_umf_and_lmf_for_each_shape(word):
    figure, axes = plot_it2f(STATUSES, words=[word])

    assert len(axes) == 1
    assert len(axes[0].patches) == 1
    assert len(axes[0].lines) == 2
    assert axes[0].get_title() == word
    assert float(axes[0].texts[0].get_text()) == pytest.approx(
        centroid_it2(STATUSES[word]["MF"])[2], abs=0.005
    )
    assert axes[0].texts[0].get_fontsize() == 7
    assert axes[0].lines[1].get_ydata() == pytest.approx(
        [
            0,
            STATUSES[word]["MF"][0][4],
            STATUSES[word]["MF"][0][4],
            0,
        ]
    )
    assert figure.axes[0] is axes[0]
    assert len(figure.axes) == 1


def test_plot_it2f_uses_a_grid_of_separate_axes_for_selected_words():
    figure, axes = plot_it2f(STATUSES, words=["Large", "Interior"])

    assert len(axes) == 2
    assert axes[0] is not axes[1]
    assert [ax.get_title() for ax in axes] == ["Interior", "Large"]
    assert all(ax.get_xlim() == (1, 10) for ax in axes)
    assert all(ax.get_ylim() == (0, 1.2) for ax in axes)
    assert all(len(ax.get_xticks()) <= 3 and len(ax.get_yticks()) <= 3 for ax in axes)
    assert axes[0].get_xticks() == pytest.approx([1, 5.5, 10])
    assert axes[0].get_yticks() == pytest.approx([0, 0.5, 1])
    assert len(figure.axes) == 2


def test_plot_it2f_uses_every_word_when_selection_is_omitted():
    _, axes = plot_it2f(STATUSES)

    assert [ax.get_title() for ax in axes] == ["Little", "Interior", "Large"]


def test_plot_it2f_builds_a_multirow_grid_and_hides_unused_panels():
    statuses = {
        **STATUSES,
        "Word 4": STATUSES["Interior"],
        "Word 5": STATUSES["Large"],
    }

    figure, axes = plot_it2f(statuses)

    assert len(axes) == 5
    assert len(figure.axes) == 8
    assert [ax.get_title() for ax in axes] == [
        "Little",
        "Interior",
        "Word 4",
        "Large",
        "Word 5",
    ]
    assert all(not ax.get_visible() for ax in figure.axes[5:])


def test_plot_it2f_uses_compact_panels_for_large_grids():
    statuses = {f"Word {index}": STATUSES["Interior"] for index in range(32)}

    figure, axes = plot_it2f(statuses)
    figure.canvas.draw()

    positions = [ax.get_position() for ax in axes]
    figure_aspect = figure.get_figwidth() / figure.get_figheight()
    assert len(axes) == 32
    assert len(figure.axes) == 32
    assert len({round(position.x0, 3) for position in positions[:8]}) == 8
    assert positions[8].y0 < positions[0].y0
    assert all(
        1.0 <= position.width / position.height * figure_aspect <= 1.5
        for position in positions
    )
    assert figure.get_layout_engine() is not None


@pytest.mark.parametrize(
    ("words", "message"),
    [
        ([], "At least one"),
        (["Unknown"], "Unknown word status"),
    ],
)
def test_plot_it2f_rejects_empty_or_unknown_word_selection(
    words: list[str], message: str
):
    with pytest.raises(ValueError, match=message):
        plot_it2f(STATUSES, words=words)
