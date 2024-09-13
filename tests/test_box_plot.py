from typing import Any

import pytest

from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import validate_output


@pytest.mark.parametrize(
    (
        "test_case",
        "expected_output",
        "array2d",
        "labels",
        "notch",
        "whis",
        "bootstrap",
        "usermedians",
        "conf_intervals",
        "title",
        "yscale",
        "ylabel",
        "metadata",
    ),
    [
        (
            "simple",
            "box_plot_simple",
            [[4, 5, 6, 7, 8], [1, 2, 4, 16, 32], [25, 16, 9, 4, 1]],
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
            "box_plot_all_features",
            [[4, 5, 6, 7, 8], [1, 2, 4, 16, 32], [25, 16, 9, 4, 1]],
            ["linear", "powerOfTwo", "squares"],
            True,
            (1.5, 1.5),
            5000,
            [6, 4, 9],
            [(1, 1), (4, 9), (5, 5)],
            "My amazing box plot",
            None,
            None,
            None,
        ),
        (
            "metadata",
            "box_test_metadata",
            [[4, 5, 6, 7, 8], [1, 2, 4, 16, 32], [25, 16, 9, 4, 1]],
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
def test_box_plot(
    test_case: str,
    expected_output: str,
    array2d: Any,
    labels: Any,
    notch: Any,
    whis: Any,
    bootstrap: Any,
    usermedians: Any,
    conf_intervals: Any,
    title: Any,
    yscale: Any,
    ylabel: Any,
    metadata: Any,
) -> None:
    serializer = MatplotlibSerializer()

    _, ax = serializer.subplots()
    ax.boxplot(
        array2d,
        tick_labels=labels,
        notch=notch,
        whis=whis,
        bootstrap=bootstrap,
        usermedians=usermedians,
        conf_intervals=conf_intervals,
    )

    if title:
        ax.set_title(title)
    if yscale:
        ax.set_yscale(yscale)
    if ylabel:
        ax.set_ylabel(ylabel)

    if metadata:
        ax.boxplot(
            array2d,
            tick_labels=labels,
            notch=notch,
            whis=whis,
            bootstrap=bootstrap,
            usermedians=usermedians,
            conf_intervals=conf_intervals,
        )
        serializer.add_custom_metadata_figure(metadata)
        serializer.add_custom_metadata_plot(metadata, plot_selector=0)
        serializer.add_custom_metadata_axis(metadata, axis="y", plot_selector=0)
        serializer.add_custom_metadata_trace(metadata, trace_selector=1)
        serializer.add_custom_metadata_datapoints(metadata, trace_selector=0, point_selector=2)

    validate_output(serializer, expected_output)
