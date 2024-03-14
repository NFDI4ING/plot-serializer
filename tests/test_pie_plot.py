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
    color = ["red", "green", "blue", "orange"]
    explode = [0.1, 0, 0.2, 0]

    _, ax = serializer.subplots()
    ax.pie(sizes, labels=labels, colors=color, explode=explode)

    ax.set_title("My amazing pie")

    validate_output(serializer, "pie_plot_all_features")
