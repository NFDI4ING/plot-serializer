from typing import Any

import numpy as np
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays
from matplotlib import pyplot as plt

from plot_serializer.matplotlib.serializer import MatplotlibSerializer


@st.composite
def matrix_triplet_strategy(draw, min_dim=1, max_dim=10, min_value=0, max_value=100):  # type: ignore
    rows = draw(st.integers(min_value=min_dim, max_value=max_dim))
    cols = draw(st.integers(min_value=min_dim, max_value=max_dim))

    matrix_strategy = st.one_of(
        st.lists(
            st.lists(st.integers(min_value=min_value, max_value=max_value), min_size=cols, max_size=cols),
            min_size=rows,
            max_size=rows,
        ),
        arrays(dtype=np.int64, shape=(rows, cols)),
    )

    matrix1 = draw(matrix_strategy)
    matrix2 = draw(matrix_strategy)
    matrix3 = draw(matrix_strategy)

    return matrix1, matrix2, matrix3


@given(matrix_triplet_strategy())
def test_surface_properties(
    matrix_triplet: Any,
) -> None:
    x, y, z = matrix_triplet
    serializer = MatplotlibSerializer()
    _, serializer_ax = serializer.subplots(subplot_kw={"projection": "3d"})
    _fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    try:
        ax.plot_surface(x, y, z)  # type: ignore
    except Exception as _e:
        pass
    else:
        serializer_ax.plot_surface(x, y, z)
        assert serializer.to_json() != "{}", "Serialized JSON is empty check input"
    finally:
        plt.close(_)
        plt.close(_fig)
