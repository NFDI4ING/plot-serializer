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
    st.lists(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), min_size=1),
    st.lists(arrays(dtype=np.float64, shape=st.integers(min_value=1, max_value=10)), min_size=1),
    arrays(
        dtype=np.float64,
        shape=st.tuples(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10)),
    ),
)
bins_strategy = st.one_of(
    st.integers(min_value=1, max_value=50),
    st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    arrays(dtype=np.float64, shape=st.integers(min_value=1, max_value=50)),
)
density_strategy = st.booleans()
cumulative_strategy = st.one_of(st.booleans(), st.just(-1))
label_strategy = st.one_of(st.none(), st.text())


@given(
    x=x_strategy, bins=bins_strategy, label=label_strategy, densitiy=density_strategy, culumative=cumulative_strategy
)
def test_hist_properties(
    x: Any,
    bins: Any,
    label: Any,
    densitiy: Any,
    culumative: Any,
) -> None:
    serializer = MatplotlibSerializer()
    _, serializer_ax = serializer.subplots()
    _fig, ax = plt.subplots()
    try:
        ax.hist(x, bins=bins, label=label, density=densitiy, cumulative=culumative)
    except Exception as _e:
        pass
    else:
        serializer_ax.hist(x, bins=bins, label=label, density=densitiy, cumulative=culumative)
        assert serializer.to_json() != "{}", "Serialized JSON is empty check input"
    finally:
        plt.close(_)
        plt.close(_fig)
