import numpy as np

from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import validate_output


def test_simple() -> None:
    serializer = MatplotlibSerializer()
    _, ax = serializer.subplots(subplot_kw={"projection": "3d"})

    x = np.arange(-2, 2, 0.5)
    y = np.arange(-2, 2, 0.5)
    x, y = np.meshgrid(x, y)
    z = -(x**2 + y**2)

    ax.plot_surface(x, y, z)

    validate_output(serializer, "surface_plot3D_simple")


def test_all_features() -> None:
    serializer = MatplotlibSerializer()
    _, ax = serializer.subplots(subplot_kw={"projection": "3d"})

    x = np.outer(np.linspace(-3, 3, 20), np.ones(20))
    y = x.copy().T  # transpose
    z = np.sin(x**2) + np.cos(y**2)

    ax.plot_surface(x, y, z, color="yellow", label="testSurface")

    ax.set_xlabel("labelX")
    ax.set_ylabel("labelY")
    ax.set_zlabel("labelZ")

    ax.set_title("testTitle")

    validate_output(serializer, "surface_plot3D_all_features")
