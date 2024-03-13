import logging
from typing import (
    Any,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
)

from matplotlib.figure import Figure as MplFigure
from matplotlib.axes import Axes as MplAxes

from mpl_toolkits.mplot3d.axes3d import Axes3D as MplAxes3D
from mpl_toolkits.mplot3d.art3d import Path3DCollection

import matplotlib.pyplot
from matplotlib.lines import Line2D
from matplotlib.container import BarContainer
from matplotlib.collections import PathCollection

import matplotlib.colors as mcolors
import matplotlib.cm as cm

import numpy as np

from plot_serializer.serializer import Serializer
from plot_serializer.proxy import Proxy
from plot_serializer.model import (
    Axis,
    Bar2D,
    BarTrace2D,
    Box,
    BoxTrace2D,
    Figure,
    LineTrace2D,
    PiePlot,
    Plot,
    Plot2D,
    Plot3D,
    Point2D,
    Point3D,
    Scale,
    ScatterTrace2D,
    ScatterTrace3D,
    Slice,
)


__all__ = ["MatplotlibSerializer"]

PLOTTING_METHODS = [
    "plot",
    "errorbar",
    "scatter",
    "step",
    "loglog",
    "semilogx",
    "semilogy",
    "bar",
    "barh",
    "stem",
    "eventplot",
    "pie",
    "stackplot",
    "broken_barh",
    "fill",
    "acorr",
    "angle_spectrum",
    "cohere",
    "csd",
    "magnitude_spectrum",
    "phase_spectrum",
    "psd",
    "specgram",
    "xcorr",
    "ecdf",
    "boxplot",
    "violinplot",
    "bxp",
    "violin",
    "hexbin",
    "hist",
    "hist2d",
    "contour",
    "contourf",
    "imshow",
    "matshow",
    "pcolor",
    "pcolorfast",
    "pcolormesh",
    "spy",
    "tripcolor",
    "triplot",
    "tricontour" "tricontourf",
]


def _convert_matplotlib_scale(scale: str) -> Scale:
    if scale == "linear":
        return "linear"
    elif scale == "log":
        return "logarithmic"
    else:
        raise NotImplementedError(
            "This type of scaling is not supported in PlotSerializer yet!"
        )


def _convert_matplotlib_color(color: str) -> str:
    # TODO: We leave the color as-is for now, but we should probably
    #  build some kind of conversion later, so plotserializer has a
    #  predictable color format between different plotting libraries.
    return color


