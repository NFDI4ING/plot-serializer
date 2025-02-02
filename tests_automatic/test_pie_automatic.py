from typing import Any

import numpy as np
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays
from matplotlib import pyplot as plt

from plot_serializer.matplotlib.serializer import MatplotlibSerializer

x_strategy = st.one_of(
    st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    arrays(dtype=np.float64, shape=st.integers(min_value=1, max_value=10)),
)

explode_strategy = st.one_of(
    st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    arrays(dtype=np.float64, shape=st.integers(min_value=1, max_value=10)),
    st.none(),
)

radius_strategy = st.floats(allow_nan=False, allow_infinity=False)

labels_strategy = st.one_of(st.lists(st.text(), min_size=1), st.none())


@given(x=x_strategy, explode=explode_strategy, labels=labels_strategy, radius=radius_strategy)
def test_pie_properties(
    x: Any,
    explode: Any,
    labels: Any,
    radius: Any,
) -> None:
    serializer = MatplotlibSerializer()
    _, serializer_ax = serializer.subplots()
    _fig, ax = plt.subplots()
    try:
        ax.pie(x, explode=explode, labels=labels, radius=radius)
    except Exception as _e:
        pass
    else:
        serializer_ax.pie(x, explode=explode, labels=labels, radius=radius)
        assert serializer.to_json() != "{}", "Serialized JSON is empty check input"
    finally:
        plt.close(_)
        plt.close(_fig)
