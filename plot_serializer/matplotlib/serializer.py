import itertools
import logging
from collections.abc import Sequence
from typing import (
    Any,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
)

import matplotlib.cbook as cbook
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.pyplot
import numpy as np
from matplotlib.axes import Axes as MplAxes
from matplotlib.cbook import _reshape_2D
from matplotlib.collections import PathCollection
from matplotlib.container import BarContainer, ErrorbarContainer
from matplotlib.figure import Figure as MplFigure
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon
from mpl_toolkits.mplot3d.art3d import Path3DCollection, Poly3DCollection
from mpl_toolkits.mplot3d.axes3d import Axes3D as MplAxes3D
from numpy import ndarray, reshape
from numpy.typing import ArrayLike

from plot_serializer.model import (
    Axis,
    Bar2D,
    BarTrace2D,
    Box,
    BoxTrace2D,
    ErrorBar2DTrace,
    ErrorPoint2D,
    Figure,
    HistDataset,
    HistogramTrace,
    LineTrace2D,
    LineTrace3D,
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
    SurfaceTrace3D,
)
from plot_serializer.proxy import Proxy
from plot_serializer.serializer import Serializer

__all__ = ["MatplotlibSerializer"]

PLOTTING_METHODS = [
    "plot",
    "errorbar",
    "hist",
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
        raise NotImplementedError("This type of scaling is not supported in PlotSerializer yet!")


def is_array_like(x):
    try:
        np.array(x)
        return True
    except Exception:
        return False


def _convert_matplotlib_color(
    self, color_list: Any, length: int, cmap: Any, norm: Any
) -> Tuple[List[str] | None, bool]:
    cmap_used = False
    if not color_list:
        return ([None], cmap_used)
    colors: List[str] = []
    color_type = type(color_list)

    if color_type is str:
        colors.append(mcolors.to_hex(color_list, keep_alpha=True))
    elif color_type is int or color_type is float:
        scalar_mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
        rgba_tuple = scalar_mappable.to_rgba(color_list)
        hex_value = mcolors.to_hex(rgba_tuple, keep_alpha=True)
        colors.append(hex_value)
        cmap_used = True
    elif color_type is tuple and (len(color_list) == 3 or len(color_list) == 4):
        hex_value = mcolors.to_hex(color_list, keep_alpha=True)
        colors.append(hex_value)
    elif (color_type is list or isinstance(color_list, np.ndarray)) and all(
        isinstance(item, (int, float)) for item in color_list
    ):
        scalar_mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
        rgba_tuples = scalar_mappable.to_rgba(color_list)
        hex_values = [mcolors.to_hex(rgba_value, keep_alpha=True) for rgba_value in rgba_tuples]
        colors.extend(hex_values)
        cmap_used = True
    elif color_type is list or isinstance(color_list, np.ndarray):
        for item in color_list:
            if (isinstance(item, str)) or (isinstance(item, tuple) and (len(item) == 3 or len(item) == 4)):
                colors.append(mcolors.to_hex(item, keep_alpha=True))
            elif item is None:
                colors.append(None)
    else:
        raise NotImplementedError("Your color is not supported by PlotSerializer, see Documentation for more detail")
    if not (len(colors) == length):
        if not (len(colors) - 1):
            colors = [colors[0] for i in range(length)]
        else:
            raise ValueError("the lenth of your color array does not match the length of given data")
    return (colors, cmap_used)


class _AxesProxy(Proxy[MplAxes]):
    def __init__(self, delegate: MplAxes, figure: Figure, serializer: Serializer) -> None:
        super().__init__(delegate)
        self._figure = figure
        self._serializer = serializer
        self._plot: Optional[Plot] = None

    def pie(self, size_list, **kwargs: Any) -> Any:
        try:
            result = self.delegate.pie(size_list, **kwargs)
        except Exception as e:
            logging.warning(
                "An Error got thrown from Matplotlib's independent from PlotSerializer!",
                exc_info=e,
            )

        try:
            if self._plot is not None:
                raise NotImplementedError("PlotSerializer does not yet support adding multiple plots per axes!")

            slices: List[Slice] = []

            explode_list = kwargs.get("explode") or []
            label_list = kwargs.get("labels") or []
            radius = kwargs.get("radius") or None

            color_list = kwargs.get("colors") or []
            color_list = _convert_matplotlib_color(self, color_list, len(size_list), cmap="viridis", norm="linear")[0]

            size_list = np.asarray(size_list, np.float32)
            if not explode_list:
                explode_list = itertools.repeat(None)
            if not label_list:
                label_list = itertools.repeat(None)

            for size, label, explode, color in zip(size_list, label_list, explode_list, color_list):
                slices.append(
                    Slice(
                        size=size,
                        radius=radius,
                        offset=explode,
                        name=label,
                        color=color,
                    )
                )
            pie_plot = PiePlot(type="pie", radius=radius, slices=slices)
            self._plot = pie_plot
        except Exception as e:
            logging.warning(
                "An unexpected error occurred in PlotSerializer when trying to read plot data! "
                + "Parts of the plot will not be serialized!",
                exc_info=e,
            )

        return result

    def bar(
        self,
        x,
        height_list,
        **kwargs: Any,
    ) -> BarContainer:
        result = self.delegate.bar(x, height_list, **kwargs)

        try:
            bars: List[Bar2D] = []

            color_list = kwargs.get("color") or []
            color_list = _convert_matplotlib_color(self, color_list, len(x), cmap="viridis", norm="linear")[0]

            if not x:
                x = 0
            if isinstance(x, float):
                x = [x]
            else:
                x = np.asarray(x)
            if not height_list:
                pass

            if isinstance(height_list, float):
                height_list = [height_list]
            else:
                height_list = np.asarray(height_list)

            for label, height, color in zip(x, height_list, color_list):
                bars.append(Bar2D(y=height, label=label, color=color))

            trace = BarTrace2D(type="bar", datapoints=bars)

            if self._plot is not None:
                if not isinstance(self._plot, Plot2D):
                    raise NotImplementedError("PlotSerializer does not yet support mixing 2d plots with other plots!")

                self._plot.traces.append(trace)
            else:
                self._plot = Plot2D(type="2d", x_axis=Axis(), y_axis=Axis(), traces=[trace])
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
                color_list = kwargs.get("color") or []

                xdata = mpl_line.get_xdata()
                ydata = mpl_line.get_ydata()

                points: List[Point2D] = []

                for x, y in zip(xdata, ydata):
                    points.append(Point2D(x=x, y=y))

                label = mpl_line.get_label()
                color_list = _convert_matplotlib_color(self, color_list, len(xdata), cmap="viridis", norm="linear")[0]
                thickness = mpl_line.get_linewidth()
                linestyle = mpl_line.get_linestyle()
                marker = mpl_line.get_marker()

                traces.append(
                    LineTrace2D(
                        type="line",
                        line_color=color_list[0],
                        line_thickness=thickness,
                        line_style=linestyle,
                        label=label,
                        datapoints=points,
                        marker=marker,
                    )
                )

            if self._plot is not None:
                if not isinstance(self._plot, Plot2D):
                    raise NotImplementedError("PlotSerializer does not yet support mixing 2d plots with other plots!")
                self._plot.traces += traces
            else:
                self._plot = Plot2D(type="2d", x_axis=Axis(), y_axis=Axis(), traces=traces)
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
            marker = kwargs.get("marker") or "o"
            color_list = kwargs.get("c") or []
            sizes_list = kwargs.get("s") or []
            cmap = kwargs.get("cmap") or "viridis"
            norm = kwargs.get("norm") or "linear"

            (color_list, cmap_used) = _convert_matplotlib_color(self, color_list, len(x_values), cmap, norm)

            if sizes_list:
                sizes_list = path.get_sizes()
            else:
                sizes_list = itertools.repeat(None)

            label = str(path.get_label())
            datapoints: List[Point2D] = []

            verteces = path.get_offsets().tolist()

            for vertex, color, size in zip(verteces, color_list, sizes_list):
                datapoints.append(
                    Point2D(
                        x=vertex[0],
                        y=vertex[1],
                        color=color,
                        size=size,
                    )
                )
            if not cmap_used:
                cmap = None
                norm = None
            trace: List[ScatterTrace2D] = []
            trace.append(
                ScatterTrace2D(type="scatter", cmap=cmap, norm=norm, label=label, datapoints=datapoints, marker=marker)
            )

            if self._plot is not None:
                if not isinstance(self._plot, Plot2D):
                    raise NotImplementedError("PlotSerializer does not yet support mixing 2d plots with other plots!")
                self._plot.traces += trace
            else:
                self._plot = Plot2D(type="2d", x_axis=Axis(), y_axis=Axis(), traces=trace)
        except Exception as e:
            logging.warning(
                "An unexpected error occurred in PlotSerializer when trying to read plot data! "
                + "Parts of the plot will not be serialized!",
                exc_info=e,
            )

        return path

    def boxplot(self, x, *args, **kwargs) -> dict:
        try:
            dic = self.delegate.boxplot(x, *args, **kwargs)
        except Exception as e:
            add_msg = " - This error was thrown by Matplotlib and is independent of PlotSerializer!"
            e.args = (e.args[0] + add_msg,) + e.args[1:] if e.args else (add_msg,)
            raise

        try:
            notch = kwargs.get("notch") or None
            whis = kwargs.get("whis") or None
            bootstrap = kwargs.get("bootstrap")
            usermedians = kwargs.get("usermedians") or []
            conf_intervals = kwargs.get("conf_intervals") or []
            labels = kwargs.get("tick_labels") or []

            trace: List[BoxTrace2D] = []
            boxes: List[Box] = []
            x = _reshape_2D(x, "x")

            if not labels:
                labels = itertools.repeat(None)
            if not usermedians:
                usermedians = itertools.repeat(None)
            if not conf_intervals:
                conf_intervals = itertools.repeat(None)

            for dataset, label, umedian, cintervals in zip(x, labels, usermedians, conf_intervals):
                boxes.append(
                    Box(
                        data=dataset,
                        label=label,
                        usermedian=umedian,
                        conf_interval=cintervals,
                    )
                )
            trace.append(BoxTrace2D(type="box", boxes=boxes, notch=notch, whis=whis, bootstrap=bootstrap))
            if self._plot is not None:
                if not isinstance(self._plot, Plot2D):
                    raise NotImplementedError("PlotSerializer does not yet support mixing 2d plots with other plots!")
                self._plot.traces += trace
            else:
                self._plot = Plot2D(type="2d", x_axis=Axis(), y_axis=Axis(), traces=trace)
        except Exception as e:
            logging.warning(
                "An unexpected error occurred in PlotSerializer when trying to read plot data! "
                + "Parts of the plot will not be serialized!",
                exc_info=e,
            )

        return dic

    def errorbar(self, x, y, *args, **kwargs) -> ErrorbarContainer:
        def _upcast_err(err):
            """
            Imported local function from Matplotlib errorbar function.
            """

            if np.iterable(err) and len(err) > 0 and isinstance(cbook._safe_first_finite(err), np.ndarray):
                atype = type(cbook._safe_first_finite(err))
                if atype is np.ndarray:
                    return np.asarray(err, dtype=object)

                return atype(err)

            return np.asarray(err, dtype=object)

        try:
            container = self.delegate.errorbar(x, y, *args, **kwargs)
        except Exception as e:
            add_msg = " - This error was thrown by Matplotlib and is independent of PlotSerializer!"
            e.args = (e.args[0] + add_msg,) + e.args[1:] if e.args else (add_msg,)
            raise

        try:
            xerr = kwargs.get("xerr") or None
            yerr = kwargs.get("yerr") or None
            marker = kwargs.get("marker") or None
            color = kwargs.get("color") or None
            ecolor = kwargs.get("ecolor") or None
            label = kwargs.get("label") or None

            if not isinstance(x, np.ndarray):
                x = np.asarray(x, dtype=object)
            if not isinstance(y, np.ndarray):
                y = np.asarray(y, dtype=object)
            x, y = np.atleast_1d(x, y)

            if xerr is not None and not isinstance(xerr, np.ndarray):
                xerr = _upcast_err(xerr)
                np.broadcast_to(xerr, (2, len(x)))
            if yerr is not None and not isinstance(yerr, np.ndarray):
                yerr = _upcast_err(yerr)
                np.broadcast_to(xerr, (2, len(y)))
            if xerr is None:
                xerr = itertools.repeat(None)
            if yerr is None:
                yerr = itertools.repeat(None)

            errorpoints: List[ErrorPoint2D] = []

            for xi, yi, x_error, y_error in zip(x, y, xerr, yerr):
                errorpoints.append(
                    ErrorPoint2D(
                        x=xi,
                        y=yi,
                        x_error=x_error,
                        y_error=y_error,
                    )
                )
            color = mcolors.to_hex(color) if color else None
            ecolor = mcolors.to_hex(ecolor) if ecolor else None
            trace = ErrorBar2DTrace(
                type="errorbar2d",
                label=label,
                marker=marker,
                datapoints=errorpoints,
                color=color,
                ecolor=ecolor,
            )
            if self._plot is not None:
                if not isinstance(self._plot, Plot2D):
                    raise NotImplementedError("PlotSerializer does not yet support mixing 2d plots with other plots!")

                self._plot.traces.append(trace)
            else:
                self._plot = Plot2D(type="2d", x_axis=Axis(), y_axis=Axis(), traces=[trace])

        except Exception as e:
            logging.warning(
                "An unexpected error occurred in PlotSerializer when trying to read plot data! "
                + "Parts of the plot will not be serialized!",
                exc_info=e,
            )
        return container

    def hist(
        self, x, *args, **kwargs
    ) -> tuple[
        ndarray | list[ndarray],
        ndarray,
        BarContainer | Polygon | list[BarContainer | Polygon],
    ]:
        ret = self.delegate.hist(x, *args, **kwargs)
        try:
            bins = kwargs.get("bins") or 10
            density = kwargs.get("density") or False
            cumulative = kwargs.get("cumulative") or False
            label_list = kwargs.get("label") or None
            color_list = kwargs.get("color") or None

            color_list = _convert_matplotlib_color(self, color_list, len(x), "viridis", "linear")[0]

            if not label_list:
                label_list = itertools.repeat(None)
            else:
                label_list = np.atleast_1d(np.asarray(label_list, str))

            if np.isscalar(x):
                x = [x]
            x = _reshape_2D(x, "x")

            datasets: List[HistDataset] = []

            for element, label, color in zip(x, label_list, color_list):
                datasets.append(HistDataset(data=element, color=color, label=label))

            trace = HistogramTrace(
                type="histogram",
                datasets=datasets,
                bins=bins,
                density=density,
                cumulative=cumulative,
            )
            if self._plot is not None:
                if not isinstance(self._plot, Plot2D):
                    raise NotImplementedError("PlotSerializer does not yet support mixing 2d plots with other plots!")

                self._plot.traces.append(trace)
            else:
                self._plot = Plot2D(type="2d", x_axis=Axis(), y_axis=Axis(), traces=[trace])

        except Exception as e:
            logging.warning(
                "An unexpected error occurred in PlotSerializer when trying to read plot data! "
                + "Parts of the plot will not be serialized!",
                exc_info=e,
            )
        return ret

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
            for spine in self.delegate.spines:
                if not self.delegate.spines[spine].get_visible():
                    if not self._plot.spines_removed:
                        self._plot.spines_removed = [spine]
                    else:
                        self._plot.spines_removed.append(spine)
            xlabel = self.delegate.get_xlabel()
            xscale = _convert_matplotlib_scale(self.delegate.get_xscale())

            self._plot.x_axis.label = xlabel
            self._plot.x_axis.scale = xscale
            if not self.delegate.get_autoscalex_on():
                self._plot.x_axis.limit = self.delegate.get_xlim()

            ylabel = self.delegate.get_ylabel()
            yscale = _convert_matplotlib_scale(self.delegate.get_yscale())
            if not self.delegate.get_autoscaley_on():
                self._plot.y_axis.limit = self.delegate.get_ylim()

            self._plot.y_axis.label = ylabel
            self._plot.y_axis.scale = yscale

        self._figure.plots.append(self._plot)

    def __getattr__(self, __name: str) -> Any:
        if __name in PLOTTING_METHODS:
            logging.warning(f"{__name} is not supported by PlotSerializer! Data will be lost!")

        return super().__getattr__(__name)


class _AxesProxy3D(Proxy[MplAxes3D]):
    def __init__(self, delegate: MplAxes3D, figure: Figure, serializer: Serializer) -> None:
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
            sizes_list = kwargs.get("s") or []
            marker = kwargs.get("marker") or "o"

            color_list = kwargs.get("c") or []
            cmap = kwargs.get("cmap") or "viridis"
            norm = kwargs.get("norm") or "linear"
            (color_list, cmap_used) = _convert_matplotlib_color(self, color_list, len(x_values), cmap, norm)

            if isinstance(x_values, float) or isinstance(x_values, int):
                x_values = [x_values]
            if isinstance(y_values, float) or isinstance(y_values, int):
                y_values = [y_values]
            if isinstance(z_values, float) or isinstance(z_values, int):
                z_values = [z_values]
            if isinstance(sizes_list, float) or isinstance(sizes_list, int):
                sizes_list = [sizes_list]

            trace: List[ScatterTrace3D] = []
            datapoints: List[Point3D] = []

            sizes: List[float] = []
            if sizes_list:
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

            for i in range(len(x_values)):
                c = color_list[i] if i < len(color_list) else None
                s = sizes[i]
                datapoints.append(Point3D(x=x_values[i], y=y_values[i], z=z_values[i], color=c, size=s))

            label = str(path.get_label())
            if not cmap_used:
                cmap = None
                norm = None
            trace.append(
                ScatterTrace3D(
                    type="scatter3D", cmap=cmap, norm=norm, label=label, datapoints=datapoints, marker=marker
                )
            )

            if self._plot is not None:
                if not isinstance(self._plot, Plot3D):
                    raise NotImplementedError("PlotSerializer does not yet support mixing 3d plots with other plots!")
                self._plot.traces += trace
            else:
                self._plot = Plot3D(type="3d", x_axis=Axis(), y_axis=Axis(), z_axis=Axis(), traces=trace)
        except Exception as e:
            logging.warning(
                "An unexpected error occurred in PlotSerializer when trying to read plot data! "
                + "Parts of the plot will not be serialized!",
                exc_info=e,
            )

        return path

    def plot(
        self,
        x_values: list[float],
        y_values: list[float],
        *args: Any,
        **kwargs: Any,
    ) -> Path3DCollection:
        path = self.delegate.plot(x_values, y_values, *args, **kwargs)

        try:
            marker = kwargs.get("marker") or None
            color_list = kwargs.get("color") or []
            color_list = _convert_matplotlib_color(self, color_list, len(x_values), "viridis", "linear")[0]

            mpl_line = path[0]
            xdata, ydata, zdata = mpl_line.get_data_3d()

            label = mpl_line.get_label()
            thickness = mpl_line.get_linewidth()
            linestyle = mpl_line.get_linestyle()

            datapoints: List[Point3D] = []
            for i in range(len(xdata)):
                datapoints.append(Point3D(x=xdata[i], y=ydata[i], z=zdata[i]))

            trace: List[LineTrace3D] = []
            trace.append(
                LineTrace3D(
                    type="line3D",
                    line_color=color_list[0],
                    line_thickness=thickness,
                    line_style=linestyle,
                    label=label,
                    datapoints=datapoints,
                    marker=marker,
                )
            )

            if self._plot is not None:
                if not isinstance(self._plot, Plot3D):
                    raise NotImplementedError("PlotSerializer does not yet support mixing 3d plots with other plots!")
                self._plot.traces += trace
            else:
                self._plot = Plot3D(type="3d", x_axis=Axis(), y_axis=Axis(), z_axis=Axis(), traces=trace)
        except Exception as e:
            logging.warning(
                "An unexpected error occurred in PlotSerializer when trying to read plot data! "
                + "Parts of the plot will not be serialized!",
                exc_info=e,
            )

        return path

    def plot_surface(
        self,
        x_values: list[list[float]],
        y_values: list[list[float]],
        z_values: list[list[float]],
        *args: Any,
        **kwargs: Any,
    ) -> Poly3DCollection:
        surface = self.delegate.plot_surface(x_values, y_values, z_values, *args, **kwargs)

        try:
            length = len(x_values)
            width = len(x_values[0])

            if not length == len(y_values) == len(z_values):
                raise ValueError("The x, y and z arrays do not contain the same amount of elements")

            traces: List[SurfaceTrace3D] = []
            datapoints: List[Point3D] = []

            color = kwargs.get("color") or None
            label = surface.get_label()

            for i in range(length):
                if not width == len(x_values[i]) == len(y_values[i]) == len(z_values[i]):
                    raise ValueError(
                        f"The x, y and z arrays do not contain the same amount of elements in the second dimension {i}"
                    )

                for j in range(width):
                    datapoints.append(
                        Point3D(
                            x=x_values[i][j],
                            y=y_values[i][j],
                            z=z_values[i][j],
                            color=color,
                            # size=s,
                        )
                    )

            traces.append(
                SurfaceTrace3D(
                    type="surface3D",
                    length=length,
                    width=width,
                    label=label,
                    datapoints=datapoints,
                )
            )

            if self._plot is not None:
                if not isinstance(self._plot, Plot3D):
                    raise NotImplementedError("PlotSerializer does not yet support mixing 3d plots with other plots!")
                self._plot.traces += traces
            else:
                self._plot = Plot3D(
                    type="3d",
                    x_axis=Axis(),
                    y_axis=Axis(),
                    z_axis=Axis(),
                    traces=traces,
                )
        except Exception as e:
            logging.warning(
                "An unexpected error occurred in PlotSerializer when trying to read plot data! "
                + "Parts of the plot will not be serialized!",
                exc_info=e,
            )

        return surface

    def _on_collect(self) -> None:
        if self._plot is None:
            return

        self._plot.title = self.delegate.get_title()

        if isinstance(self._plot, Plot3D):
            xlabel = self.delegate.get_xlabel()
            xscale = _convert_matplotlib_scale(self.delegate.get_xscale())

            self._plot.x_axis.label = xlabel
            self._plot.x_axis.scale = xscale
            if not self.delegate.get_autoscalex_on():
                self._plot.x_axis.limit = self.delegate.get_xlim()

            ylabel = self.delegate.get_ylabel()
            yscale = _convert_matplotlib_scale(self.delegate.get_yscale())

            self._plot.y_axis.label = ylabel
            self._plot.y_axis.scale = yscale
            if not self.delegate.get_autoscaley_on():
                self._plot.y_axis.limit = self.delegate.get_ylim()

            zlabel = self.delegate.get_zlabel()
            zscale = _convert_matplotlib_scale(self.delegate.get_zscale())

            self._plot.z_axis.label = zlabel
            self._plot.z_axis.scale = zscale
            if not self.delegate.get_autoscalez_on():
                self._plot.z_axis.limit = self.delegate.get_zlim()

        self._figure.plots.append(self._plot)

    def __getattr__(self, __name: str) -> Any:
        if __name in PLOTTING_METHODS:
            logging.warning(f"{__name} is not supported by PlotSerializer, the Data will not be saved!")

        return super().__getattr__(__name)


class MatplotlibSerializer(Serializer):
    """
    Serializer specific to matplotlib. Most of the methods on this object mirror the
    matplotlib.pyplot api from matplotlib.

    Args:
        Serializer (_type_): Parent class
    """

    def _create_axes_proxy(self, mpl_axes: Union[MplAxes3D, MplAxes]) -> Union[_AxesProxy, _AxesProxy3D]:
        proxy: Any
        if isinstance(mpl_axes, MplAxes3D):
            proxy = _AxesProxy3D(mpl_axes, self._figure, self)
            self._add_collect_action(lambda: proxy._on_collect())
        elif isinstance(mpl_axes, MplAxes):
            proxy = _AxesProxy(mpl_axes, self._figure, self)
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
