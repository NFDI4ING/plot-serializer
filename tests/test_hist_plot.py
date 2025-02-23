from typing import Any

import numpy as np
import pytest
from matplotlib import pyplot as plt

from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import validate_output


@pytest.mark.parametrize(
    (
        "expected_output",
        "x",
        "bins",
        "color",
        "label",
        "cumulative",
        "density",
        "title",
        "yscale",
        "ylabel",
        "metadata",
    ),
    [
        (
            "hist_plot_simple",
            [1, 2, 2, 2, 5, 5, 8, 8],
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
            "hist_plot_all_features_single",
            [1, 2, 2, 2, 5, 5, 8, 8],
            "auto",
            "green",
            "dataset one",
            True,
            True,
            "My amazing hist plot",
            "log",
            "log axis",
            None,
        ),
        (
            "hist_plot_all_features_datasets",
            [[1, 2, 2, 2, 5, 5, 8], [1, 1, 1, 4, 4, 4, 4], [3, 3, 7, 7, 9, 9, 9]],
            [1, 4, 6, 8],
            ["orange", "black", "green"],
            ["dist1", "dist2", "dist3"],
            True,
            True,
            None,
            None,
            None,
            None,
        ),
        (
            "hist_plot_array_like",
            np.array([[1, 2, 2, 2, 5, 5, 8], [1, 1, 1, 4, 4, 4, 4], [3, 3, 7, 7, 9, 9, 9]]).T,
            [1, 4, 6, 8],
            ["orange", "black", "green"],
            ["dist1", "dist2", "dist3"],
            True,
            True,
            None,
            None,
            None,
            None,
        ),
        (
            "hist_test_metadata",
            [[1, 2, 2, 2, 5, 5, 8, 8], [1, 1, 1, 4, 4, 4, 4], [3, 3, 7, 7, 9, 9, 9]],
            None,
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
def test_hist_plot(
    expected_output: str,
    x: Any,
    bins: Any,
    color: Any,
    label: Any,
    cumulative: Any,
    density: Any,
    title: Any,
    yscale: Any,
    ylabel: Any,
    metadata: Any,
    request: Any,
) -> None:
    serializer = MatplotlibSerializer()

    update_tests = request.config.getoption("--update-tests")

    _, ax = serializer.subplots()
    if bins is None and cumulative is None and density is None:
        # giving arguments the none value throws errors, might need a test overhaul overall
        ax.hist(x)
    else:
        ax.hist(
            x,
            bins=bins,
            color=color,
            label=label,
            cumulative=cumulative,
            density=density,
        )

    if title:
        ax.set_title(title)
    if yscale:
        ax.set_yscale(yscale)
    if ylabel:
        ax.set_ylabel(ylabel)

    if metadata:
        ax.hist(x)
        serializer.add_custom_metadata_figure(metadata)
        serializer.add_custom_metadata_plot(metadata, plot_selector=0)
        serializer.add_custom_metadata_axis(metadata, axis="y", plot_selector=0)
        serializer.add_custom_metadata_trace(metadata, trace_selector=1)
        serializer.add_custom_metadata_datapoints(metadata, trace_selector=0, point_selector=1)

    if update_tests == "confirm":
        serializer.write_json_file("./tests_updated/" + expected_output + ".json")
    else:
        validate_output(serializer, expected_output)
    plt.close()
