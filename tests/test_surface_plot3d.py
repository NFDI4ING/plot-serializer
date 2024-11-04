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
        "z",
        "color",
        "label",
        "title",
        "xlabel",
        "ylabel",
        "zlabel",
        "metadata",
    ),
    [
        (
            "simple",
            "surface_plot3D_simple",
            np.arange(-2, 2, 0.5),
            np.arange(-2, 2, 0.5),
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
            "surface_plot3D_all_features",
            np.outer(np.linspace(-3, 3, 20), np.ones(20)),
            None,
            np.sin(np.outer(np.linspace(-3, 3, 20), np.ones(20)) ** 2)
            + np.cos(np.outer(np.linspace(-3, 3, 20), np.ones(20)).T ** 2),
            "yellow",
            "testSurface",
            "testTitle",
            "labelX",
            "labelY",
            "labelZ",
            None,
        ),
        (
            "metadata",
            "surface_plot3D_test_metadata",
            np.arange(-2, 2, 0.5),
            np.arange(-2, 2, 0.5),
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
def test_surface_plot3d(
    test_case: str,
    expected_output: str,
    x: Any,
    y: Any,
    z: Any,
    color: Any,
    label: Any,
    title: Any,
    xlabel: Any,
    ylabel: Any,
    zlabel: Any,
    metadata: Any,
    request: Any,
) -> None:
    serializer = MatplotlibSerializer()

    update_tests = request.config.getoption("--update-tests")

    _, ax = serializer.subplots(subplot_kw={"projection": "3d"})

    if y is None:
        y = x.copy().T  # transpose if y is not provided
    if z is None:
        x, y = np.meshgrid(x, y)
        z = -(x**2 + y**2)

    ax.plot_surface(x, y, z, color=color, label=label)

    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if zlabel:
        ax.set_zlabel(zlabel)

    if metadata:
        ax.plot_surface(x, y, z, color=color, label=label)
        serializer.add_custom_metadata_figure(metadata)
        serializer.add_custom_metadata_plot(metadata, plot_selector=0)
        serializer.add_custom_metadata_axis(metadata, axis="z", plot_selector=0)
        serializer.add_custom_metadata_trace(metadata, trace_selector=1)
        serializer.add_custom_metadata_datapoints(metadata, trace_selector=0, point_selector=1)
        serializer.add_custom_metadata_datapoints(
            {"key2": "value2"},
            trace_selector=(-2, 2, 8),
            trace_rel_tol=1,
            point_selector=(-2, 2, 8),
            point_rel_tolerance=1,
        )

    if update_tests == "confirm":
        serializer.write_json_file("./tests_updated/" + expected_output + ".json")
    else:
        validate_output(serializer, expected_output)
    plt.close()
