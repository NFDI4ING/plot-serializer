from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import validate_output


def test_simple() -> None:
    serializer = MatplotlibSerializer()

    x = [1, 2, 3, 4, 3]
    y = [2, 1.5, 5, 0, 4]

    _, ax = serializer.subplots()
    ax.scatter(x, y)

    validate_output(serializer, "scatter_plot_simple")


def test_sizes() -> None:
    serializer = MatplotlibSerializer()

    x = [1, 2, 3, 4, 3]
    y = [2, 1.5, 5, 0, 4]
    sizes = [1, 5, 10, 20, 30]

    _, ax = serializer.subplots()
    ax.scatter(x, y, s=sizes)

    validate_output(serializer, "scatter_plot_sizes")


def test_color() -> None:
    serializer = MatplotlibSerializer()

    x = [1, 2, 3, 4, 3]
    y = [2, 1.5, 5, 0, 4]
    color = "green"

    _, ax = serializer.subplots()
    ax.scatter(x, y, c=color)

    validate_output(serializer, "scatter_plot_color")


def test_color_list_string() -> None:
    serializer = MatplotlibSerializer()

    x = [1, 2, 3, 4, 3]
    y = [2, 1.5, 5, 0, 4]
    color = ["green", "blue", "red", "yellow", "black"]

    _, ax = serializer.subplots()
    ax.scatter(x, y, c=color)

    validate_output(serializer, "scatter_plot_color_list")


def test_all_enabled() -> None:
    serializer = MatplotlibSerializer()

    x = [1, 2, 3, 4, 3]
    y = [2, 1.5, 5, 0, 4]
    color = [1, 0.5, 3, 0.2, 0.1]
    sizes = [1, 5, 10, 20, 30]

    _, ax = serializer.subplots()
    ax.scatter(x, y, c=color, s=sizes, marker="<")

    validate_output(serializer, "scatter_plot_all_enabled")


def test_metadata() -> None:
    serializer = MatplotlibSerializer()

    x = [1, 2, 3, 4, 3]
    y = [2, 1.5, 5, 0, 4]

    _, ax = serializer.subplots()
    ax.scatter(x, y)
    ax.scatter(x, y)
    dict = {"key": "value"}
    serializer.add_custom_metadata_figure(dict)
    serializer.add_custom_metadata_plot(dict, plot_selector=0)
    serializer.add_custom_metadata_axis(dict, axis="y", plot_selector=0)
    serializer.add_custom_metadata_trace(dict, trace_selector=1)
    serializer.add_custom_metadata_datapoints(dict, trace_selector=0, point_selector=1)
    serializer.add_custom_metadata_datapoints(
        {"key2": "value2"}, trace_selector=(3, 5), trace_rel_tol=0.1, point_selector=(4, 0), point_rel_tolerance=0.2
    )

    validate_output(serializer, "scatter_test_metadata")
