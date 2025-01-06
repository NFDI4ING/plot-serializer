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
        "sizes",
        "color",
        "marker",
        "title",
        "metadata",
    ),
    [
        (
            "simple",
            "scatter_plot_simple",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "sizes",
            "scatter_plot_sizes",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            [1, 5, 10, 20, 30],
            None,
            None,
            None,
            None,
        ),
        (
            "color",
            "scatter_plot_color",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            None,
            "green",
            None,
            None,
            None,
        ),
        (
            "color_list_string",
            "scatter_plot_color_list",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            None,
            ["green", "blue", "red", "yellow", "black"],
            None,
            None,
            None,
        ),
        (
            "all_enabled",
            "scatter_plot_all_enabled",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            [1, 5, 10, 20, 30],
            [1, 0.5, 3, 0.2, 0.1],
            "<",
            None,
            None,
        ),
        (
            "array_like",
            "scatter_plot_array_like",
            np.array([1, 2, 3, 4, 3]),
            np.array([2, 1.5, 5, 0, 4]),
            np.array([1, 5, 10, 20, 30]),
            [1, 0.5, 3, 0.2, 0.1],
            "<",
            None,
            None,
        ),
        (
            "metadata",
            "scatter_test_metadata",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            None,
            None,
            None,
            None,
            {"key": "value"},
        ),
    ],
)
def test_scatter_plot(
    test_case: str,
    expected_output: str,
    x: Any,
    y: Any,
    sizes: Any,
    color: Any,
    marker: Any,
    title: Any,
    metadata: Any,
    request: Any,
) -> None:
    serializer = MatplotlibSerializer()

    update_tests = request.config.getoption("--update-tests")

    _, ax = serializer.subplots()
    ax.scatter(x, y, s=sizes, c=color, marker=marker)

    if title:
        ax.set_title(title)

    if metadata:
        ax.scatter(x, y, s=sizes, c=color, marker=marker)
        serializer.add_custom_metadata_figure(metadata)
        serializer.add_custom_metadata_plot(metadata, plot_selector=0)
        serializer.add_custom_metadata_axis(metadata, axis="y", plot_selector=0)
        serializer.add_custom_metadata_trace(metadata, trace_selector=1)
        serializer.add_custom_metadata_datapoints(metadata, trace_selector=0, point_selector=1)
        serializer.add_custom_metadata_datapoints(
            {"key2": "value2"}, trace_selector=(3, 5), trace_rel_tol=0.1, point_selector=(4, 0), point_rel_tolerance=0.2
        )

    if update_tests == "confirm":
        serializer.write_json_file("./tests_updated/" + expected_output + ".json")
    else:
        validate_output(serializer, expected_output)
    plt.close()
