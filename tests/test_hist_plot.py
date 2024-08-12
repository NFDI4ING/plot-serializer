from plot_serializer.matplotlib.serializer import MatplotlibSerializer
from tests import validate_output


def test_simple() -> None:
    serializer = MatplotlibSerializer()

    x = [1, 2, 2, 2, 5, 5, 8, 8]

    _, ax = serializer.subplots()
    ax.hist(x)

    validate_output(serializer, "hist_plot_simple")


def test_all_features_single() -> None:
    serializer = MatplotlibSerializer()

    x = [1, 2, 2, 2, 5, 5, 8, 8]

    _, ax = serializer.subplots()
    ax.hist(
        x,
        bins="auto",
        color="green",
        label="dataset one",
        cumulative=True,
        density=True,
    )
    ax.set_title("My amazing hist plot")

    ax.set_yscale("log")
    ax.set_ylabel("log axis")

    validate_output(serializer, "hist_plot_all_features_single")


def test_all_features_datasets() -> None:
    serializer = MatplotlibSerializer()

    x = [1, 2, 2, 2, 5, 5, 8, 8]
    y = [1, 1, 1, 4, 4, 4, 4]
    z = [3, 3, 7, 7, 9, 9, 9]

    _, ax = serializer.subplots()
    ax.hist(
        [x, y, z],
        bins=[1, 4, 6, 8],
        color=["orange", "black", "green"],
        label=["dist1", "dist2", "dist3"],
        cumulative=True,
        density=True,
    )

    validate_output(serializer, "hist_plot_all_features_datasets")


def test_metadata() -> None:
    serializer = MatplotlibSerializer()

    x = [1, 2, 2, 2, 5, 5, 8, 8]
    y = [1, 1, 1, 4, 4, 4, 4]
    z = [3, 3, 7, 7, 9, 9, 9]

    _, ax = serializer.subplots()
    ax.hist([x, y, z])
    ax.hist([x, y, z])
    dict = {"key": "value"}
    serializer.add_custom_metadata_figure(dict)
    serializer.add_custom_metadata_plot(dict, plot_selector=0)
    serializer.add_custom_metadata_axis(dict, axis="y", plot_selector=0)
    serializer.add_custom_metadata_trace(dict, trace_selector=1)
    serializer.add_custom_metadata_datapoints(dict, trace_selector=0, point_selector=1)

    validate_output(serializer, "hist_test_metadata")
