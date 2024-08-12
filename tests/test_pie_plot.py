from typing import List, Tuple

from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import validate_output


def test_simple() -> None:
    serializer = MatplotlibSerializer()

    labels = "Frogs", "Hogs", "Dogs", "Logs"
    sizes = [15, 30, 45, 10]

    _, ax = serializer.subplots()
    ax.pie(sizes, labels=labels)

    validate_output(serializer, "pie_plot_simple")


def test_all_features() -> None:
    serializer = MatplotlibSerializer()

    labels = "Frogs", "Hogs", "Dogs", "Logs"
    sizes = [15, 30, 45, 10]
    color: List[Tuple[float, float, float, float] | Tuple[float, float, float] | str] = [
        (0.1, 0.1, 1, 1),
        "green",
        (0.7, 0.3, 0),
        "orange",
    ]
    explode = [0.1, 0, 0.2, 0]

    _, ax = serializer.subplots()
    ax.pie(sizes, labels=labels, colors=color, explode=explode)

    ax.set_title("My amazing pie")

    validate_output(serializer, "pie_plot_all_features")


def test_metadata() -> None:
    serializer = MatplotlibSerializer()

    labels = "Frogs", "Hogs", "Dogs", "Logs"
    sizes = [15, 30, 45, 10]

    _, ax = serializer.subplots()
    ax.pie(sizes, labels=labels)
    dict = {"key": "value"}
    serializer.add_custom_metadata_figure(dict)
    serializer.add_custom_metadata_plot(dict, plot_selector=0)
    serializer.add_custom_metadata_datapoints(dict, trace_selector=0, point_selector=1)

    validate_output(serializer, "pie_test_metadata")
