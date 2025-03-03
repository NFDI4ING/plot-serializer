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
    arrays(np.float64, shape=st.integers(min_value=1, max_value=10)),
)

y_strategy = st.one_of(
    st.floats(allow_nan=False, allow_infinity=False),
    st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    arrays(np.float64, shape=st.integers(min_value=1, max_value=10)),
)

xerr_strategy = st.one_of(
    st.none(),
    st.floats(min_value=0, allow_nan=False, allow_infinity=False),
    st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1),
    arrays(np.float64, shape=st.integers(min_value=1, max_value=10)),
    arrays(np.float64, shape=st.tuples(st.just(2), st.integers(min_value=1, max_value=10))),
)

yerr_strategy = st.one_of(
    st.none(),
    st.floats(min_value=0, allow_nan=False, allow_infinity=False),
    st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1),
    arrays(np.float64, shape=st.integers(min_value=1, max_value=10)),
    arrays(np.float64, shape=st.tuples(st.just(2), st.integers(min_value=1, max_value=10))),
)

marker_strategy = st.one_of(st.none(), st.text())

label_strategy = st.one_of(st.none(), st.text())


@given(x=x_strategy, y=y_strategy, xerr=xerr_strategy, yerr=yerr_strategy, marker=marker_strategy, label=label_strategy)
def test_bar_properties(
    x: Any,
    y: Any,
    xerr: Any,
    yerr: Any,
    marker: Any,
    label: Any,
) -> None:
    serializer = MatplotlibSerializer()
    _, serializer_ax = serializer.subplots()
    _fig, ax = plt.subplots()
    try:
        ax.errorbar(x, y, xerr=xerr, yerr=yerr, marker=marker, label=label)
    except Exception as _e:
        pass
    else:
        serializer_ax.errorbar(x, y, xerr=xerr, yerr=yerr, marker=marker, label=label)
        assert serializer.to_json() != "{}", "Serialized JSON is empty check input"
    finally:
        plt.close(_)
        plt.close(_fig)
