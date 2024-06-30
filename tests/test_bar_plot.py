from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import validate_output


def test_simple() -> None:
    serializer = MatplotlibSerializer()

    names = ["a", "b", "c", "d", "e", "f", "g", "h"]
    heights = [10, 20, 30, 40, 50, 60, 70, 80]

    _, ax = serializer.subplots()
    ax.bar(names, heights)

    validate_output(serializer, "bar_plot_simple")


def test_all_features() -> None:
    serializer = MatplotlibSerializer()

    names = ["a", "b", "c", "d", "e", "f", "g", "h"]
    heights = [10, 20, 30, 40, 50, 60, 70, 80]
    color = ["red", "green", "blue", "orange", "purple", "cyan", "blue", "blue"]

    _, ax = serializer.subplots()
    ax.bar(names, heights, color=color)
    ax.set_title("My amazing bar plot")

    ax.set_yscale("log")
    ax.set_ylabel("log axis")

    validate_output(serializer, "bar_plot_all_features")


def test_different_input_types() -> None:
    serializer = MatplotlibSerializer()

    heights = [10, 20, 30, 40, 50, 60, 70, 80]
    color = [
        "red",
        "green",
        "blue",
        (0.7, 0.7, 1),
        "purple",
        "cyan",
        (0.8, 0.9, 0.2, 0.5),
        "blue",
    ]

    _, ax = serializer.subplots()
    ax.bar(heights, heights, color=color)
    ax.set_title("My amazing bar plot")

    ax.set_yscale("log")
    ax.set_ylabel("log axis")

    validate_output(serializer, "bar_plot_different_input_types")
