from typing import Any

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
    ".plots/line_plot3D_all_features.json",
    "./plots/scatter3D_plot_marker.json",
    "./plots/surface_plot3D_all_features.json",
]


def test_deserializer(request: Any) -> None:
    rows, columns = 3, 3

    update_tests = request.config.getoption("--update-tests")

    serializer = MatplotlibSerializer()
    fig, ax = serializer.subplots(rows, columns)
    fig.suptitle("Amount of plots: " + str(len(files)))

    for i, file in enumerate(files):
        deserialize_from_json_file(file, ax[i // columns, i % columns])

    if update_tests == "confirm":
        fig.savefig("./tests/plots/deserializer2d.png")
