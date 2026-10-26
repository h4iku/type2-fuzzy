"""Plot interval type-2 fuzzy sets for linguistic word statuses."""

import json
import math
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Literal, NamedTuple, TypedDict

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from utils.centroid_it2fs import centroid_it2


class WordStatus(TypedDict):
    shape: Literal["interior", "left-shoulder", "right-shoulder"]
    MF: list[list[float]]
    ET1FS: list[list[float]]


class PlotData(NamedTuple):
    word: str
    lower_x: list[float]
    upper_x: list[float]
    lower_height: float
    centroid: float


def _prepare_plot_data(
    words_status: Mapping[str, WordStatus],
    words: Sequence[str] | None,
) -> list[PlotData]:
    selected_words = list(words_status) if words is None else list(words)
    if not selected_words:
        raise ValueError("At least one word status must be selected.")

    missing_words = [word for word in selected_words if word not in words_status]
    if missing_words:
        raise ValueError(f"Unknown word status names: {', '.join(missing_words)}")

    plot_data = []
    for word in selected_words:
        membership_functions = words_status[word]["MF"]
        if (
            len(membership_functions) != 2
            or len(membership_functions[0]) != 5
            or len(membership_functions[1]) != 4
        ):
            raise ValueError(
                f"Word status {word!r} must contain a four-point UMF and "
                "a four-point LMF plus its height."
            )

        lmf, umf = membership_functions
        plot_data.append(
            PlotData(
                word,
                lmf[:4],
                umf,
                lmf[4],
                centroid_it2(membership_functions)[2],
            )
        )

    return sorted(plot_data, key=lambda item: item.centroid)


def _get_axis_ticks(
    plot_data: Sequence[PlotData],
) -> tuple[tuple[float, float], list[float], list[float]]:
    x_data_min = min(min(data.lower_x + data.upper_x) for data in plot_data)
    x_data_max = max(max(data.lower_x + data.upper_x) for data in plot_data)
    x_ticks = _three_data_ticks(x_data_min, x_data_max)
    x_min, x_max = x_data_min, x_data_max
    if x_min == x_max:
        x_min -= 0.5
        x_max += 0.5

    y_values = [0, 1, *(data.lower_height for data in plot_data)]
    y_ticks = _three_data_ticks(min(y_values), max(y_values))
    return (x_min, x_max), x_ticks, y_ticks


def _three_data_ticks(data_min: float, data_max: float) -> list[float]:
    if data_min == data_max:
        return [data_min]
    return [data_min, (data_min + data_max) / 2, data_max]


def _draw_subplot(
    ax: Axes,
    data: PlotData,
    x_limits: tuple[float, float],
    x_ticks: list[float],
    y_ticks: list[float],
) -> None:
    upper_y = [0, 1, 1, 0]
    lower_y = [0, data.lower_height, data.lower_height, 0]
    ax.fill(
        data.upper_x + data.lower_x[::-1],
        upper_y + lower_y[::-1],
        color="0.8",
        edgecolor="black",
        linewidth=1.2,
    )
    ax.plot(data.upper_x, upper_y, color="black", linewidth=1.2)
    ax.plot(data.lower_x, lower_y, color="black", linewidth=1.2)
    ax.set_title(data.word, fontsize=9, pad=5)
    ax.text(
        0.97,
        0.93,
        f"{data.centroid:.2f}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=7,
    )
    ax.set_xlim(*x_limits)
    ax.set_ylim(0, 1.2)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.tick_params(labelsize=7)


def plot_it2f(
    words_status: Mapping[str, WordStatus],
    words: Sequence[str] | None = None,
) -> tuple[Figure, list[Axes]]:
    """Plot selected word statuses in a grid of individually labelled panels.

    If ``words`` is omitted, all entries in ``words_status`` are plotted.
    The status mapping stores membership functions as ``[LMF, UMF]``. Returns
    the figure and axes ordered by ascending centroid, with ties kept in the
    order given by ``words``.
    """
    plot_data = _prepare_plot_data(words_status, words)
    subplot_count = len(plot_data)
    columns = min(
        subplot_count,
        math.ceil(math.sqrt(2 * subplot_count)),
    )
    rows = math.ceil(subplot_count / columns)
    figure, axes_grid = plt.subplots(
        rows,
        columns,
        figsize=(3.2 * columns, 2.8 * rows),
        squeeze=False,
        sharex=True,
        sharey=True,
        layout="constrained",
    )
    axes = list(axes_grid.flat[:subplot_count])
    x_limits, x_ticks, y_ticks = _get_axis_ticks(plot_data)
    for ax, data in zip(axes, plot_data):
        _draw_subplot(ax, data, x_limits, x_ticks, y_ticks)

    for ax in axes_grid.flat[subplot_count:]:
        ax.set_visible(False)

    figure.supxlabel("Domain", fontsize=10)
    figure.supylabel("Membership", fontsize=10)
    return figure, axes


def main() -> None:
    status_path = Path(__file__).parent.parent / "words_status.json"
    with status_path.open(encoding="utf-8") as file:
        words_status: dict[str, WordStatus] = json.load(file)

    plot_it2f(words_status)
    plt.show()


if __name__ == "__main__":
    main()