class _AxesProxy(Proxy[MplAxes]):
    def __init__(
        self, delegate: MplAxes, figure: Figure, serializer: Serializer
    ) -> None:
        super().__init__(delegate)
        self._figure = figure
        self._serializer = serializer
        self._plot: Optional[Plot] = None

    # FIXME: size_list cannot only be floats, but also different other types of data
    def pie(self, size_list: Iterable[float], **kwargs: Any) -> Any:
        result = self.delegate.pie(size_list, **kwargs)

        try:
            if self._plot is not None:
                raise NotImplementedError(
                    "PlotSerializer does not yet support adding multiple plots per axes!"
                )

            slices: List[Slice] = []

            color_list = kwargs.get("colors") or []
            explode_list = kwargs.get("explode") or []
            label_list = kwargs.get("labels") or []
            radius_list = kwargs.get("radius") or []

            for i, size in enumerate(size_list):
                color = color_list[i] if i < len(color_list) else None
                explode = explode_list[i] if i < len(explode_list) else None
                label = label_list[i] if i < len(label_list) else None
                radius = radius_list[i] if i < len(radius_list) else None

                slices.append(
                    Slice(
                        size=size,
                        radius=radius,
                        offset=explode,
                        name=label,
                        color=_convert_matplotlib_color(color),
                    )
                )

            pie_plot = PiePlot(type="pie", slices=slices)
            self._plot = pie_plot
        except Exception as e:
            logging.warning(
                "An unexpected error occurred in PlotSerializer when trying to read plot data! "
                + "Parts of the plot will not be serialized!",
                exc_info=e,
            )

        return result

    # FIXME: name_list and height_list cannot only be floats, but also different other types of data
    def bar(
        self, label_list: Iterable[str], height_list: Iterable[float], **kwargs: Any
    ) -> BarContainer:
        result = self.delegate.bar(label_list, height_list, **kwargs)

        try:
            bars: List[Bar2D] = []

            color_list = kwargs.get("color") or []

            for i, label in enumerate(label_list):
                height = height_list[i]
                color = color_list[i] if i < len(color_list) else None

                bars.append(
                    Bar2D(y=height, label=label, color=_convert_matplotlib_color(color))
                )

            trace = BarTrace2D(type="bar", datapoints=bars)

            if self._plot is not None:
                if not isinstance(self._plot, Plot2D):
                    raise NotImplementedError(
                        "PlotSerializer does not yet support mixing 2d plots with other plots!"
                    )

                self._plot.traces.append(trace)
            else:
                self._plot = Plot2D(
                    type="2d", x_axis=Axis(), y_axis=Axis(), traces=[trace]
                )
        except Exception as e:
            logging.warning(
                "An unexpected error occurred in PlotSerializer when trying to read plot data! "
                + "Parts of the plot will not be serialized!",
                exc_info=e,
            )

        return result

    def plot(self, *args: Any, **kwargs: Any) -> list[Line2D]:
        mpl_lines = self.delegate.plot(*args, **kwargs)

        try:
            traces: List[LineTrace2D] = []

            for mpl_line in mpl_lines:
                xdata = mpl_line.get_xdata()
                ydata = mpl_line.get_ydata()

                points: List[Point2D] = []

                for x, y in zip(xdata, ydata):
                    points.append(Point2D(x=x, y=y))

                label = mpl_line.get_label()
                color = _convert_matplotlib_color(mpl_line.get_color())
                thickness = mpl_line.get_linewidth()
                linestyle = mpl_line.get_linestyle()

                traces.append(
                    LineTrace2D(
                        type="line",
                        line_color=color,
                        line_thickness=thickness,
                        line_style=linestyle,
                        label=label,
                        datapoints=points,
                    )
                )

            if self._plot is not None:
                if not isinstance(self._plot, Plot2D):
                    raise NotImplementedError(
                        "PlotSerializer does not yet support mixing 2d plots with other plots!"
                    )
                self._plot.traces += traces
            else:
                self._plot = Plot2D(
                    type="2d", x_axis=Axis(), y_axis=Axis(), traces=traces
                )
        except Exception as e:
            logging.warning(
                "An unexpected error occurred in PlotSerializer when trying to read plot data! "
                + "Parts of the plot will not be serialized!",
                exc_info=e,
            )

        return mpl_lines

    def scatter(
        self,
        x_values,
        y_values,
        *args: Any,
        **kwargs: Any,
    ) -> PathCollection:
        path = self.delegate.scatter(x_values, y_values, *args, **kwargs)

        try:
            color_list = kwargs.get("c") or []
            sizes_list = kwargs.get("s") or []
            enable_colors: bool = True
            enable_sizes: bool = True

            if not color_list:
                enable_colors = False
            if not sizes_list:
                enable_sizes = False

            trace: List[ScatterTrace2D] = []
            label = str(path.get_label())
            datapoints: List[Point2D] = []

            verteces = path.get_offsets().tolist()
            colors = path.get_facecolor().tolist()
            sizes = path.get_sizes().tolist()

            # extend lists when only containing one element
            if not (len(colors) - 1):
                colors = [colors[0] for i in range(len(verteces))]
            if not (len(sizes) - 1):
                sizes = [sizes[0] for i in range(len(verteces))]

            if not (len(colors) == len(verteces) == len(sizes)):
                raise NotImplementedError(
                    "A different amount of sizes/colors and points is not implemented by matplotlib or plotserializer"
                )

            for index, vertex in enumerate(verteces):
                color = (
                    mcolors.to_hex(colors[index], keep_alpha=True)
                    if enable_colors
                    else None
                )
                size = sizes[index] if enable_sizes else None

                datapoints.append(
                    Point2D(
                        x=vertex[0],
                        y=vertex[1],
                        color=color,
                        size=size,
                    )
                )

            trace.append(
                ScatterTrace2D(type="scatter", label=label, datapoints=datapoints)
            )

            if self._plot is not None:
                if not isinstance(self._plot, Plot2D):
                    raise NotImplementedError(
                        "PlotSerializer does not yet support mixing 2d plots with other plots!"
                    )
                self._plot.traces += trace
            else:
                self._plot = Plot2D(
                    type="2d", x_axis=Axis(), y_axis=Axis(), traces=trace
                )
        except Exception as e:
            logging.warning(
                "An unexpected error occurred in PlotSerializer when trying to read plot data! "
                + "Parts of the plot will not be serialized!",
                exc_info=e,
            )

        return path

    def boxplot(self, x, *args, **kwargs) -> dict:
        dic = self.delegate.boxplot(x, *args, **kwargs)
        try:
            notch = kwargs.get("notch") or None
            whis = kwargs.get("whis") or None
            bootstrap = kwargs.get("bootstrap")
            usermedians = kwargs.get("usermedians") or []
            conf_intervals = kwargs.get("conf_intervals") or []
            labels = kwargs.get("labels") or []

            trace: List[ScatterTrace2D] = []
            boxes: List[Box] = []

            if not (
                self._are_lists_same_length(x, labels, usermedians, conf_intervals)
            ):
                raise ValueError("lengthes of lists do not match")
            if not (
                isinstance(x, list) and all(isinstance(sublist, list) for sublist in x)
            ):
                x = [x]
            for index, dataset in enumerate(x):
                label = labels[index] if labels else None
                umedian = usermedians[index] if usermedians else None
                cintervals = conf_intervals[index] if conf_intervals else None
                boxes.append(
                    Box(
                        data=dataset,
                        label=label,
                        usermedian=umedian,
                        conf_interval=cintervals,
                    )
                )
            trace.append(
                BoxTrace2D(
                    type="box", boxes=boxes, notch=notch, whis=whis, bootstrap=bootstrap
                )
            )
            if self._plot is not None:
                if not isinstance(self._plot, Plot2D):
                    raise NotImplementedError(
                        "PlotSerializer does not yet support mixing 2d plots with other plots!"
                    )
                self._plot.traces += trace
            else:
                self._plot = Plot2D(
                    type="2d", x_axis=Axis(), y_axis=Axis(), traces=trace
                )
        except Exception as e:
            logging.warning(
                "An unexpected error occurred in PlotSerializer when trying to read plot data! "
                + "Parts of the plot will not be serialized!",
                exc_info=e,
            )

        return dic

    def _are_lists_same_length(self, *lists) -> bool:
        non_empty_lists = [lst for lst in lists if lst]
        if not non_empty_lists:
            return True
        length = len(non_empty_lists[0])
        return all(len(lst) == length for lst in non_empty_lists)

    def _on_collect(self) -> None:
        if self._plot is None:
            return

        self._plot.title = self.delegate.get_title()

        if isinstance(self._plot, Plot2D):
            xlabel = self.delegate.get_xlabel()
            xscale = _convert_matplotlib_scale(self.delegate.get_xscale())

            self._plot.x_axis.label = xlabel
            self._plot.x_axis.scale = xscale

            ylabel = self.delegate.get_ylabel()
            yscale = _convert_matplotlib_scale(self.delegate.get_yscale())

            self._plot.y_axis.label = ylabel
            self._plot.y_axis.scale = yscale

        self._figure.plots.append(self._plot)

    def __getattr__(self, __name: str) -> Any:
        if __name in PLOTTING_METHODS:
            logging.warning(
                f"{__name} is not supported by PlotSerializer! Data will be lost!"
            )

        return super().__getattr__(__name)


