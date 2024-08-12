from typing import Any

import numpy as np

from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import validate_output


def test_simple() -> None:
    serializer = MatplotlibSerializer()

    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [10, 20, 30, 40, 50, 60, 70, 70, 90, 100]

    _, ax = serializer.subplots()
    ax.plot(x, y)

    validate_output(serializer, "line_plot_simple")


def func(x: Any, d: float) -> Any:
    return 1 / (np.sqrt((1 - x**2) ** 2 + (2 * x * d)))


def test_all_features() -> None:
    serializer = MatplotlibSerializer()
    x = np.linspace(0, 3, 500)

    e = func(x, 0)
    y = func(x, 0.1)
    y2 = func(x, 0.2)
    y3 = func(x, 0.5)
    y4 = func(x, 1)

    _, ax = serializer.subplots()
    ax.plot(x, e, label="Einhuellend", linestyle="--", color="gray", marker=">")
    ax.plot(x, y, label="D = 0.1", color=(0.7, 0.7, 1))
    ax.plot(x, y2, label="D = 0.2")
    ax.plot(x, y3, label="D = 0.5", color=(0.3, 0.6, 0.8, 1), marker=".")
    ax.plot(x, y4, label="D = 1")

    ax.legend()
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_xlabel(r"$\omega/\omega_0$")
    ax.set_ylabel("$A/A_E$")
    ax.grid(True)
    ax.set_title("Ressonanz")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim((40, 0))

    validate_output(serializer, "line_plot_all_features")


def test_metadata() -> None:
    serializer = MatplotlibSerializer()

    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [10, 20, 30, 40, 50, 60, 70, 70, 90, 100]

    _, ax = serializer.subplots()
    ax.plot(x, y)
    ax.plot(x, y)
    dict = {"key": "value"}
    serializer.add_custom_metadata_figure(dict)
    serializer.add_custom_metadata_plot(dict, plot_selector=0)
    serializer.add_custom_metadata_axis(dict, axis="y", plot_selector=0)
    serializer.add_custom_metadata_trace(dict, trace_selector=1)
    serializer.add_custom_metadata_datapoints(dict, trace_selector=0, point_selector=1)
    serializer.add_custom_metadata_datapoints(
        {"key2": "value2"}, trace_selector=(1, 10), trace_rel_tol=0.01, point_selector=(4, 30), point_rel_tolerance=0.5
    )

    validate_output(serializer, "line_test_metadata")
