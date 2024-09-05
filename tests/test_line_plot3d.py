from typing import Any

import numpy as np
import pytest

from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import validate_output


@pytest.mark.parametrize(
    (
        "test_case",
        "expected_output",
        "x",
        "y",
        "z",
        "label",
        "color",
        "linestyle",
        "marker",
        "linewidth",
        "title",
        "xlabel",
        "ylabel",
        "zlabel",
        "xlim",
        "ylim",
        "zlim",
        "metadata",
    ),
    [
        (
            "simple",
            "line_plot3D_simple",
            np.sin(np.arange(0, 10 * np.pi, np.pi / 50)),
            np.cos(np.arange(0, 10 * np.pi, np.pi / 50)),
            np.arange(0, 10 * np.pi, np.pi / 50),
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
            "line_plot3D_all_features",
            np.sin(np.arange(0, np.pi * 2, 0.1)),
            np.arange(0, np.pi * 2, 0.1),
            np.arange(0, np.pi * 2, 0.1),
            "line xzz",
            "green",
            "--",
            "<",
            None,
            "3-D line plot",
            "labelX",
            "labelY",
            "labelZ",
            (-1, 1),
            (0, 6.5),
            (0, 6.5),
            None,
        ),
        (
            "metadata",
            "line3D_test_metadata",
            np.sin(np.arange(0, 10 * np.pi, np.pi / 50)),
            np.cos(np.arange(0, 10 * np.pi, np.pi / 50)),
            np.arange(0, 10 * np.pi, np.pi / 50),
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
            {"key": "value"},
        ),
    ],
)
def test_line_plot3d(
    test_case: str,
    expected_output: str,
    x: Any,
    y: Any,
    z: Any,
    label: Any,
    color: Any,
    linestyle: Any,
    marker: Any,
    linewidth: Any,
    title: Any,
    xlabel: Any,
    ylabel: Any,
    zlabel: Any,
    xlim: Any,
    ylim: Any,
    zlim: Any,
    metadata: Any,
) -> None:
    serializer = MatplotlibSerializer()
    _, ax = serializer.subplots(subplot_kw={"projection": "3d"})

    ax.plot(x, y, z, label=label, color=color, linestyle=linestyle, marker=marker, linewidth=linewidth)

    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if zlabel:
        ax.set_zlabel(zlabel)
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    if zlim:
        ax.set_zlim(*zlim)

    if metadata:
        ax.plot(x, y, z, label=label, color=color, linestyle=linestyle, marker=marker, linewidth=linewidth)
        serializer.add_custom_metadata_figure(metadata)
        serializer.add_custom_metadata_plot(metadata, plot_selector=0)
        serializer.add_custom_metadata_axis(metadata, axis="z", plot_selector=0)
        serializer.add_custom_metadata_trace(metadata, trace_selector=1)
        serializer.add_custom_metadata_datapoints(metadata, trace_selector=0, point_selector=1)
        serializer.add_custom_metadata_datapoints(
            {"key2": "value2"},
            trace_selector=(1, 1, 5),
            trace_rel_tol=0.4,
            point_selector=(1, 1, 5),
            point_rel_tolerance=0.5,
        )

    validate_output(serializer, expected_output)
