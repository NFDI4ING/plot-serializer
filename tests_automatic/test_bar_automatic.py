from typing import Any

import numpy as np
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays
from matplotlib import pyplot as plt

from plot_serializer.matplotlib.serializer import MatplotlibSerializer

x_strategy = st.one_of(
    st.integers(),
    st.floats(),
    st.text(),
    st.lists(st.text()),
    st.lists(st.integers()),
    st.lists(st.floats()),
    arrays(np.int64, st.integers(min_value=0, max_value=10)),
    arrays(np.float64, st.integers(min_value=0, max_value=10)),
)
heights_strategy = st.one_of(
    st.integers(),
    st.floats(),
    st.lists(st.integers()),
    st.lists(st.floats()),
    arrays(np.int64, st.integers(min_value=0, max_value=10)),
    arrays(np.float64, st.integers(min_value=0, max_value=10)),
)


@given(x=x_strategy, heights=heights_strategy)
def test_bar_properties(
    x: Any,
    heights: Any,
) -> None:
    serializer = MatplotlibSerializer()
    _, serializer_ax = serializer.subplots()
    _fig, ax = plt.subplots()
    try:
        ax.bar(x, heights)
    except Exception as _e:
        pass
    else:
        serializer_ax.bar(x, heights)
        assert serializer.to_json() != "{}", "Serialized JSON is empty check input"
    finally:
        plt.close(_)
        plt.close(_fig)
