from typing import Any

from matplotlib import pyplot as plt

from plot_serializer.matplotlib.deserializer import deserialize_from_json_file
from plot_serializer.matplotlib.serializer import MatplotlibSerializer

files = [
    "./tests/plots/bar_plot_all_features.json",
    "./tests/plots/box_plot_all_features.json",
    "./tests/plots/errorbar_all_features.json",
    "./tests/plots/hist_plot_all_features_datasets.json",
    "./tests/plots/line_plot_all_features.json",
    "./tests/plots/pie_plot_all_features.json",
    "./tests/plots/scatter_plot_all_enabled.json",
]

files3d = [
    "./tests/plots/line_plot3D_all_features.json",
    "./tests/plots/scatter3D_plot_marker.json",
    "./tests/plots/surface_plot3D_all_features.json",
]


def test_deserializer(request: Any) -> None:
    rows, columns = 3, 3

    update_tests = request.config.getoption("--update-tests")

    serializer = MatplotlibSerializer()
    fig, ax = serializer.subplots(rows, columns, figsize=(15, 10))
    fig.suptitle("Amount of plots: " + str(len(files)))

    for i in range(len(files)):
        deserialize_from_json_file(files[i], ax=ax[i // columns, i % columns])

    if update_tests == "confirm":
        fig.savefig("./tests/deserializer_matrix/new_deserializer2d.png")

    plt.close()


def test_deserializer3d(request: Any) -> None:
    rows, columns = 2, 2

    update_tests = request.config.getoption("--update-tests")

    serializer = MatplotlibSerializer()
    fig, ax = serializer.subplots(rows, columns, figsize=(15, 10), subplot_kw={"projection": "3d"})
    fig.suptitle("Amount of plots: " + str(len(files3d)))

    for i in range(len(files3d)):
        deserialize_from_json_file(files3d[i], ax=ax[i // columns, i % columns])

    if update_tests == "confirm":
        fig.savefig("./tests/deserializer_matrix/new_deserializer3d.png")

    plt.close()
