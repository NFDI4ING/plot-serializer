from typing import Any, Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes as MplAxes
from matplotlib.figure import Figure as MplFigure
from mpl_toolkits.mplot3d.axes3d import Axes3D as MplAxes3D

from plot_serializer.model import (
    BarTrace2D,
    BoxTrace2D,
    ErrorBar2DTrace,
    Figure,
    HistogramTrace,
    LineTrace2D,
    LineTrace3D,
    PiePlot,
    Plot2D,
    Plot3D,
    ScatterTrace2D,
    ScatterTrace3D,
    SurfaceTrace3D,
)
from plot_serializer.proxy import Proxy


def deserialize_from_json_file(filename: str, fig: Any = None, ax: Any = None) -> Optional[MplFigure]:
    with open(filename, "r") as file:
        return deserialize_from_json(file.read(), fig=fig, ax=ax)


def deserialize_from_json(json: str, fig: Optional[MplFigure] = None, ax: Any = None) -> Optional[MplFigure]:
    model_figure = Figure.model_validate_json(json_data=json)
    if isinstance(ax, Proxy):
        ax = ax.delegate
    if ax is None:
        if model_figure.plots[0].type == "3d":
            fig, ax = plt.subplots(len(model_figure.plots), subplot_kw={"projection": "3d"})
        else:
            fig, ax = plt.subplots(len(model_figure.plots))
    if fig is not None:
        if model_figure.title is not None:
            fig.suptitle(model_figure.title)

    i = 0
    for plot in model_figure.plots:
        ax_ref: MplAxes
        if isinstance(ax, MplAxes):
            ax_ref = ax
        else:
            ax_ref = ax[i]

        if isinstance(plot, Plot2D):
            _deserialize_plot2d(plot, ax_ref)
        elif isinstance(plot, Plot3D):
            _deserialize_plot3d(plot, ax_ref)
        elif isinstance(plot, PiePlot):
            _deserialize_pieplot(plot, ax_ref)
        if plot.title is not None:
            ax_ref.set_title(plot.title)

        i = i + 1

    return fig


def _deserialize_axis2d(plot: Plot2D, ax: MplAxes) -> None:
    ax.set_xlabel("" if plot.x_axis.label is None else plot.x_axis.label)
    ax.set_xscale("" if plot.x_axis.scale is None else plot.x_axis.scale)
    ax.set_ylabel("" if plot.y_axis.label is None else plot.y_axis.label)
    ax.set_yscale("" if plot.y_axis.scale is None else plot.y_axis.scale)
    if plot.x_axis.limit:
        ax.set_xlim(plot.x_axis.limit)
    if plot.y_axis.limit:
        ax.set_ylim(plot.y_axis.limit)
    if plot.spines_removed:
        for spine in plot.spines_removed:
            ax.spines[spine].set_visible(False)


def _deserialize_plot2d(plot: Plot2D, ax: MplAxes) -> None:
    _deserialize_axis2d(plot, ax)

    if plot.title is not None:
        plt.title(plot.title)

    for trace in plot.traces:
        if isinstance(trace, LineTrace2D):
            _deserialize_linetrace2d(trace=trace, ax=ax)
        elif isinstance(trace, ScatterTrace2D):
            _deserialize_scattertrace2d(trace=trace, ax=ax)
        elif isinstance(trace, BarTrace2D):
            _deserialize_bartrace2d(trace=trace, ax=ax)
        elif isinstance(trace, BoxTrace2D):
            _deserialize_boxtrace2d(trace=trace, ax=ax)
        elif isinstance(trace, ErrorBar2DTrace):
            _deserialize_errobar2d(trace=trace, ax=ax)
        elif isinstance(trace, HistogramTrace):
            _deserialize_histtrace2d(trace=trace, ax=ax)
        else:
            raise NotImplementedError(f"Unknown trace type found during deserialization: {type(trace)}")


def _deserialize_linetrace2d(trace: LineTrace2D, ax: MplAxes) -> None:
    x = []
    y = []

    for point in trace.datapoints:
        x.append(point.x)
        y.append(point.y)

    ax.plot(
        x,
        y,
        label=trace.label,
        color=trace.color,
        linewidth=trace.linewidth,
        linestyle=trace.linestyle,
        marker=trace.marker,
    )


def _deserialize_scattertrace2d(trace: ScatterTrace2D, ax: MplAxes) -> None:
    x = []
    y = []
    color = []
    size = []

    for point in trace.datapoints:
        x.append(point.x)
        y.append(point.y)
        color.append(point.color)
        size.append(point.size)

    # We need to ignore the argument types here, because matplotlib says
    # it doesn't support None inside of the lists, but it actually does.
    ax.scatter(
        x,
        y,
        c=color,  # type: ignore[arg-type]
        s=size,
        marker=trace.marker,
    )


def _deserialize_bartrace2d(trace: BarTrace2D, ax: MplAxes) -> None:
    x = []
    height = []
    color = []

    for bar in trace.datapoints:
        x.append(bar.x_i)
        height.append(bar.height)
        color.append(bar.color)

    ax.bar(x, height, color=color)


def _deserialize_boxtrace2d(trace: BoxTrace2D, ax: MplAxes) -> None:
    data = []
    conf_intervals = []
    usermedians = []
    labels = []
    for box in trace.x:
        data.append(box.x_i)
        conf_intervals.append(box.conf_interval)
        usermedians.append(box.usermedian)
        labels.append(box.tick_label)
    ax.boxplot(
        data,
        tick_labels=labels,
        notch=trace.notch,
        whis=trace.whis,  # type: ignore[arg-type]
        bootstrap=trace.bootstrap,
        usermedians=usermedians,
        conf_intervals=conf_intervals,
    )


