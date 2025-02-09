from typing import (
    Any,
    Tuple,
    Union,
)

import matplotlib.pyplot
import numpy as np
from matplotlib.axes import Axes as MplAxes
from matplotlib.figure import Figure as MplFigure
from mpl_toolkits.mplot3d.axes3d import Axes3D as MplAxes3D

from plot_serializer.matplotlib.axesproxy import AxesProxy, AxesProxy3D
from plot_serializer.serializer import Serializer


class MatplotlibSerializer(Serializer):
    """
    Serializer specific to matplotlib. Most of the methods on this object mirror the
    matplotlib.pyplot api from matplotlib.

    Args:
        Serializer (_type_): Parent class
    """

    def _create_axes_proxy(self, mpl_axes: Union[MplAxes3D, MplAxes]) -> Union[AxesProxy, AxesProxy3D]:
        proxy: Any
        if isinstance(mpl_axes, MplAxes3D):
            proxy = AxesProxy3D(mpl_axes, self._figure, self)
            self._add_collect_action(lambda: proxy._on_collect())
        elif isinstance(mpl_axes, MplAxes):
            proxy = AxesProxy(mpl_axes, self._figure, self)
            self._add_collect_action(lambda: proxy._on_collect())
        else:
            raise NotImplementedError("The matplotlib adapter only supports plots on 3D and normal axes")
        return proxy

    def subplots(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Tuple[MplFigure, Union[MplAxes, MplAxes3D, Any]]:
        figure, axes = matplotlib.pyplot.subplots(*args, **kwargs)

        new_axes: Any

        if isinstance(axes, np.ndarray):
            if isinstance(axes[0], np.ndarray):
                new_axes = np.array([list(map(self._create_axes_proxy, row)) for row in axes])
            else:
                new_axes = np.array(list(map(self._create_axes_proxy, axes)))
        else:
            new_axes = self._create_axes_proxy(axes)

        return (figure, new_axes)

    def show(self, *args: Any, **kwargs: Any) -> None:
        matplotlib.pyplot.show(*args, **kwargs)