class _AxesProxy3D(Proxy[MplAxes3D]):
    def __init__(
        self, delegate: MplAxes3D, figure: Figure, serializer: Serializer
    ) -> None:
        super().__init__(delegate)
        self._figure = figure
        self._serializer = serializer
        self._plot: Optional[Plot] = None

    def scatter(
        self,
        x_values: Iterable[float],
        y_values: Iterable[float],
        z_values: Iterable[float],
        *args: Any,
        **kwargs: Any,
    ) -> Path3DCollection:
        path = self.delegate.scatter(x_values, y_values, z_values, *args, **kwargs)

        try:
            color_list = kwargs.get("c") or []
            sizes_list = kwargs.get("s") or []
            cmap = kwargs.get("cmap") or "viridis"
            norm = kwargs.get("norm") or "linear"
            enable_colors: bool = True
            enable_sizes: bool = True

            if not x_values or not y_values or not z_values:
                raise ValueError("one of your x,y,z data is missing")
            if isinstance(x_values, float) or isinstance(x_values, int):
                x_values = [x_values]
            if isinstance(y_values, float) or isinstance(y_values, int):
                y_values = [y_values]
            if isinstance(z_values, float) or isinstance(z_values, int):
                z_values = [z_values]
            if not sizes_list:
                enable_sizes = False
            if not color_list:
                enable_colors = False
            if isinstance(sizes_list, float) or isinstance(sizes_list, int):
                sizes_list = [sizes_list]

            if not (len(x_values) == len(y_values) == len(z_values)):
                raise ValueError(
                    "the x,y,z arrays do not contain the same amount of elements"
                )
            trace: List[ScatterTrace3D] = []
            datapoints: List[Point3D] = []

            sizes: List[float] = []
            if enable_sizes:
                if not (len(x_values) == len(sizes_list)):
                    if not (len(sizes_list) - 1):
                        sizes = [sizes_list[0] for i in range(len(x_values))]
                    else:
                        raise ValueError(
                            "sizes list contains more than one element while not being as long as the x_values array"
                        )
                else:
                    sizes = sizes_list
            else:
                sizes = [None] * len(x_values)

            colors: List[str] = []
            if enable_colors:
                scalar_mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
                colors = self._get_colors_scatter(
                    color_list, scalar_mappable, len(x_values)
                )
            else:
                colors = [None] * len(x_values)

            for i in range(len(x_values)):
                c = colors[i]
                s = sizes[i]
                datapoints.append(
                    Point3D(
                        x=x_values[i], y=y_values[i], z=z_values[i], color=c, size=s
                    )
                )

            label = str(path.get_label())

            trace.append(
                ScatterTrace3D(type="scatter3D", label=label, datapoints=datapoints)
            )

            if self._plot is not None:
                self._plot.traces += trace
            else:
                self._plot = Plot3D(
                    type="3d", x_axis=Axis(), y_axis=Axis(), z_axis=Axis(), traces=trace
                )
        except Exception as e:
            logging.warning(
                "An unexpected error occurred in PlotSerializer when trying to read plot data! "
                + "Parts of the plot will not be serialized!",
                exc_info=e,
            )

        return path

    def _get_colors_scatter(
        self, color_list: Any, scalar_mappable: cm.ScalarMappable, length: int
    ) -> List[str]:
        colors: List[str] = []
        color_type = type(color_list)

        if color_type is str:
            colors.append(mcolors.to_hex(color_list, keep_alpha=True))
        elif color_type is list and all(isinstance(item, str) for item in color_list):
            colors.append(color_list)
            colors = [mcolors.to_hex(c, keep_alpha=True) for c in color_list]
        elif color_type is list and (
            all(isinstance(item, tuple) and len(item) == 3 for item in color_list)
            or all(isinstance(item, tuple) and len(item) == 4 for item in color_list)
        ):
            hex_values = [mcolors.to_hex(c, keep_alpha=True) for c in color_list]
            colors.extend(hex_values)
        elif (color_type is list or isinstance(color_list, np.ndarray)) and all(
            isinstance(item, (int, float)) for item in color_list
        ):
            rgba_tuples = scalar_mappable.to_rgba(color_list)
            hex_values = [
                mcolors.to_hex(rgba_value, keep_alpha=True)
                for rgba_value in rgba_tuples
            ]
            colors.extend(hex_values)
        else:
            raise NotImplementedError(
                "Your color is not supported by PlotSerializer, see Documentation for more detail"
            )
        if not (len(colors) == length):
            if not (len(colors) - 1):
                colors = [colors[0] for i in range(length)]
            else:
                raise ValueError(
                    "the lenth of your color array does not match the length of given data"
                )
        return colors

    def _on_collect(self) -> None:
        if self._plot is None:
            return

        self._plot.title = self.delegate.get_title()

        if isinstance(self._plot, Plot3D):
            xlabel = self.delegate.get_xlabel()
            xscale = _convert_matplotlib_scale(self.delegate.get_xscale())

            self._plot.x_axis.label = xlabel
            self._plot.x_axis.scale = xscale

            ylabel = self.delegate.get_ylabel()
            yscale = _convert_matplotlib_scale(self.delegate.get_yscale())

            self._plot.y_axis.label = ylabel
            self._plot.y_axis.scale = yscale

            zlabel = self.delegate.get_zlabel()
            zscale = _convert_matplotlib_scale(self.delegate.get_zscale())

            self._plot.z_axis.label = zlabel
            self._plot.z_axis.scale = zscale

        self._figure.plots.append(self._plot)

    def __getattr__(self, __name: str) -> Any:
        if __name in PLOTTING_METHODS:
            logging.warning(
                f"{__name} is not supported by PlotSerializer! Data will be lost!"
            )

        return super().__getattr__(__name)


