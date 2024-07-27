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