def _deserialize_errobar2d(trace: ErrorBar2DTrace, ax: MplAxes) -> None:
    x = []
    y = []
    xerr: Any = []
    yerr: Any = []

    for errorpoint in trace.datapoints:
        x.append(errorpoint.x)
        y.append(errorpoint.y)
        if xerr is not None:
            xerr.append(errorpoint.xerr)
        else:
            xerr = None
        if yerr is not None:
            yerr.append(errorpoint.yerr)
        else:
            yerr = None

    ax.errorbar(
        x,
        y,
        xerr=xerr,
        yerr=yerr,
        color=trace.color,
        ecolor=trace.ecolor,
        marker=trace.marker,
    )


def _deserialize_histtrace2d(trace: HistogramTrace, ax: MplAxes) -> None:
    x = []
    color: Any = []
    label: Any = []

    for dataset in trace.x:
        x.append(dataset.x_i)
        if color is not None:
            if not dataset.color:
                color = None
            else:
                color.append(dataset.color)
        if label is not None:
            if not dataset.label:
                label = None
            else:
                label.append(dataset.label)

    ax.hist(
        x,
        color=color,
        label=label,
        bins=trace.bins,
        density=trace.density,
        cumulative=trace.cumulative,
    )


def _deserialize_axis3d(plot: Plot3D, ax: MplAxes3D) -> None:
    ax.set_xlabel("" if plot.x_axis.label is None else plot.x_axis.label)
    ax.set_xscale("" if plot.x_axis.scale is None else plot.x_axis.scale)
    ax.set_ylabel("" if plot.y_axis.label is None else plot.y_axis.label)
    ax.set_yscale("" if plot.y_axis.scale is None else plot.y_axis.scale)
    ax.set_zlabel("" if plot.z_axis.label is None else plot.z_axis.label, rotation=90)
    ax.zaxis.labelpad = -0.7
    ax.set_zscale("" if plot.z_axis.scale is None else plot.z_axis.scale)
    if plot.x_axis.limit:
        ax.set_xlim(plot.x_axis.limit)
    if plot.y_axis.limit:
        ax.set_ylim(plot.y_axis.limit)
    if plot.z_axis.limit:
        ax.set_zlim(plot.z_axis.limit)


def _deserialize_plot3d(plot: Plot3D, ax: MplAxes) -> None:
    _deserialize_axis3d(plot, ax)

    if plot.title is not None:
        plt.title(plot.title)

    for trace in plot.traces:
        if isinstance(trace, ScatterTrace3D):
            _deserialize_scattertrace3d(trace=trace, ax=ax)
        elif isinstance(trace, LineTrace3D):
            _deserialize_linetrace3d(trace=trace, ax=ax)
        elif isinstance(trace, SurfaceTrace3D):
            _deserialize_surfacetrace3d(trace=trace, ax=ax)
        else:
            raise NotImplementedError(f"Unknown trace type found during deserialization: {type(trace)}")


_MATPLOTLIB_DEFAULT_3D_SCATTER_COLOR = "#000000"
_MATPLOTLIB_DEFAULT_3D_SCATTER_SIZE = 20


def _deserialize_scattertrace3d(trace: ScatterTrace3D, ax: MplAxes3D) -> None:
    x = []
    y = []
    z = []
    color = []
    size = []

    for point in trace.datapoints:
        x.append(point.x)
        y.append(point.y)
        z.append(point.z)
        color.append(point.color if point.color is not None else _MATPLOTLIB_DEFAULT_3D_SCATTER_COLOR)
        size.append(point.size if point.size is not None else _MATPLOTLIB_DEFAULT_3D_SCATTER_SIZE)

    ax.scatter(x, y, z, c=color, s=size, marker=trace.marker)


def _deserialize_linetrace3d(trace: LineTrace3D, ax: MplAxes3D) -> None:
    x = []
    y = []
    z = []

    for point in trace.datapoints:
        x.append(point.x)
        y.append(point.y)
        z.append(point.z)

    ax.plot(
        x,
        y,
        z,
        label=trace.label,
        color=trace.color,
        linewidth=trace.linewidth,
        linestyle=trace.linestyle,
        marker=trace.marker,
    )


def _deserialize_surfacetrace3d(trace: SurfaceTrace3D, ax: MplAxes3D) -> None:
    x = np.zeros([trace.length, trace.width])
    y = np.zeros([trace.length, trace.width])
    z = np.zeros([trace.length, trace.width])
    i = 0
    j = 0
    for point in trace.datapoints:
        if j == trace.width:
            j = 0
            i = i + 1
        x[i][j] = point.x
        y[i][j] = point.y
        z[i][j] = point.z
        j = j + 1
    ax.plot_surface(x, y, z, label=trace.label)


def _deserialize_pieplot(plot: PiePlot, ax: MplAxes) -> None:
    x = []
    explode = []
    label = []
    color = []

    for slice in plot.slices:
        x.append(slice.x)
        label.append(slice.label)
        explode.append(slice.explode)
        color.append(slice.color)

    # We need to ignore the argument types here, because matplotlib says
    # it doesn't support None inside of the lists, but it actually does.
    if plot.radius is None:
        plot.radius = 1
    else:
        ax.pie(
            x,
            labels=label,  # type: ignore[arg-type]
            colors=color,  # type: ignore[arg-type]
            explode=explode,  # type: ignore[arg-type]
            radius=plot.radius,
        )
