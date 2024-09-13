import logging
from typing import (
    Any,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
)

import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.pyplot
import numpy as np
from matplotlib.axes import Axes as MplAxes
from matplotlib.collections import PathCollection
from matplotlib.container import BarContainer, ErrorbarContainer
from matplotlib.figure import Figure as MplFigure
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon
from mpl_toolkits.mplot3d.art3d import Path3DCollection, Poly3DCollection
from mpl_toolkits.mplot3d.axes3d import Axes3D as MplAxes3D
from numpy import ndarray

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

    # FIXME: size_list cannot only be floats, but also different other types of data
    def pie(self, size_list: Iterable[float], **kwargs: Any) -> Any:
        result = self.delegate.pie(size_list, **kwargs)

        try:
            if self._plot is not None:
                raise NotImplementedError("PlotSerializer does not yet support adding multiple plots per axes!")

            slices: List[Slice] = []

            explode_list = kwargs.get("explode") or []
            label_list = kwargs.get("labels") or []
            radius_list = kwargs.get("radius") or []

            color_list = kwargs.get("colors") or []
            color_list = _convert_matplotlib_color(self, color_list, len(size_list), cmap="viridis", norm="linear")[0]
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
                        color=color,
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
        self,
        label_list: Iterable[str] | float | int | Iterable[float] | Iterable[int],
        height_list: Iterable[str] | float | int | Iterable[float] | Iterable[int],
        **kwargs: Any,
    ) -> BarContainer:
        result = self.delegate.bar(label_list, height_list, **kwargs)

        try:
            bars: List[Bar2D] = []

            color_list = kwargs.get("color") or []
            color_list = _convert_matplotlib_color(self, color_list, len(label_list), cmap="viridis", norm="linear")[0]

            for i, label in enumerate(label_list):
                height = height_list[i]
                color = color_list[i] if i < len(color_list) else None

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

            label = str(path.get_label())
            datapoints: List[Point2D] = []

            verteces = path.get_offsets().tolist()

            for index, vertex in enumerate(verteces):
                color = color_list[index] if index < len(color_list) else None
                size = sizes_list[index] if index < len(sizes_list) else None

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
        dic = self.delegate.boxplot(x, *args, **kwargs)
        try:
            notch = kwargs.get("notch") or None
            whis = kwargs.get("whis") or None
            bootstrap = kwargs.get("bootstrap")
            usermedians = kwargs.get("usermedians") or []
            conf_intervals = kwargs.get("conf_intervals") or []
            labels = kwargs.get("tick_labels") or []

            trace: List[BoxTrace2D] = []
            boxes: List[Box] = []

            if not (self._are_lists_same_length(x, labels, usermedians, conf_intervals)):
                raise ValueError("lengthes of lists do not match")
            if not (isinstance(x, list) and all(isinstance(sublist, list) for sublist in x)):
                x = [x]
            if isinstance(labels, str):
                labels = [labels for element in x]
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
        container = self.delegate.errorbar(x, y, *args, **kwargs)
        try:
            xerr = kwargs.get("xerr") or None
            yerr = kwargs.get("yerr") or None
            marker = kwargs.get("marker") or None
            color = kwargs.get("color") or None
            ecolor = kwargs.get("ecolor") or None
            label = kwargs.get("label") or None

            if isinstance(xerr, float) or isinstance(xerr, int):
                xerr = [[xerr, xerr] for i in range(len(x))]
            elif isinstance(xerr[0], float) or isinstance(xerr[0], int):
                xerr = [[xerr[i], xerr[i]] for i in range(x)]

            if isinstance(yerr, float) or isinstance(yerr, int):
                yerr = [[yerr, yerr] for i in range(len(x))]
            elif isinstance(yerr[0], float) or isinstance(yerr[0], int):
                yerr = [[yerr[i], yerr[i]] for i in range(len(x))]

            errorpoints: List[ErrorPoint2D] = []

            for i in range(len(x)):
                errorpoints.append(
                    ErrorPoint2D(
                        x=x[i],
                        y=y[i],
                        x_error=(xerr[i][0], xerr[i][1]) if xerr else None,
                        y_error=(yerr[i][0], yerr[i][1]) if yerr else None,
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
            label_list = kwargs.get("label") or []
            color_list = kwargs.get("color") or []

            color_list = _convert_matplotlib_color(self, color_list, len(x), "viridis", "linear")[0]

            if label_list:
                label_type = type(label_list)
                if label_type is not list:
                    label_list = [label_list]
                if not (len(label_list) == len(x)):
                    if not (len(label_list) - 1):
                        label_list = [label_list[0] for i in range(len(x))]
                    else:
                        raise ValueError("the lenth of your label array does not match the amount of datasets")

            if isinstance(x[0], float) or isinstance(x[0], int):
                x = [x]

            datasets: List[HistDataset] = []

            for i in range(len(x)):
                color = color_list[i] if i < len(color_list) else None
                label = label_list[i] if label_list else None
                datasets.append(HistDataset(data=x[i], color=color, label=label))

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
