from typing import Any

import numpy as np
import pytest
from matplotlib import pyplot as plt

from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import validate_output


@pytest.mark.parametrize(
    (
        "test_case",
        "expected_output",
        "x",
        "y",
        "xerr",
        "yerr",
        "color",
        "ecolor",
        "marker",
        "label",
        "title",
        "yscale",
        "ylabel",
        "metadata",
    ),
    [
        (
            "literal_and_array",
            "errorbar_literal_and_array",
            [1, 2],
            [4, 3],
            2,
            [4, 5],
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
            "errorbar_all_features",
            [1, 2],
            [4, 3],
            [[1, 2], [2, 3]],
            [3, 4],
            "green",
            "red",
            "o",
            "Errorbartest",
            "My amazing errorbar plot",
            "log",
            "log axis",
            None,
        ),
        (
            "array_like",
            "errorbar_array_like",
            np.array([1, 2]),
            np.array([4, 3]),
            np.array([[1, 2], [2, 3]]),
            np.array([3, 4]),
            "green",
            "red",
            "o",
            "Errorbartest",
            "My amazing errorbar plot",
            "log",
            "log axis",
            None,
        ),
        (
            "metadata",
            "errorbar_test_metadata",
            [1, 2],
            [4, 3],
            2,
            [4, 5],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            {"key": "value"},
        ),
    ],
)
def test_errorbar_plot(
    test_case: str,
    expected_output: str,
    x: Any,
    y: Any,
    xerr: Any,
    yerr: Any,
    color: Any,
    ecolor: Any,
    marker: Any,
    label: Any,
    title: Any,
    yscale: Any,
    ylabel: Any,
    metadata: Any,
    request: Any,
) -> None:
    serializer = MatplotlibSerializer()

    update_tests = request.config.getoption("--update-tests")

    _, ax = serializer.subplots()
    ax.errorbar(x, y, xerr=xerr, yerr=yerr, color=color, ecolor=ecolor, marker=marker, label=label)

    if title:
        ax.set_title(title)
    if yscale:
        ax.set_yscale(yscale)
    if ylabel:
        ax.set_ylabel(ylabel)

    if metadata:
        ax.errorbar(x, y, xerr=xerr, yerr=yerr, color=color, ecolor=ecolor, marker=marker, label=label)
        serializer.add_custom_metadata_figure(metadata)
        serializer.add_custom_metadata_plot(metadata, plot_selector=0)
        serializer.add_custom_metadata_axis(metadata, axis="y", plot_selector=0)
        serializer.add_custom_metadata_trace(metadata, trace_selector=1)
        serializer.add_custom_metadata_datapoints(metadata, trace_selector=0, point_selector=1)
        serializer.add_custom_metadata_datapoints(
            metadata, trace_selector=(2, 3), trace_rel_tol=0.01, point_selector=(1, 4), point_rel_tolerance=0.01
        )

    if update_tests == "confirm":
        serializer.write_json_file("./tests_updated/" + expected_output + ".json")
    else:
        validate_output(serializer, expected_output)
    plt.close()
