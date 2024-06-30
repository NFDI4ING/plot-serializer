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
