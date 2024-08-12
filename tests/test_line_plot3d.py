import numpy as np

from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import validate_output


def test_simple() -> None:
    serializer = MatplotlibSerializer()

    z = np.arange(0, 10 * np.pi, np.pi / 50)
    x = np.sin(z)
    y = np.cos(z)

    _, ax = serializer.subplots(subplot_kw={"projection": "3d"})

    ax.plot(x, y, z)

    validate_output(serializer, "line_plot3D_simple")


def test_all_features() -> None:
    serializer = MatplotlibSerializer()

    z = np.arange(0, np.pi * 2, 0.1)
    x = np.sin(z)
    y = np.cos(z)

    _, ax = serializer.subplots(subplot_kw={"projection": "3d"})

    ax.plot(x, z, z, label="line xzz", color="green", linestyle="--", marker="<")
    ax.plot(y, z, z, label="line yzz", color=(0.3, 0.7, 1), linewidth=2, marker=".")

    ax.set_title("3-D line plot")

    ax.legend()
    ax.set_xlim(-1, 1)
    ax.set_ylim(0, 6.5)
    ax.set_zlim(0, 6.5)

    ax.set_xlabel("labelX")
    ax.set_ylabel("labelY")
    ax.set_zlabel("labelZ")

    validate_output(serializer, "line_plot3D_all_features")


def test_metadata() -> None:
    serializer = MatplotlibSerializer()

    z = np.arange(0, 10 * np.pi, np.pi / 50)
    x = np.sin(z)
    y = np.cos(z)

    _, ax = serializer.subplots(subplot_kw={"projection": "3d"})

    ax.plot(x, y, z)
    ax.plot(x, y, z)
    dict = {"key": "value"}
    serializer.add_custom_metadata_figure(dict)
    serializer.add_custom_metadata_plot(dict, plot_selector=0)
    serializer.add_custom_metadata_axis(dict, axis="z", plot_selector=0)
    serializer.add_custom_metadata_trace(dict, trace_selector=1)
    serializer.add_custom_metadata_datapoints(dict, trace_selector=0, point_selector=1)
    serializer.add_custom_metadata_datapoints(
        {"key2": "value2"},
        trace_selector=(1, 1, 5),
        trace_rel_tol=0.4,
        point_selector=(1, 1, 5),
        point_rel_tolerance=0.5,
    )

    validate_output(serializer, "line3D_test_metadata")
