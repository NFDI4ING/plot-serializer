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
        "labels",
        "sizes",
        "colors",
        "explode",
        "title",
        "metadata",
    ),
    [
        (
            "simple",
            "pie_plot_simple",
            ["Frogs", "Hogs", "Dogs", "Logs"],
            [15, 30, 45, 10],
            None,
            None,
            None,
            None,
        ),
        (
            "all_features",
            "pie_plot_all_features",
            ["Frogs", "Hogs", "Dogs", "Logs"],
            [15, 30, 45, 10],
            [(0.1, 0.1, 1, 1), "green", (0.7, 0.3, 0), "orange"],
            [0.1, 0, 0.2, 0],
            "My amazing pie",
            None,
        ),
        (
            "array_like",
            "pie_plot_array_like",
            ["Frogs", "Hogs", "Dogs", "Logs"],
            np.array([15, 30, 45, 10]),
            [(0.1, 0.1, 1, 1), "green", (0.7, 0.3, 0), "orange"],
            [0.1, 0, 0.2, 0],
            "Array-like pie",
            None,
        ),
        (
            "metadata",
            "pie_test_metadata",
            ["Frogs", "Hogs", "Dogs", "Logs"],
            [15, 30, 45, 10],
            None,
            None,
            None,
            {"key": "value"},
        ),
    ],
)
def test_pie_plot(
    test_case: str,
    expected_output: str,
    labels: Any,
    sizes: Any,
    colors: Any,
    explode: Any,
    title: Any,
    metadata: Any,
    request: Any,
) -> None:
    serializer = MatplotlibSerializer()

    update_tests = request.config.getoption("--update-tests")

    _, ax = serializer.subplots()
    ax.pie(sizes, labels=labels, colors=colors, explode=explode)

    if title:
        ax.set_title(title)

    if metadata:
        serializer.add_custom_metadata_figure(metadata)
        serializer.add_custom_metadata_plot(metadata, plot_selector=0)
        serializer.add_custom_metadata_datapoints(metadata, trace_selector=0, point_selector=1)

    if update_tests == "confirm":
        serializer.write_json_file("./tests_updated/" + expected_output + ".json")
    else:
        validate_output(serializer, expected_output)
    plt.close()
