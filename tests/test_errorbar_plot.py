from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import validate_output


def test_literal_and_array() -> None:
    serializer = MatplotlibSerializer()

    x = [1, 2]
    y = [4, 3]
    xerr = 2
    yerr = [4, 5]

    _, ax = serializer.subplots()
    ax.errorbar(x, y, xerr=xerr, yerr=yerr)

    validate_output(serializer, "errorbar_literal_and_array")


def test_all_features() -> None:
    serializer = MatplotlibSerializer()

    x = [1, 2]
    y = [4, 3]
    xerr = [[1, 2], [2, 3]]
    yerr = [3, 4]

    _, ax = serializer.subplots()
    ax.errorbar(
        x,
        y,
        xerr=xerr,
        yerr=yerr,
        color="green",
        ecolor="red",
        marker="o",
        label="Errorbartest",
    )
    ax.set_title("My amazing errorbar plot")

    ax.set_yscale("log")
    ax.set_ylabel("log axis")

    validate_output(serializer, "errorbar_all_features")
