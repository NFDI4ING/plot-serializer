from typing import Any, Dict

import numpy as np
import pytest
from matplotlib import pyplot as plt

from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import validate_output


def func(x: Any, d: float) -> Any:
    return 1 / (np.sqrt((1 - x**2) ** 2 + (2 * x * d)))


x = np.linspace(0, 3, 500)


@pytest.mark.parametrize(
    (
        "test_case",
        "expected_output",
        "x",
        "y",
        "label",
        "linestyle",
        "color",
        "marker",
        "title",
        "xlabel",
        "xscale",
        "ylabel",
        "yscale",
        "metadata",
        "xlim",
        "ylim",
        "spines",
    ),
    [
        (
            "simple",
            "line_plot_simple",
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [10, 20, 30, 40, 50, 60, 70, 70, 90, 100],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "simple_array_like",
            "line_plot_array_like",
            np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            np.array([10, 20, 30, 40, 50, 60, 70, 70, 90, 100]),
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "all_features",
            "line_plot_all_features",
            x,
            [
                func(x, 0),
                func(x, 0.1),
                func(x, 0.2),
                func(x, 0.5),
                func(x, 1),
            ],
            ["Einhuellend", "D = 0.1", "D = 0.2", "D = 0.5", "D = 1"],
            ["--", None, None, None, None],
            ["gray", (0.7, 0.7, 1), None, (0.3, 0.6, 0.8, 1), None],
            [">", None, None, ".", None],
            "Ressonanz",
            r"$\omega/\omega_0$",
            None,
            "$A/A_E$",
            None,
            None,
            (0, 3),
            (40, 0),
            {"top": False, "right": False, "bottom": True, "left": True},
        ),
        (
            "metadata",
            "line_test_metadata",
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [10, 20, 30, 40, 50, 60, 70, 70, 90, 100],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            {"key": "value"},
            None,
            None,
            None,
        ),
    ],
)
def test_line_plot(
    test_case: str,
    expected_output: str,
    x: Any,
    y: Any,
    label: Any,
    linestyle: Any,
    color: Any,
    marker: Any,
    title: Any,
    xlabel: Any,
    xscale: Any,
    ylabel: Any,
    yscale: Any,
    metadata: Any,
    xlim: Any,
    ylim: Any,
    spines: Dict[str, bool],
    request: Any,
) -> None:
    serializer = MatplotlibSerializer()

    update_tests = request.config.getoption("--update-tests")

    _, ax = serializer.subplots()

    if not (isinstance(y[0], (float, int, np.generic))):
        for i in range(len(y)):
            ax.plot(x, y[i], label=label[i], linestyle=linestyle[i], color=color[i], marker=marker[i])
    else:
        ax.plot(x, y, label=label, linestyle=linestyle, color=color, marker=marker)

    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if xscale:
        ax.set_xscale(xscale)
    if ylabel:
        ax.set_ylabel(ylabel)
    if yscale:
        ax.set_yscale(yscale)
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
    if spines:
        for spine, visible in spines.items():
            ax.spines[spine].set_visible(visible)

    if metadata:
        ax.plot(x, y, label=label, linestyle=linestyle, color=color, marker=marker)
        serializer.add_custom_metadata_figure(metadata)
        serializer.add_custom_metadata_plot(metadata, plot_selector=0)
        serializer.add_custom_metadata_axis(metadata, axis="y", plot_selector=0)
        serializer.add_custom_metadata_trace(metadata, trace_selector=1)
        serializer.add_custom_metadata_datapoints(metadata, trace_selector=0, point_selector=1)
        serializer.add_custom_metadata_datapoints(
            {"key2": "value2"},
            trace_selector=(1, 10),
            trace_rel_tol=0.01,
            point_selector=(4, 30),
            point_rel_tolerance=0.5,
        )

    if update_tests == "confirm":
        serializer.write_json_file("./tests_updated/" + expected_output + ".json")
    else:
        validate_output(serializer, expected_output)
    plt.close()
