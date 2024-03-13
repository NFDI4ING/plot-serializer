import json
from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import read_plot


def test_simple() -> None:
    serializer = MatplotlibSerializer()

    x = [4, 5, 6, 7, 8]
    y = [1, 2, 4, 16, 32]
    z = [25, 16, 9, 4, 1]
    array2d = [x, y, z]

    _, ax = serializer.subplots()
    ax.boxplot(array2d)

    json_string = serializer.to_json()
    output = json.loads(json_string)
    expected = json.loads(read_plot("box_plot_simple"))

    assert output == expected


def test_all_features() -> None:
    serializer = MatplotlibSerializer()

    x = [4, 5, 6, 7, 8]
    y = [1, 2, 4, 16, 32]
    z = [25, 16, 9, 4, 1]
    array2d = [x, y, z]
    labels = ["linear", None, "squares"]
    usermedians = [6, None, 9]
    conf_intervals = [(1, 1), (4, 9), None]

    _, ax = serializer.subplots()
    ax.boxplot(
        array2d,
        labels=labels,
        notch=True,
        whis=(1.5, 1.5),
        bootstrap=5000,
        usermedians=usermedians,
        conf_intervals=conf_intervals,
    )
    ax.set_title("My amazing box plot")

    json_string = serializer.to_json()
    output = json.loads(json_string)
    expected = json.loads(read_plot("box_plot_all_features"))

    assert output == expected
