import json
from typing import Any
import numpy as np
from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import read_plot
from mpl_toolkits.mplot3d.axes3d import Axes3D as MplAxes3D


def test_simple() -> None:

    serializer = MatplotlibSerializer()

    z = np.arange(0, 10 * np.pi, np.pi / 50)
    x = np.sin(z)
    y = np.cos(z)

    _, ax = serializer.subplots(subplot_kw={"projection": "3d"})

    ax.plot(x, y, z)

    json_string = serializer.to_json()

    output = json.loads(json_string)

    expected = json.loads(read_plot("line_plot3D_simple"))
    assert output == expected


def test_all_features() -> None:
    serializer = MatplotlibSerializer()

    z = np.arange(0, np.pi * 2, 0.1)
    x = np.sin(z)
    y = np.cos(z)

    _, ax = serializer.subplots(subplot_kw={"projection": "3d"})

    ax.plot(x, z, z, label="line xzz", color="green", linestyle="--")
    ax.plot(y, z, z, label="line yzz", color="red", linewidth=2)

    ax.set_title("3-D line plot")

    ax.legend()
    ax.set_xlim(-1, 1)
    ax.set_ylim(0, 6.5)
    ax.set_zlim(0, 6.5)

    ax.set_xlabel("labelX")
    ax.set_ylabel("labelY")
    ax.set_zlabel("labelZ")

    json_string = serializer.to_json(emit_warnings=True)

    output = json.loads(json_string)

    expected = json.loads(read_plot("line_plot3D_all_features"))

    assert output == expected
