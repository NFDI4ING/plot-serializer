from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import validate_output


def test_simple() -> None:
    serializer = MatplotlibSerializer()

    x = [4, 5, 6, 7, 8]
    y = [1, 2, 4, 16, 32]
    z = [25, 16, 9, 4, 1]
    array2d = [x, y, z]

    _, ax = serializer.subplots()
    ax.boxplot(array2d)

    validate_output(serializer, "box_plot_simple")


def test_all_features() -> None:
    serializer = MatplotlibSerializer()

    x = [4, 5, 6, 7, 8]
    y = [1, 2, 4, 16, 32]
    z = [25, 16, 9, 4, 1]
    array2d = [x, y, z]
    labels = ["linear", "powerOfTwo", "squares"]
    usermedians = [6, 4, 9]
    conf_intervals = [(1, 1), (4, 9), (5, 5)]

    _, ax = serializer.subplots()
    ax.boxplot(
        array2d,
        tick_labels=labels,
        notch=True,
        whis=(1.5, 1.5),
        bootstrap=5000,
        usermedians=usermedians,
        conf_intervals=conf_intervals,
    )
    ax.set_title("My amazing box plot")

    validate_output(serializer, "box_plot_all_features")
