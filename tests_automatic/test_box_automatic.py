from typing import Any

import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays
from matplotlib import pyplot as plt

from plot_serializer.matplotlib.serializer import MatplotlibSerializer

x_strategy = st.one_of(
    st.lists(st.lists(st.floats(), min_size=1), min_size=1),
    st.lists(arrays(np.float64, st.integers(min_value=1, max_value=10)), min_size=1),
    arrays(np.float64, st.integers(min_value=1, max_value=10)),
    arrays(np.int64, st.integers(min_value=1, max_value=10)),
)
notch_strategy = st.one_of(st.none(), st.booleans())
whis_strategy = st.one_of(
    st.none(),
    st.floats(),
    st.tuples(st.floats(), st.floats()),
)
bootstrap_strategy = st.one_of(st.none(), st.integers(min_value=0))
usermedians_strategy = st.one_of(
    st.none(),
    st.lists(st.one_of(st.floats(), st.none()), min_size=1),
    arrays(np.float64, st.integers(min_value=1, max_value=10)),
)
conf_intervals_strategy = st.one_of(
    st.none(),
    st.lists(
        st.tuples(
            st.one_of(st.floats(), st.none()),
            st.one_of(st.floats(), st.none()),
        ),
        min_size=1,
    ),
    arrays(np.float64, st.integers(min_value=1, max_value=10)),
)
tick_labels_strategy = st.one_of(st.none(), st.lists(st.text(), min_size=1))


@given(
    x=x_strategy,
    notch=notch_strategy,
    whis=whis_strategy,
    bootstrap=bootstrap_strategy,
    usermedians=usermedians_strategy,
    conf_intervals=conf_intervals_strategy,
    tick_labels=tick_labels_strategy,
)
@settings(deadline=500)
def test_box_properties(
    x: Any,
    notch: Any,
    whis: Any,
    bootstrap: Any,
    usermedians: Any,
    conf_intervals: Any,
    tick_labels: Any,
) -> None:
    serializer = MatplotlibSerializer()
    _, serializer_ax = serializer.subplots()
    _fig, ax = plt.subplots()
    try:
        ax.boxplot(
            x=x,
            notch=notch,
            whis=whis,
            bootstrap=bootstrap,
            usermedians=usermedians,
            conf_intervals=conf_intervals,
            tick_labels=tick_labels,
        )
    except Exception as _e:
        pass
    else:
        serializer_ax.boxplot(
            x=x,
            notch=notch,
            whis=whis,
            bootstrap=bootstrap,
            usermedians=usermedians,
            conf_intervals=conf_intervals,
            tick_labels=tick_labels,
        )
        assert serializer.to_json() != "{}", "Serialized JSON is empty check input"
    finally:
        plt.close(_)
        plt.close(_fig)
