from typing import Any

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
        "sizes",
        "color",
        "cmap",
        "marker",
        "title",
        "xlabel",
        "ylabel",
        "zlabel",
        "metadata",
    ),
    [
        (
            "simple",
            "scatter3D_plot_simple",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            [3, 2, 1, 0.5, 2],
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
            "marker",
            "scatter3D_plot_marker",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            [3, 2, 1, 0.5, 2],
            None,
            None,
            None,
            "<",
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "size",
            "scatter3D_plot_size",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            [3, 2, 1, 0.5, 2],
            5,
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
            "sizes_list",
            "scatter3D_plot_size_list",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            [3, 2, 1, 0.5, 2],
            [1, 5, 10, 20, 30],
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
            "color_string",
            "scatter3D_plot_color_string",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            [3, 2, 1, 0.5, 2],
            None,
            "green",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "color_list_string",
            "scatter3D_plot_color_string_list",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            [3, 2, 1, 0.5, 2],
            None,
            ["green", "blue", "red", "yellow", "black"],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "color_hex",
            "scatter3D_plot_color_hex",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            [3, 2, 1, 0.5, 2],
            None,
            ["#008000ff", "#0000ffff", "#ff0000ff", "#ffff00ff", "#000000ff"],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "color_rgb",
            "scatter3D_plot_color_rgb",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            [3, 2, 1, 0.5, 2],
            None,
            [
                (0.0, 0.5019607843137255, 0.0),
                (0.0, 0.0, 1.0),
                (1.0, 0.0, 0.0),
                (1.0, 1.0, 0.0),
                (0.0, 0.0, 0.0),
            ],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "color_cmap",
            "scatter3D_plot_color_cmap",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            [3, 2, 1, 0.5, 2],
            None,
            [0.1, 0.4, 0.6, 0.8, 1],
            "cividis",
            None,
            "via cividis cmap",
            "testX",
            "testY",
            "testZ",
            None,
        ),
        (
            "metadata",
            "scatter3D_test_metadata",
            [1, 2, 3, 4, 3],
            [2, 1.5, 5, 0, 4],
            [3, 2, 1, 0.5, 2],
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
def test_scatter3d_plot(
    test_case: str,
    expected_output: str,
    x: Any,
    y: Any,
    z: Any,
    sizes: Any,
    color: Any,
    cmap: Any,
    marker: Any,
    title: Any,
    xlabel: Any,
    ylabel: Any,
    zlabel: Any,
    metadata: Any,
) -> None:
    serializer = MatplotlibSerializer()
    _, ax = serializer.subplots(subplot_kw={"projection": "3d"})
    if not sizes:
        ax.scatter(x, y, z, c=color, cmap=cmap, marker=marker)
    else:
        ax.scatter(x, y, z, s=sizes, c=color, cmap=cmap, marker=marker)

    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if zlabel:
        ax.set_zlabel(zlabel)

    if metadata:
        if not sizes:
            ax.scatter(x, y, z, c=color, cmap=cmap, marker=marker)
        else:
            ax.scatter(x, y, z, s=sizes, c=color, cmap=cmap, marker=marker)
        serializer.add_custom_metadata_figure(metadata)
        serializer.add_custom_metadata_plot(metadata, plot_selector=0)
        serializer.add_custom_metadata_axis(metadata, axis="z", plot_selector=0)
        serializer.add_custom_metadata_trace(metadata, trace_selector=1)
        serializer.add_custom_metadata_datapoints(metadata, trace_selector=0, point_selector=1)
        serializer.add_custom_metadata_datapoints(
            {"key2": "value2"},
            trace_selector=(2, 1.5, 2),
            trace_rel_tol=0.2,
            point_selector=(2, 1, 5),
            point_rel_tolerance=0.5,
        )

    validate_output(serializer, expected_output)
