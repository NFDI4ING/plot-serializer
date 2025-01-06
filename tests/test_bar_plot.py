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
        "names",
        "heights",
        "color",
        "title",
        "yscale",
        "ylabel",
        "metadata",
    ),
    [
        (
            "simple",
            "bar_plot_simple",
            ["a", "b", "c", "d", "e", "f", "g", "h"],
            [10, 20, 30, 40, 50, 60, 70, 80],
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "all_features",
            "bar_plot_all_features",
            ["a", "b", "c", "d", "e", "f", "g", "h"],
            [10, 20, 30, 40, 50, 60, 70, 80],
            ["red", "green", "blue", "orange", "purple", "cyan", "blue", "blue"],
            "My amazing bar plot",
            "log",
            "log axis",
            None,
        ),
        (
            "all_features_arraylike",
            "bar_plot_all_features_arraylike_names",
            np.array(["a", "b", "c", "d", "e", "f", "g", "h"]),
            np.array([10, 20, 30, 40, 50, 60, 70, 80]),
            ["red", "green", "blue", "orange", "purple", "cyan", "blue", "blue"],
            "My amazing bar plot",
            "log",
            "log axis",
            None,
        ),
        (
            "different_input_types",
            "bar_plot_different_input_types",
            [10, 20, 30, 40, 50, 60, 70, 80],
            [10, 20, 30, 40, 50, 60, 70, 80],
            ["red", "green", "blue", (0.7, 0.7, 1), "purple", "cyan", (0.8, 0.9, 0.2, 0.5), "blue"],
            "My amazing bar plot",
            "log",
            "log axis",
            None,
        ),
        (
            "metadata",
            "bar_test_metadata",
            ["a", "b", "c", "d", "e", "f", "g", "h"],
            [10, 20, 30, 40, 50, 60, 70, 80],
            None,
            None,
            None,
            None,
            {"key": "value"},
        ),
    ],
)
def test_bar_plot(
    test_case: str,
    expected_output: str,
    names: Any,
    heights: Any,
    color: Any,
    title: Any,
    yscale: Any,
    ylabel: Any,
    metadata: Any,
    request: Any,
) -> None:
    serializer = MatplotlibSerializer()
    _, ax = serializer.subplots()
    ax.bar(names, heights, color=color)

    update_tests = request.config.getoption("--update-tests")

    if title:
        ax.set_title(title)
    if yscale:
        ax.set_yscale(yscale)
    if ylabel:
        ax.set_ylabel(ylabel)

    if metadata:
        ax.bar(names, heights, color=color)
        serializer.add_custom_metadata_figure(metadata)
        serializer.add_custom_metadata_plot(metadata, plot_selector=0)
        serializer.add_custom_metadata_axis(metadata, axis="y", plot_selector=0)
        serializer.add_custom_metadata_trace(metadata, trace_selector=1)
        serializer.add_custom_metadata_datapoints(metadata, trace_selector=0, point_selector=3)
    if update_tests == "confirm":
        serializer.write_json_file("./tests_updated/" + expected_output + ".json")
    else:
        validate_output(serializer, expected_output)
    plt.close()
