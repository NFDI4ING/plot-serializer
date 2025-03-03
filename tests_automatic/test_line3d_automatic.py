from typing import Any

import numpy as np
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays
from matplotlib import pyplot as plt

from plot_serializer.matplotlib.serializer import MatplotlibSerializer

x_strategy = st.one_of(
    st.floats(allow_nan=False, allow_infinity=False),
    st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    arrays(dtype=np.float64, shape=st.integers(min_value=1, max_value=10)),
)

y_strategy = st.one_of(
    st.floats(allow_nan=False, allow_infinity=False),
    st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    arrays(dtype=np.float64, shape=st.integers(min_value=1, max_value=10)),
)

z_strategy = st.one_of(
    st.floats(allow_nan=False, allow_infinity=False),
    st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    arrays(dtype=np.float64, shape=st.integers(min_value=1, max_value=10)),
)

label_strategy = st.one_of(st.none(), st.text())

linewidth_strategy = st.one_of(st.floats(allow_nan=False, allow_infinity=False), st.integers())


@given(x=x_strategy, y=y_strategy, z=z_strategy, label=label_strategy, linewidth=linewidth_strategy)
def test_line_properties(
    x: Any,
    y: Any,
    z: Any,
    label: Any,
    linewidth: Any,
) -> None:
    serializer = MatplotlibSerializer()
    _, serializer_ax = serializer.subplots()
    _fig, ax = plt.subplots()
    try:
        ax.plot(x, y, z, label=label, linewidth=linewidth)
    except Exception as _e:
        pass
    else:
        serializer_ax.plot(x, y, z, label=label, linewidth=linewidth)
        assert serializer.to_json() != "{}", "Serialized JSON is empty check input"
    finally:
        plt.close(_)
        plt.close(_fig)