class MatplotlibSerializer(Serializer):
    """
    Serializer specific to matplotlib. Most of the methods on this object mirror the
    matplotlib.pyplot api from matplotlib.

    Args:
        Serializer (_type_): Parent class
    """

    def _create_axes_proxy(
        self, mpl_axes: Union[MplAxes3D, MplAxes]
    ) -> Union[_AxesProxy, _AxesProxy3D]:
        proxy: Any
        if isinstance(mpl_axes, MplAxes3D):
            proxy = _AxesProxy3D(mpl_axes, self._figure, self)
            self._add_collect_action(lambda: proxy._on_collect())
        elif isinstance(mpl_axes, MplAxes):
            proxy = _AxesProxy(mpl_axes, self._figure, self)
            self._add_collect_action(lambda: proxy._on_collect())
        else:
            raise NotImplementedError(
                "The matplotlib adapter only supports plots on 3D and normal axes"
            )
        return proxy

    def subplots(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Tuple[MplFigure, Union[MplAxes, MplAxes3D, Any]]:
        figure, axes = matplotlib.pyplot.subplots(*args, **kwargs)

        new_axes: Any

        if isinstance(axes, np.ndarray):
            new_axes = np.array(list(map(self._create_axes_proxy, axes)))
        else:
            new_axes = self._create_axes_proxy(axes)

        return (figure, new_axes)
