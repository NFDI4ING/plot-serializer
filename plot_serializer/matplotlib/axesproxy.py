import itertools
import logging
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Tuple,
    TypeVar,
)

import matplotlib.cbook as cbook
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.axes import Axes as MplAxes
from matplotlib.collections import PathCollection
from matplotlib.container import BarContainer, ErrorbarContainer
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Path3DCollection, Poly3DCollection
from mpl_toolkits.mplot3d.axes3d import Axes3D as MplAxes3D

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
    ScatterTrace2D,
    ScatterTrace3D,
    Slice,
    SurfaceTrace3D,
)
from plot_serializer.proxy import Proxy
from plot_serializer.serializer import Serializer

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
    "tricontourtricontourf",
]


F = TypeVar("F", bound=Callable[..., Any])


def inherit_and_extend_doc(base_class: Any, method_name: str, additional_doc: str) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        base_doc = getattr(base_class, method_name).__doc__
        if base_doc is None:
            base_doc = ""
        func.__doc__ = base_doc + additional_doc
        return func

    return decorator


def _convert_matplotlib_color(
    color_list: Any, length: int, cmap: Any, norm: Any
) -> Tuple[List[str] | List[None], bool]:
    cmap_used = False
    if not color_list:
        return ([None], cmap_used)
    colors: List[str] = []
    color_type = type(color_list)

    if isinstance(color_list, np.generic):
        color_list = color_list.item()
    elif isinstance(color_list, np.ndarray):
        color_list = color_list.tolist()

    if color_type is str:
        colors.append(mcolors.to_hex(color_list, keep_alpha=True))
    elif color_type is int or color_type is float:
        scalar_mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
        rgba_tuple = scalar_mappable.to_rgba(color_list)
        hex_value = mcolors.to_hex(rgba_tuple, keep_alpha=True)  # type: ignore
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
                colors.append(None)  # type: ignore
    else:
        raise NotImplementedError("Your color is not supported by PlotSerializer, see Documentation for more detail")
    if not (len(colors) == length):
        if not (len(colors) - 1):
            colors = [colors[0] for i in range(length)]
        else:
            raise ValueError("the lenth of your color array does not match the length of given data")
    return (colors, cmap_used)


class AxesProxy(Proxy[MplAxes]):
    def __init__(self, delegate: MplAxes, figure: Figure, serializer: Serializer) -> None:
        super().__init__(delegate)
        self._figure = figure
        self._serializer = serializer
        self._plot: Optional[Plot] = None

    @inherit_and_extend_doc(MplAxes, "plot", "\n\n Serialized parameters: x, y, color, marker, label. \n\n")
    def pie(self, x: Any, **kwargs: Any) -> Any:
        """
        Serialized parameters: x, labels, explode, radius, colors, title.

        ----------------
        Original matplotlib documentation

        Plot a pie chart.

        Make a pie chart of array *x*.  The fractional area of each wedge is
        given by ``x/sum(x)``.

        The wedges are plotted counterclockwise, by default starting from the
        x-axis.

        Parameters
        ----------
        x : 1D array-like
            The wedge sizes.

        explode : array-like, default: None
            If not *None*, is a ``len(x)`` array which specifies the fraction
            of the radius with which to offset each wedge.

        labels : list, default: None
            A sequence of strings providing the labels for each wedge

        colors : :class:`color` or list of :class:`color`, default: None
            A sequence of colors through which the pie chart will cycle.  If
            *None*, will use the colors in the currently active cycle.

        hatch : str or list, default: None
            Hatching pattern applied to all pie wedges or sequence of patterns
            through which the chart will cycle. For a list of valid patterns.

            .. versionadded:: 3.7

        autopct : None or str or callable, default: None
            If not *None*, *autopct* is a string or function used to label the
            wedges with their numeric value. The label will be placed inside
            the wedge. If *autopct* is a format string, the label will be
            ``fmt % pct``. If *autopct* is a function, then it will be called.

        pctdistance : float, default: 0.6
            The relative distance along the radius at which the text
            generated by *autopct* is drawn. To draw the text outside the pie,
            set *pctdistance* > 1. This parameter is ignored if *autopct* is
            ``None``.

        labeldistance : float or None, default: 1.1
            The relative distance along the radius at which the labels are
            drawn. To draw the labels inside the pie, set  *labeldistance* < 1.
            If set to ``None``, labels are not drawn but are still stored for
            use in `.legend`.

        shadow : bool or dict, default: False
            If bool, whether to draw a shadow beneath the pie. If dict, draw a shadow
            passing the properties in the dict to `.Shadow`.

            .. versionadded:: 3.8
                *shadow* can be a dict.

        startangle : float, default: 0 degrees
            The angle by which the start of the pie is rotated,
            counterclockwise from the x-axis.

        radius : float, default: 1
            The radius of the pie.

        counterclock : bool, default: True
            Specify fractions direction, clockwise or counterclockwise.

        wedgeprops : dict, default: None
            Dict of arguments passed to each `.patches.Wedge` of the pie.
            For example, ``wedgeprops = {'linewidth': 3}`` sets the width of
            the wedge border lines equal to 3. By default, ``clip_on=False``.
            When there is a conflict between these properties and other
            keywords, properties passed to *wedgeprops* take precedence.

        textprops : dict, default: None
            Dict of arguments to pass to the text objects.

        center : (float, float), default: (0, 0)
            The coordinates of the center of the chart.

        frame : bool, default: False
            Plot Axes frame with the chart if true.

        rotatelabels : bool, default: False
            Rotate each label to the angle of the corresponding slice if true.

        normalize : bool, default: True
            When *True*, always make a full pie by normalizing x so that
            ``sum(x) == 1``. *False* makes a partial pie if ``sum(x) <= 1``
            and raises a `ValueError` for ``sum(x) > 1``.

        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER

        Returns
        -------
        patches : list
            A sequence of `matplotlib.patches.Wedge` instances

        texts : list
            A list of the label `.Text` instances.

        autotexts : list
            A list of `.Text` instances for the numeric labels. This will only
            be returned if the parameter *autopct* is not *None*.

        Notes
        -----
        The pie chart will probably look best if the figure and Axes are
        square, or the Axes aspect is equal.
        This method sets the aspect ratio of the axis to "equal".
        The Axes aspect ratio can be controlled with `.Axes.set_aspect`.
        """
        try:
            result = self.delegate.pie(x, **kwargs)
        except Exception as e:
            add_msg = " - This error was thrown by Matplotlib and is independent of PlotSerializer!"
            e.args = (e.args[0] + add_msg,) + e.args[1:] if e.args else (add_msg,)
            raise

        try:
            if self._plot is not None:
                raise NotImplementedError("PlotSerializer does not yet support adding multiple plots per axes!")

            explode_list = kwargs.get("explode")
            label_list = kwargs.get("labels")
            radius = kwargs.get("radius") or 1
            color_list = kwargs.get("colors")
            c = kwargs.get("c")

            x = np.asarray(x)
            if not explode_list:
                explode_list = itertools.repeat(None)
            if not label_list:
                label_list = itertools.repeat(None)
            if c is not None and color_list is None:
                color_list = c
            color_list = _convert_matplotlib_color(color_list, len(x), cmap="viridis", norm="linear")[0]

            slices: List[Slice] = []
            for index, (xi, label, explode) in enumerate(zip(x, label_list, explode_list)):
                color = color_list[index] if len(color_list) > index else None
                slices.append(
                    Slice(
                        x=xi,
                        explode=explode,
                        label=label,
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

    @inherit_and_extend_doc(MplAxes, "bar", "\n\n Serialized parameters: x, height, color. \n\n")
    def bar(
        self,
        x: Any,
        height: Any,
        **kwargs: Any,
    ) -> BarContainer:
        r"""
        Serialized parameters: x, height, color.

        ----------------
        Original matplotlib documentation:
        Make a bar plot.

        The bars are positioned at *x* with the given *align*\ment. Their
        dimensions are given by *height* and *width*. The vertical baseline
        is *bottom* (default 0).

        Many parameters can take either a single value applying to all bars
        or a sequence of values, one for each bar.

        Parameters
        ----------
        x : float or array-like
            The x coordinates of the bars. See also *align* for the
            alignment of the bars to the coordinates.

        height : float or array-like
            The height(s) of the bars.

            Note that if *bottom* has units (e.g. datetime), *height* should be in
            units that are a difference from the value of *bottom* (e.g. timedelta).

        width : float or array-like, default: 0.8
            The width(s) of the bars.

            Note that if *x* has units (e.g. datetime), then *width* should be in
            units that are a difference (e.g. timedelta) around the *x* values.

        bottom : float or array-like, default: 0
            The y coordinate(s) of the bottom side(s) of the bars.

            Note that if *bottom* has units, then the y-axis will get a Locator and
            Formatter appropriate for the units (e.g. dates, or categorical).

        align : {'center', 'edge'}, default: 'center'
            Alignment of the bars to the *x* coordinates:

            - 'center': Center the base on the *x* positions.
            - 'edge': Align the left edges of the bars with the *x* positions.

            To align the bars on the right edge pass a negative *width* and
            ``align='edge'``.

        Returns
        -------
        `.BarContainer`
            Container with all the bars and optionally errorbars.

        Other Parameters
        ----------------
        color : :class:`color` or list of :class:`color`, optional
            The colors of the bar faces.

        edgecolor : :class:`color` or list of :class:`color`, optional
            The colors of the bar edges.

        linewidth : float or array-like, optional
            Width of the bar edge(s). If 0, don't draw edges.

        tick_label : str or list of str, optional
            The tick labels of the bars.
            Default: None (Use default numeric labels.)

        label : str or list of str, optional
            A single label is attached to the resulting `.BarContainer` as a
            label for the whole dataset.
            If a list is provided, it must be the same length as *x* and
            labels the individual bars. Repeated labels are not de-duplicated
            and will cause repeated label entries, so this is best used when
            bars also differ in style (e.g., by passing a list to *color*.)

        xerr, yerr : float or array-like of shape(N,) or shape(2, N), optional
            If not *None*, add horizontal / vertical errorbars to the bar tips.
            The values are +/- sizes relative to the data:

            - scalar: symmetric +/- values for all bars
            - shape(N,): symmetric +/- values for each bar
            - shape(2, N): Separate - and + values for each bar. First row
              contains the lower errors, the second row contains the upper
              errors.
            - *None*: No errorbar. (Default)



        ecolor : :class:`color` or list of :class:`color`, default: 'black'
            The line color of the errorbars.

        capsize : float, default: :rc:`errorbar.capsize`
           The length of the error bar caps in points.

        error_kw : dict, optional
            Dictionary of keyword arguments to be passed to the
            `~.Axes.errorbar` method. Values of *ecolor* or *capsize* defined
            here take precedence over the independent keyword arguments.

        log : bool, default: False
            If *True*, set the y-axis to be log scale.

        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER

        **kwargs : `.Rectangle` properties

        %(Rectangle:kwdoc)s

        See Also
        --------
        barh : Plot a horizontal bar plot.

        Notes
        -----
        Stacked bars can be achieved by passing individual *bottom* values per
        bar.
        """
        try:
            result = self.delegate.bar(x, height, **kwargs)
        except Exception as e:
            add_msg = " - This error was thrown by Matplotlib and is independent of PlotSerializer!"
            e.args = (e.args[0] + add_msg,) + e.args[1:] if e.args else (add_msg,)
            raise

        try:
            color_list = kwargs.get("color")
            c = kwargs.get("c")
            if c is not None and color_list is None:
                color_list = c
            if isinstance(x, np.generic):
                x = x.item()
            if isinstance(x, (float, int, str)):
                x = [x]
            else:
                x = np.asarray(x)
            if isinstance(height, np.generic):
                height = height.item()
            if isinstance(height, (float, int, str)):
                height = [height]
            else:
                height = np.asarray(height)

            color_list = _convert_matplotlib_color(color_list, len(x), cmap="viridis", norm="linear")[0]

            bars: List[Bar2D] = []
            for index, (xi, h) in enumerate(zip(x, height)):
                color = color_list[index] if len(color_list) > index else None
                bars.append(Bar2D(x_i=xi, height=h, color=color))

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
        """
        Serialized parameters: x, y, linewidth, linestyle, marker, color, label.

        ----------------
        Original matplotlib documentation:

        Plot y versus x as lines and/or markers.

        Call signatures::

            plot([x], y, [fmt], *, data=None, **kwargs)
            plot([x], y, [fmt], [x2], y2, [fmt2], ..., **kwargs)

        The coordinates of the points or line nodes are given by *x*, *y*.

        The optional parameter *fmt* is a convenient way for defining basic
        formatting like color, marker and linestyle. It's a shortcut string
        notation described in the *Notes* section below.

        >>> plot(x, y)  # plot x and y using default line style and color
        >>> plot(x, y, "bo")  # plot x and y using blue circle markers
        >>> plot(y)  # plot y using x as index array 0..N-1
        >>> plot(y, "r+")  # ditto, but with red plusses

        You can use `.Line2D` properties as keyword arguments for more
        control on the appearance. Line properties and *fmt* can be mixed.
        The following two calls yield identical results:

        >>> plot(x, y, "go--", linewidth=2, markersize=12)
        >>> plot(x, y, color="green", marker="o", linestyle="dashed", linewidth=2, markersize=12)

        When conflicting with *fmt*, keyword arguments take precedence.


        **Plotting labelled data**

        There's a convenient way for plotting objects with labelled data (i.e.
        data that can be accessed by index ``obj['y']``). Instead of giving
        the data in *x* and *y*, you can provide the object in the *data*
        parameter and just give the labels for *x* and *y*::

        >>> plot("xlabel", "ylabel", data=obj)

        All indexable objects are supported. This could e.g. be a `dict`, a
        `pandas.DataFrame` or a structured numpy array.


        **Plotting multiple sets of data**

        There are various ways to plot multiple sets of data.

        - The most straight forward way is just to call `plot` multiple times.
          Example:

          >>> plot(x1, y1, "bo")
          >>> plot(x2, y2, "go")

        - If *x* and/or *y* are 2D arrays, a separate data set will be drawn
          for every column. If both *x* and *y* are 2D, they must have the
          same shape. If only one of them is 2D with shape (N, m) the other
          must have length N and will be used for every data set m.

          Example:

          >>> x = [1, 2, 3]
          >>> y = np.array([[1, 2], [3, 4], [5, 6]])
          >>> plot(x, y)

          is equivalent to:

          >>> for col in range(y.shape[1]):
          ...     plot(x, y[:, col])

        - The third way is to specify multiple sets of *[x]*, *y*, *[fmt]*
          groups::

          >>> plot(x1, y1, "g^", x2, y2, "g-")

          In this case, any additional keyword argument applies to all
          datasets. Also, this syntax cannot be combined with the *data*
          parameter.

        By default, each line is assigned a different style specified by a
        'style cycle'. The *fmt* and line property parameters are only
        necessary if you want explicit deviations from these defaults.
        Alternatively, you can also change the style cycle using
        :rc:`axes.prop_cycle`.


        Parameters
        ----------
        x, y : array-like or scalar
            The horizontal / vertical coordinates of the data points.
            *x* values are optional and default to ``range(len(y))``.

            Commonly, these parameters are 1D arrays.

            They can also be scalars, or two-dimensional (in that case, the
            columns represent separate data sets).

            These arguments cannot be passed as keywords.

        fmt : str, optional
            A format string, e.g. 'ro' for red circles. See the *Notes*
            section for a full description of the format strings.

            Format strings are just an abbreviation for quickly setting
            basic line properties. All of these and more can also be
            controlled by keyword arguments.

            This argument cannot be passed as keyword.

        data : indexable object, optional
            An object with labelled data. If given, provide the label names to
            plot in *x* and *y*.

            .. note::
                Technically there's a slight ambiguity in calls where the
                second label is a valid *fmt*. ``plot('n', 'o', data=obj)``
                could be ``plt(x, y)`` or ``plt(y, fmt)``. In such cases,
                the former interpretation is chosen, but a warning is issued.
                You may suppress the warning by adding an empty format string
                ``plot('n', 'o', '', data=obj)``.

        Returns
        -------
        list of `.Line2D`
            A list of lines representing the plotted data.

        Other Parameters
        ----------------
        scalex, scaley : bool, default: True
            These parameters determine if the view limits are adapted to the
            data limits. The values are passed on to
            `~.axes.Axes.autoscale_view`.

        **kwargs : `~matplotlib.lines.Line2D` properties, optional
            *kwargs* are used to specify properties like a line label (for
            auto legends), linewidth, antialiasing, marker face color.
            Example::

            >>> plot([1, 2, 3], [1, 2, 3], "go-", label="line 1", linewidth=2)
            >>> plot([1, 2, 3], [1, 4, 9], "rs", label="line 2")

            If you specify multiple lines with one plot call, the kwargs apply
            to all those lines. In case the label object is iterable, each
            element is used as labels for each set of data.

            Here is a list of available `.Line2D` properties:

            %(Line2D:kwdoc)s

        See Also
        --------
        scatter : XY scatter plot with markers of varying size and/or color (
            sometimes also called bubble chart).

        Notes
        -----
        **Format Strings**

        A format string consists of a part for color, marker and line::

            fmt = "[marker][line][color]"

        Each of them is optional. If not provided, the value from the style
        cycle is used. Exception: If ``line`` is given, but no ``marker``,
        the data will be a line without markers.

        Other combinations such as ``[color][marker][line]`` are also
        supported, but note that their parsing may be ambiguous.

        **Markers**

        =============   ===============================
        character       description
        =============   ===============================
        ``'.'``         point marker
        ``','``         pixel marker
        ``'o'``         circle marker
        ``'v'``         triangle_down marker
        ``'^'``         triangle_up marker
        ``'<'``         triangle_left marker
        ``'>'``         triangle_right marker
        ``'1'``         tri_down marker
        ``'2'``         tri_up marker
        ``'3'``         tri_left marker
        ``'4'``         tri_right marker
        ``'8'``         octagon marker
        ``'s'``         square marker
        ``'p'``         pentagon marker
        ``'P'``         plus (filled) marker
        ``'*'``         star marker
        ``'h'``         hexagon1 marker
        ``'H'``         hexagon2 marker
        ``'+'``         plus marker
        ``'x'``         x marker
        ``'X'``         x (filled) marker
        ``'D'``         diamond marker
        ``'d'``         thin_diamond marker
        ``'|'``         vline marker
        ``'_'``         hline marker
        =============   ===============================

        **Line Styles**

        =============    ===============================
        character        description
        =============    ===============================
        ``'-'``          solid line style
        ``'--'``         dashed line style
        ``'-.'``         dash-dot line style
        ``':'``          dotted line style
        =============    ===============================

        Example format strings::

            "b"  # blue markers with default shape

            "or"  # red circles
            "-g"  # green solid line
            "--"  # dashed line with default color
            "^k:"  # black triangle_up markers connected by a dotted line

        **Colors**

        The supported color abbreviations are the single letter codes

        =============    ===============================
        character        color
        =============    ===============================
        ``'b'``          blue
        ``'g'``          green
        ``'r'``          red
        ``'c'``          cyan
        ``'m'``          magenta
        ``'y'``          yellow
        ``'k'``          black
        ``'w'``          white
        =============    ===============================

        and the ``'CN'`` colors that index into the default property cycle.

        If the color is the only part of the format string, you can
        additionally use any  `matplotlib.colors` spec, e.g. full names
        (``'green'``) or hex strings (``'#008000'``).
        """
        try:
            mpl_lines = self.delegate.plot(*args, **kwargs)
        except Exception as e:
            add_msg = " - This error was thrown by Matplotlib and is independent of PlotSerializer!"
            e.args = (e.args[0] + add_msg,) + e.args[1:] if e.args else (add_msg,)
            raise

        try:
            traces: List[ScatterTrace2D | LineTrace2D | BarTrace2D | BoxTrace2D | HistogramTrace | ErrorBar2DTrace] = []

            for mpl_line in mpl_lines:
                xdata = mpl_line.get_xdata()
                ydata = mpl_line.get_ydata()
                thickness = mpl_line.get_linewidth()
                linestyle = mpl_line.get_linestyle()
                marker = mpl_line.get_marker()
                label = mpl_line.get_label()
                color_list = kwargs.get("color")
                c = kwargs.get("c")

            if isinstance(xdata, np.generic):
                xdata = xdata.item()
            if isinstance(xdata, (float, int, str)):
                xdata = [xdata]
            else:
                xdata = np.asarray(xdata)

            if isinstance(ydata, np.generic):
                ydata = ydata.item()
            if isinstance(ydata, (float, int, str)):
                ydata = [ydata]
            else:
                ydata = np.asarray(ydata)

                if c is not None and color_list is None:
                    color_list = c
                color_list = _convert_matplotlib_color(color_list, len(xdata), cmap="viridis", norm="linear")[0]

                points: List[Point2D] = []
                for x, y in zip(xdata, ydata):
                    points.append(Point2D(x=x, y=y))

                traces.append(
                    LineTrace2D(
                        type="line",
                        color=color_list[0],
                        linewidth=thickness,
                        linestyle=linestyle,  # type: ignore
                        label=label,  # type: ignore
                        datapoints=points,
                        marker=marker,  # type: ignore
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
        x: Any,
        y: Any,
        *args: Any,
        **kwargs: Any,
    ) -> PathCollection:
        """
        Serialized parameters: x, y, s, c, marker, cmap, norm.

        ----------------
        Original matplotlib documentation:
        A scatter plot of *y* vs. *x* with varying marker size and/or color.

        Parameters
        ----------
        x, y : float or array-like, shape (n, )
            The data positions.

        s : float or array-like, shape (n, ), optional
            The marker size in points**2 (typographic points are 1/72 in.).
            Default is ``rcParams['lines.markersize'] ** 2``.

            The linewidth and edgecolor can visually interact with the marker
            size, and can lead to artifacts if the marker size is smaller than
            the linewidth.

            If the linewidth is greater than 0 and the edgecolor is anything
            but *'none'*, then the effective size of the marker will be
            increased by half the linewidth because the stroke will be centered
            on the edge of the shape.

            To eliminate the marker edge either set *linewidth=0* or
            *edgecolor='none'*.

        c : array-like or list of :class:`color` or :class:`color`, optional
            The marker colors. Possible values:

            - A scalar or sequence of n numbers to be mapped to colors using
              *cmap* and *norm*.
            - A 2D array in which the rows are RGB or RGBA.
            - A sequence of colors of length n.
            - A single color format string.

            Note that *c* should not be a single numeric RGB or RGBA sequence
            because that is indistinguishable from an array of values to be
            colormapped. If you want to specify the same RGB or RGBA value for
            all points, use a 2D array with a single row.  Otherwise,
            value-matching will have precedence in case of a size matching with
            *x* and *y*.

            If you wish to specify a single color for all points
            prefer the *color* keyword argument.

            Defaults to `None`. In that case the marker color is determined
            by the value of *color*, *facecolor* or *facecolors*. In case
            those are not specified or `None`, the marker color is determined
            by the next color of the ``Axes``' current "shape and fill" color
            cycle. This cycle defaults to :rc:`axes.prop_cycle`.

        marker : `~.markers.MarkerStyle`, default: :rc:`scatter.marker`
            The marker style. *marker* can be either an instance of the class
            or the text shorthand for a particular marker.
            See :mod:`matplotlib.markers` for more information about marker
            styles.

        %(cmap_doc)s

            This parameter is ignored if *c* is RGB(A).

        %(norm_doc)s

            This parameter is ignored if *c* is RGB(A).

        %(vmin_vmax_doc)s

            This parameter is ignored if *c* is RGB(A).

        alpha : float, default: None
            The alpha blending value, between 0 (transparent) and 1 (opaque).

        linewidths : float or array-like, default: :rc:`lines.linewidth`
            The linewidth of the marker edges. Note: The default *edgecolors*
            is 'face'. You may want to change this as well.

        edgecolors : {'face', 'none', *None*} or :class:`color` or list of \
:class:`color`, default: :rc:`scatter.edgecolors`
            The edge color of the marker. Possible values:

            - 'face': The edge color will always be the same as the face color.
            - 'none': No patch boundary will be drawn.
            - A color or sequence of colors.

            For non-filled markers, *edgecolors* is ignored. Instead, the color
            is determined like with 'face', i.e. from *c*, *colors*, or
            *facecolors*.

        plotnonfinite : bool, default: False
            Whether to plot points with nonfinite *c* (i.e. ``inf``, ``-inf``
            or ``nan``). If ``True`` the points are drawn with the *bad*
            colormap color (see `.Colormap.set_bad`).

        Returns
        -------
        `~matplotlib.collections.PathCollection`

        Other Parameters
        ----------------
        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER
        **kwargs : `~matplotlib.collections.Collection` properties

        See Also
        --------
        plot : To plot scatter plots when markers are identical in size and
            color.

        Notes
        -----
        * The `.plot` function will be faster for scatterplots where markers
          don't vary in size or color.

        * Any or all of *x*, *y*, *s*, and *c* may be masked arrays, in which
          case all masks will be combined and only unmasked points will be
          plotted.

        * Fundamentally, scatter works with 1D arrays; *x*, *y*, *s*, and *c*
          may be input as N-D arrays, but within scatter they will be
          flattened. The exception is *c*, which will be flattened only if its
          size matches the size of *x* and *y*.

        """
        try:
            path = self.delegate.scatter(x, y, *args, **kwargs)
        except Exception as e:
            add_msg = " - This error was thrown by Matplotlib and is independent of PlotSerializer!"
            e.args = (e.args[0] + add_msg,) + e.args[1:] if e.args else (add_msg,)
            raise

        try:
            verteces = path.get_offsets().tolist()  # type: ignore
            marker = kwargs.get("marker") or "o"
            color_list = kwargs.get("c")
            color = kwargs.get("color")
            if color is not None and color_list is None:
                color_list = color
            sizes_list = kwargs.get("s")
            cmap = kwargs.get("cmap") or "viridis"
            norm = kwargs.get("norm") or "linear"
            label = str(path.get_label())

            if isinstance(x, np.generic):
                x = x.item()
            if isinstance(x, (float, int, str)):
                x = [x]

            (color_list, cmap_used) = _convert_matplotlib_color(color_list, len(x), cmap, norm)
            if not cmap_used:
                cmap = None
                norm = None

            if sizes_list is not None:
                sizes_list = path.get_sizes()
            else:
                sizes_list = itertools.repeat(None)
            if isinstance(sizes_list, np.generic):
                sizes_list = [sizes_list] * len(x)

            datapoints: List[Point2D] = []
            for index, (vertex, size) in enumerate(zip(verteces, sizes_list)):
                color = color_list[index] if len(color_list) > index else None
                datapoints.append(
                    Point2D(
                        x=vertex[0],
                        y=vertex[1],
                        color=color,
                        size=size,
                    )
                )
            trace: List[ScatterTrace2D | LineTrace2D | BarTrace2D | BoxTrace2D | HistogramTrace | ErrorBar2DTrace] = []
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

    def boxplot(self, x: Any, *args: Any, **kwargs: Any) -> dict[Any, Any]:
        """
        Serialized parameters: x, notch, whis, bootstrap, usermedians, conf_intervals, tick_labels.

        ----------------
        Original matplotlib documentation:

        Draw a box and whisker plot.

        The box extends from the first quartile (Q1) to the third
        quartile (Q3) of the data, with a line at the median.
        The whiskers extend from the box to the farthest data point
        lying within 1.5x the inter-quartile range (IQR) from the box.
        Flier points are those past the end of the whiskers.
        See https://en.wikipedia.org/wiki/Box_plot for reference.

        .. code-block:: none

                  Q1-1.5IQR   Q1   median  Q3   Q3+1.5IQR
                               |-----:-----|
               o      |--------|     :     |--------|    o  o
                               |-----:-----|
             flier             <----------->            fliers
                                    IQR


        Parameters
        ----------
        x : Array or a sequence of vectors.
            The input data.  If a 2D array, a boxplot is drawn for each column
            in *x*.  If a sequence of 1D arrays, a boxplot is drawn for each
            array in *x*.

        notch : bool, default: :rc:`boxplot.notch`
            Whether to draw a notched boxplot (`True`), or a rectangular
            boxplot (`False`).  The notches represent the confidence interval
            (CI) around the median.  The documentation for *bootstrap*
            describes how the locations of the notches are computed by
            default, but their locations may also be overridden by setting the
            *conf_intervals* parameter.

            .. note::

                In cases where the values of the CI are less than the
                lower quartile or greater than the upper quartile, the
                notches will extend beyond the box, giving it a
                distinctive "flipped" appearance. This is expected
                behavior and consistent with other statistical
                visualization packages.

        sym : str, optional
            The default symbol for flier points.  An empty string ('') hides
            the fliers.  If `None`, then the fliers default to 'b+'.  More
            control is provided by the *flierprops* parameter.

        vert : bool, default: :rc:`boxplot.vertical`
            If `True`, draws vertical boxes.
            If `False`, draw horizontal boxes.

        whis : float or (float, float), default: 1.5
            The position of the whiskers.

            If a float, the lower whisker is at the lowest datum above
            ``Q1 - whis*(Q3-Q1)``, and the upper whisker at the highest datum
            below ``Q3 + whis*(Q3-Q1)``, where Q1 and Q3 are the first and
            third quartiles.  The default value of ``whis = 1.5`` corresponds
            to Tukey's original definition of boxplots.

            If a pair of floats, they indicate the percentiles at which to
            draw the whiskers (e.g., (5, 95)).  In particular, setting this to
            (0, 100) results in whiskers covering the whole range of the data.

            In the edge case where ``Q1 == Q3``, *whis* is automatically set
            to (0, 100) (cover the whole range of the data) if *autorange* is
            True.

            Beyond the whiskers, data are considered outliers and are plotted
            as individual points.

        bootstrap : int, optional
            Specifies whether to bootstrap the confidence intervals
            around the median for notched boxplots. If *bootstrap* is
            None, no bootstrapping is performed, and notches are
            calculated using a Gaussian-based asymptotic approximation
            (see McGill, R., Tukey, J.W., and Larsen, W.A., 1978, and
            Kendall and Stuart, 1967). Otherwise, bootstrap specifies
            the number of times to bootstrap the median to determine its
            95% confidence intervals. Values between 1000 and 10000 are
            recommended.

        usermedians : 1D array-like, optional
            A 1D array-like of length ``len(x)``.  Each entry that is not
            `None` forces the value of the median for the corresponding
            dataset.  For entries that are `None`, the medians are computed
            by Matplotlib as normal.

        conf_intervals : array-like, optional
            A 2D array-like of shape ``(len(x), 2)``.  Each entry that is not
            None forces the location of the corresponding notch (which is
            only drawn if *notch* is `True`).  For entries that are `None`,
            the notches are computed by the method specified by the other
            parameters (e.g., *bootstrap*).

        positions : array-like, optional
            The positions of the boxes. The ticks and limits are
            automatically set to match the positions. Defaults to
            ``range(1, N+1)`` where N is the number of boxes to be drawn.

        widths : float or array-like
            The widths of the boxes.  The default is 0.5, or ``0.15*(distance
            between extreme positions)``, if that is smaller.

        patch_artist : bool, default: :rc:`boxplot.patchartist`
            If `False` produces boxes with the Line2D artist. Otherwise,
            boxes are drawn with Patch artists.

        tick_labels : list of str, optional
            The tick labels of each boxplot.
            Ticks are always placed at the box *positions*. If *tick_labels* is given,
            the ticks are labelled accordingly. Otherwise, they keep their numeric
            values.

            .. versionchanged:: 3.9
                Renamed from *labels*, which is deprecated since 3.9
                and will be removed in 3.11.

        manage_ticks : bool, default: True
            If True, the tick locations and labels will be adjusted to match
            the boxplot positions.

        autorange : bool, default: False
            When `True` and the data are distributed such that the 25th and
            75th percentiles are equal, *whis* is set to (0, 100) such
            that the whisker ends are at the minimum and maximum of the data.

        meanline : bool, default: :rc:`boxplot.meanline`
            If `True` (and *showmeans* is `True`), will try to render the
            mean as a line spanning the full width of the box according to
            *meanprops* (see below).  Not recommended if *shownotches* is also
            True.  Otherwise, means will be shown as points.

        zorder : float, default: ``Line2D.zorder = 2``
            The zorder of the boxplot.

        Returns
        -------
        dict
          A dictionary mapping each component of the boxplot to a list
          of the `.Line2D` instances created. That dictionary has the
          following keys (assuming vertical boxplots):

          - ``boxes``: the main body of the boxplot showing the
            quartiles and the median's confidence intervals if
            enabled.

          - ``medians``: horizontal lines at the median of each box.

          - ``whiskers``: the vertical lines extending to the most
            extreme, non-outlier data points.

          - ``caps``: the horizontal lines at the ends of the
            whiskers.

          - ``fliers``: points representing data that extend beyond
            the whiskers (fliers).

          - ``means``: points or lines representing the means.

        Other Parameters
        ----------------
        showcaps : bool, default: :rc:`boxplot.showcaps`
            Show the caps on the ends of whiskers.
        showbox : bool, default: :rc:`boxplot.showbox`
            Show the central box.
        showfliers : bool, default: :rc:`boxplot.showfliers`
            Show the outliers beyond the caps.
        showmeans : bool, default: :rc:`boxplot.showmeans`
            Show the arithmetic means.
        capprops : dict, default: None
            The style of the caps.
        capwidths : float or array, default: None
            The widths of the caps.
        boxprops : dict, default: None
            The style of the box.
        whiskerprops : dict, default: None
            The style of the whiskers.
        flierprops : dict, default: None
            The style of the fliers.
        medianprops : dict, default: None
            The style of the median.
        meanprops : dict, default: None
            The style of the mean.
        label : str or list of str, optional
            Legend labels. Use a single string when all boxes have the same style and
            you only want a single legend entry for them. Use a list of strings to
            label all boxes individually. To be distinguishable, the boxes should be
            styled individually, which is currently only possible by modifying the
            returned artists.

            In the case of a single string, the legend entry will technically be
            associated with the first box only. By default, the legend will show the
            median line (``result["medians"]``); if *patch_artist* is True, the legend
            will show the box `.Patch` artists (``result["boxes"]``) instead.

            .. versionadded:: 3.9

        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER

        See Also
        --------
        .Axes.bxp : Draw a boxplot from pre-computed statistics.
        violinplot : Draw an estimate of the probability density function.
        """
        try:
            dic = self.delegate.boxplot(x, *args, **kwargs)
        except Exception as e:
            add_msg = " - This error was thrown by Matplotlib and is independent of PlotSerializer!"
            e.args = (e.args[0] + add_msg,) + e.args[1:] if e.args else (add_msg,)
            raise

        try:
            notch = kwargs.get("notch")
            whis = kwargs.get("whis")
            bootstrap = kwargs.get("bootstrap")
            usermedians = kwargs.get("usermedians")
            conf_intervals = kwargs.get("conf_intervals")
            labels = kwargs.get("tick_labels")

            x = cbook._reshape_2D(x, "x")  # type: ignore

            if not labels:
                labels = itertools.repeat(None)
            if not usermedians:
                usermedians = itertools.repeat(None)
            if not conf_intervals:
                conf_intervals = itertools.repeat(None)

            trace: List[ScatterTrace2D | LineTrace2D | BarTrace2D | BoxTrace2D | HistogramTrace | ErrorBar2DTrace] = []
            boxes: List[Box] = []
            for dataset, label, umedian, cintervals in zip(x, labels, usermedians, conf_intervals):
                x = np.ma.asarray(x, dtype="object")  # type: ignore
                x = x.data[~x.mask].ravel()
                boxes.append(
                    Box(
                        x_i=dataset,
                        tick_label=label,
                        usermedian=umedian,
                        conf_interval=cintervals,
                    )
                )
            trace.append(BoxTrace2D(type="box", x=boxes, notch=notch, whis=whis, bootstrap=bootstrap))
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

    def errorbar(self, x: Any, y: Any, *args: Any, **kwargs: Any) -> ErrorbarContainer:
        """
        Serialized parameters: x, y, xerr, yerr, color, ecolor, marker, label.

        ----------------
        Original matplotlib documentation:

        Plot y versus x as lines and/or markers with attached errorbars.

        *x*, *y* define the data locations, *xerr*, *yerr* define the errorbar
        sizes. By default, this draws the data markers/lines as well as the
        errorbars. Use fmt='none' to draw errorbars without any data markers.

        .. versionadded:: 3.7
           Caps and error lines are drawn in polar coordinates on polar plots.


        Parameters
        ----------
        x, y : float or array-like
            The data positions.

        xerr, yerr : float or array-like, shape(N,) or shape(2, N), optional
            The errorbar sizes:

            - scalar: Symmetric +/- values for all data points.
            - shape(N,): Symmetric +/-values for each data point.
            - shape(2, N): Separate - and + values for each bar. First row
              contains the lower errors, the second row contains the upper
              errors.
            - *None*: No errorbar.

            All values must be >= 0.

        fmt : str, default: ''
            The format for the data points / data lines. See `.plot` for
            details.

            Use 'none' (case-insensitive) to plot errorbars without any data
            markers.

        ecolor : :class:`color`, default: None
            The color of the errorbar lines.  If None, use the color of the
            line connecting the markers.

        elinewidth : float, default: None
            The linewidth of the errorbar lines. If None, the linewidth of
            the current style is used.

        capsize : float, default: :rc:`errorbar.capsize`
            The length of the error bar caps in points.

        capthick : float, default: None
            An alias to the keyword argument *markeredgewidth* (a.k.a. *mew*).
            This setting is a more sensible name for the property that
            controls the thickness of the error bar cap in points. For
            backwards compatibility, if *mew* or *markeredgewidth* are given,
            then they will over-ride *capthick*. This may change in future
            releases.

        barsabove : bool, default: False
            If True, will plot the errorbars above the plot
            symbols. Default is below.

        lolims, uplims, xlolims, xuplims : bool or array-like, default: False
            These arguments can be used to indicate that a value gives only
            upper/lower limits.  In that case a caret symbol is used to
            indicate this. *lims*-arguments may be scalars, or array-likes of
            the same length as *xerr* and *yerr*.  To use limits with inverted
            axes, `~.Axes.set_xlim` or `~.Axes.set_ylim` must be called before
            :meth:`errorbar`.  Note the tricky parameter names: setting e.g.
            *lolims* to True means that the y-value is a *lower* limit of the
            True value, so, only an *upward*-pointing arrow will be drawn!

        errorevery : int or (int, int), default: 1
            draws error bars on a subset of the data. *errorevery* =N draws
            error bars on the points (x[::N], y[::N]).
            *errorevery* =(start, N) draws error bars on the points
            (x[start::N], y[start::N]). e.g. errorevery=(6, 3)
            adds error bars to the data at (x[6], x[9], x[12], x[15], ...).
            Used to avoid overlapping error bars when two series share x-axis
            values.

        Returns
        -------
        `.ErrorbarContainer`
            The container contains:

            - data_line : A `~matplotlib.lines.Line2D` instance of x, y plot markers
              and/or line.
            - caplines : A tuple of `~matplotlib.lines.Line2D` instances of the error
              bar caps.
            - barlinecols : A tuple of `.LineCollection` with the horizontal and
              vertical error ranges.

        Other Parameters
        ----------------
        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER

        **kwargs
            All other keyword arguments are passed on to the `~.Axes.plot` call
            drawing the markers. For example, this code makes big red squares
            with thick green edges::

                x, y, yerr = rand(3, 10)
                errorbar(x, y, yerr, marker="s", mfc="red", mec="green", ms=20, mew=4)

            where *mfc*, *mec*, *ms* and *mew* are aliases for the longer
            property names, *markerfacecolor*, *markeredgecolor*, *markersize*
            and *markeredgewidth*.

            Valid kwargs for the marker properties are:

            - *dashes*
            - *dash_capstyle*
            - *dash_joinstyle*
            - *drawstyle*
            - *fillstyle*
            - *linestyle*
            - *marker*
            - *markeredgecolor*
            - *markeredgewidth*
            - *markerfacecolor*
            - *markerfacecoloralt*
            - *markersize*
            - *markevery*
            - *solid_capstyle*
            - *solid_joinstyle*

            Refer to the corresponding `.Line2D` property for more details:

            %(Line2D:kwdoc)s
        """

        def _upcast_err(err: Any) -> Any:
            """
            Imported local function from Matplotlib errorbar function.
            """

            if np.iterable(err) and len(err) > 0 and isinstance(cbook._safe_first_finite(err), np.ndarray):  # type: ignore
                atype = type(cbook._safe_first_finite(err))  # type: ignore
                if atype is np.ndarray:
                    return np.asarray(err, dtype=object)

                return atype(err)

            return np.asarray(err)

        try:
            container = self.delegate.errorbar(x, y, *args, **kwargs)
        except Exception as e:
            add_msg = " - This error was thrown by Matplotlib and is independent of PlotSerializer!"
            e.args = (e.args[0] + add_msg,) + e.args[1:] if e.args else (add_msg,)
            raise

        try:
            xerr = kwargs.get("xerr")
            yerr = kwargs.get("yerr")
            marker = kwargs.get("marker")
            color = kwargs.get("color")
            c = kwargs.get("c")
            if c is not None and color is None:
                color = c
            ecolor = kwargs.get("ecolor")
            label = kwargs.get("label")

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
            else:
                if xerr.ndim == 0 or xerr.ndim == 1:
                    xerr = np.broadcast_to(xerr, (2, len(x)))
                xerr = xerr.T

            if yerr is None:
                yerr = itertools.repeat(None)
            else:
                if yerr.ndim == 0 or yerr.ndim == 1:
                    yerr = np.broadcast_to(yerr, (2, len(y)))
                yerr = yerr.T

            color = mcolors.to_hex(color) if color else None
            ecolor = mcolors.to_hex(ecolor) if ecolor else None

            errorpoints: List[ErrorPoint2D] = []
            for xi, yi, x_error, y_error in zip(x, y, xerr, yerr):
                errorpoints.append(
                    ErrorPoint2D(
                        x=xi,
                        y=yi,
                        xerr=x_error,
                        yerr=y_error,
                    )
                )
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

    def hist(self, x: Any, *args: Any, **kwargs: Any) -> Any:
        """
        Serialized parameters: x, bins, range, cumulative, color, label.

        ----------------
        Original matplotlib documentation:

        Compute and plot a histogram.

        This method uses `numpy.histogram` to bin the data in *x* and count the
        number of values in each bin, then draws the distribution either as a
        `.BarContainer` or `.Polygon`. The *bins*, *range*, *density*, and
        *weights* parameters are forwarded to `numpy.histogram`.

        If the data has already been binned and counted, use `~.bar` or
        `~.stairs` to plot the distribution::

            counts, bins = np.histogram(x)
            plt.stairs(counts, bins)

        Alternatively, plot pre-computed bins and counts using ``hist()`` by
        treating each bin as a single point with a weight equal to its count::

            plt.hist(bins[:-1], bins, weights=counts)

        The data input *x* can be a singular array, a list of datasets of
        potentially different lengths ([*x0*, *x1*, ...]), or a 2D ndarray in
        which each column is a dataset. Note that the ndarray form is
        transposed relative to the list form. If the input is an array, then
        the return value is a tuple (*n*, *bins*, *patches*); if the input is a
        sequence of arrays, then the return value is a tuple
        ([*n0*, *n1*, ...], *bins*, [*patches0*, *patches1*, ...]).

        Masked arrays are not supported.

        Parameters
        ----------
        x : (n,) array or sequence of (n,) arrays
            Input values, this takes either a single array or a sequence of
            arrays which are not required to be of the same length.

        bins : int or sequence or str, default: :rc:`hist.bins`
            If *bins* is an integer, it defines the number of equal-width bins
            in the range.

            If *bins* is a sequence, it defines the bin edges, including the
            left edge of the first bin and the right edge of the last bin;
            in this case, bins may be unequally spaced.  All but the last
            (righthand-most) bin is half-open.  In other words, if *bins* is::

                [1, 2, 3, 4]

            then the first bin is ``[1, 2)`` (including 1, but excluding 2) and
            the second ``[2, 3)``.  The last bin, however, is ``[3, 4]``, which
            *includes* 4.

            If *bins* is a string, it is one of the binning strategies
            supported by `numpy.histogram_bin_edges`: 'auto', 'fd', 'doane',
            'scott', 'stone', 'rice', 'sturges', or 'sqrt'.

        range : tuple or None, default: None
            The lower and upper range of the bins. Lower and upper outliers
            are ignored. If not provided, *range* is ``(x.min(), x.max())``.
            Range has no effect if *bins* is a sequence.

            If *bins* is a sequence or *range* is specified, autoscaling
            is based on the specified bin range instead of the
            range of x.

        density : bool, default: False
            If ``True``, draw and return a probability density: each bin
            will display the bin's raw count divided by the total number of
            counts *and the bin width*
            (``density = counts / (sum(counts) * np.diff(bins))``),
            so that the area under the histogram integrates to 1
            (``np.sum(density * np.diff(bins)) == 1``).

            If *stacked* is also ``True``, the sum of the histograms is
            normalized to 1.

        weights : (n,) array-like or None, default: None
            An array of weights, of the same shape as *x*.  Each value in
            *x* only contributes its associated weight towards the bin count
            (instead of 1).  If *density* is ``True``, the weights are
            normalized, so that the integral of the density over the range
            remains 1.

        cumulative : bool or -1, default: False
            If ``True``, then a histogram is computed where each bin gives the
            counts in that bin plus all bins for smaller values. The last bin
            gives the total number of datapoints.

            If *density* is also ``True`` then the histogram is normalized such
            that the last bin equals 1.

            If *cumulative* is a number less than 0 (e.g., -1), the direction
            of accumulation is reversed.  In this case, if *density* is also
            ``True``, then the histogram is normalized such that the first bin
            equals 1.

        bottom : array-like, scalar, or None, default: None
            Location of the bottom of each bin, i.e. bins are drawn from
            ``bottom`` to ``bottom + hist(x, bins)`` If a scalar, the bottom
            of each bin is shifted by the same amount. If an array, each bin
            is shifted independently and the length of bottom must match the
            number of bins. If None, defaults to 0.

        histtype : {'bar', 'barstacked', 'step', 'stepfilled'}, default: 'bar'
            The type of histogram to draw.

            - 'bar' is a traditional bar-type histogram.  If multiple data
              are given the bars are arranged side by side.
            - 'barstacked' is a bar-type histogram where multiple
              data are stacked on top of each other.
            - 'step' generates a lineplot that is by default unfilled.
            - 'stepfilled' generates a lineplot that is by default filled.

        align : {'left', 'mid', 'right'}, default: 'mid'
            The horizontal alignment of the histogram bars.

            - 'left': bars are centered on the left bin edges.
            - 'mid': bars are centered between the bin edges.
            - 'right': bars are centered on the right bin edges.

        orientation : {'vertical', 'horizontal'}, default: 'vertical'
            If 'horizontal', `~.Axes.barh` will be used for bar-type histograms
            and the *bottom* kwarg will be the left edges.

        rwidth : float or None, default: None
            The relative width of the bars as a fraction of the bin width.  If
            ``None``, automatically compute the width.

            Ignored if *histtype* is 'step' or 'stepfilled'.

        log : bool, default: False
            If ``True``, the histogram axis will be set to a log scale.

        color : :class:`color` or list of :class:`color` or None, default: None
            Color or sequence of colors, one per dataset.  Default (``None``)
            uses the standard line color sequence.

        label : str or list of str, optional
            String, or sequence of strings to match multiple datasets.  Bar
            charts yield multiple patches per dataset, but only the first gets
            the label, so that `~.Axes.legend` will work as expected.

        stacked : bool, default: False
            If ``True``, multiple data are stacked on top of each other If
            ``False`` multiple data are arranged side by side if histtype is
            'bar' or on top of each other if histtype is 'step'

        Returns
        -------
        n : array or list of arrays
            The values of the histogram bins. See *density* and *weights* for a
            description of the possible semantics.  If input *x* is an array,
            then this is an array of length *nbins*. If input is a sequence of
            arrays ``[data1, data2, ...]``, then this is a list of arrays with
            the values of the histograms for each of the arrays in the same
            order.  The dtype of the array *n* (or of its element arrays) will
            always be float even if no weighting or normalization is used.

        bins : array
            The edges of the bins. Length nbins + 1 (nbins left edges and right
            edge of last bin).  Always a single array even when multiple data
            sets are passed in.

        patches : `.BarContainer` or list of a single `.Polygon` or list of \
such objects
            Container of individual artists used to create the histogram
            or list of such containers if there are multiple input datasets.

        Other Parameters
        ----------------
        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER

        **kwargs
            `~matplotlib.patches.Patch` properties

        See Also
        --------
        hist2d : 2D histogram with rectangular bins
        hexbin : 2D histogram with hexagonal bins
        stairs : Plot a pre-computed histogram
        bar : Plot a pre-computed histogram

        Notes
        -----
        For large numbers of bins (>1000), plotting can be significantly
        accelerated by using `~.Axes.stairs` to plot a pre-computed histogram
        (``plt.stairs(*np.histogram(data))``), or by setting *histtype* to
        'step' or 'stepfilled' rather than 'bar' or 'barstacked'.
        """
        try:
            ret = self.delegate.hist(x, *args, **kwargs)
        except Exception as e:
            add_msg = " - This error was thrown by Matplotlib and is independent of PlotSerializer!"
            e.args = (e.args[0] + add_msg,) + e.args[1:] if e.args else (add_msg,)
            raise

        try:
            bins = kwargs.get("bins") or 10
            density = kwargs.get("density") or False
            cumulative = kwargs.get("cumulative") or False
            label_list = kwargs.get("label")
            color_list = kwargs.get("color")
            c = kwargs.get("c")

            if c is not None and color_list is None:
                color_list = c

            if not label_list:
                label_list = itertools.repeat(None)
            else:
                label_list = np.atleast_1d(np.asarray(label_list, str))

            if np.isscalar(x):
                x = [x]
            x = cbook._reshape_2D(x, "x")  # type: ignore

            color_list = _convert_matplotlib_color(color_list, len(x), "viridis", "linear")[0]

            datasets: List[HistDataset] = []
            for index, (element, label) in enumerate(zip(x, label_list)):
                color = color_list[index] if len(color_list) > index else None
                datasets.append(HistDataset(x_i=element, color=color, label=label))

            trace = HistogramTrace(
                type="histogram",
                x=datasets,
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
            xscale = self.delegate.get_xscale()

            self._plot.x_axis.label = xlabel
            self._plot.x_axis.scale = xscale
            if not self.delegate.get_autoscalex_on():
                self._plot.x_axis.limit = self.delegate.get_xlim()

            ylabel = self.delegate.get_ylabel()
            yscale = self.delegate.get_yscale()
            if not self.delegate.get_autoscaley_on():
                self._plot.y_axis.limit = self.delegate.get_ylim()

            self._plot.y_axis.label = ylabel
            self._plot.y_axis.scale = yscale

        self._figure.plots.append(self._plot)

    def __getattr__(self, __name: str) -> Any:
        if __name in PLOTTING_METHODS:
            logging.warning(f"{__name} is not supported by PlotSerializer! Data will be lost!")

        return super().__getattr__(__name)


class AxesProxy3D(Proxy[MplAxes3D]):
    def __init__(self, delegate: MplAxes3D, figure: Figure, serializer: Serializer) -> None:
        super().__init__(delegate)
        self._figure = figure
        self._serializer = serializer
        self._plot: Optional[Plot] = None

    def scatter(
        self,
        xs: Any,
        ys: Any,
        zs: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Path3DCollection:
        """
        Serialized parameters: xs, ys, zs, s, c, cmap, norm, marker, label.

        ----------------
        Original matplotlib documentation:

        Create a scatter plot.

        Parameters
        ----------
        xs, ys : array-like
            The data positions.
        zs : float or array-like, default: 0
            The z-positions. Either an array of the same length as *xs* and
            *ys* or a single value to place all points in the same plane.
        zdir : {'x', 'y', 'z', '-x', '-y', '-z'}, default: 'z'
            The axis direction for the *zs*. This is useful when plotting 2D
            data on a 3D Axes. The data must be passed as *xs*, *ys*. Setting
            *zdir* to 'y' then plots the data to the x-z-plane.

        s : float or array-like, default: 20
            The marker size in points**2. Either an array of the same length
            as *xs* and *ys* or a single value to make all markers the same
            size.
        c : :class:`color`, sequence, or sequence of colors, optional
            The marker color. Possible values:

            - A single color format string.
            - A sequence of colors of length n.
            - A sequence of n numbers to be mapped to colors using *cmap* and
              *norm*.
            - A 2D array in which the rows are RGB or RGBA.

            For more details see the *c* argument of `~.axes.Axes.scatter`.
        depthshade : bool, default: True
            Whether to shade the scatter markers to give the appearance of
            depth. Each call to ``scatter()`` will perform its depthshading
            independently.
        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER
        **kwargs
            All other keyword arguments are passed on to `~.axes.Axes.scatter`.

        Returns
        -------
        paths : `~matplotlib.collections.PathCollection`
        """

        try:
            path = self.delegate.scatter(xs, ys, zs, *args, **kwargs)
        except Exception as e:
            add_msg = " - This error was thrown by Matplotlib and is independent of PlotSerializer!"
            e.args = (e.args[0] + add_msg,) + e.args[1:] if e.args else (add_msg,)
            raise

        try:
            sizes_list = kwargs.get("s")
            marker = kwargs.get("marker") or "o"
            color_list = kwargs.get("c")
            color = kwargs.get("color")
            if color is not None and color_list is None:
                color_list = color
            cmap = kwargs.get("cmap") or "viridis"
            norm = kwargs.get("norm") or "linear"
            label = str(path.get_label())

            if isinstance(xs, np.generic):
                xs = xs.item()
            if isinstance(xs, (float, int, str)):
                xs = [xs]

            (color_list, cmap_used) = _convert_matplotlib_color(color_list, len(xs), cmap, norm)
            if not cmap_used:
                cmap = None
                norm = None

            xs, ys, zs = cbook._broadcast_with_masks(xs, ys, zs)
            xs, ys, zs, sizes_list, color_list, color = cbook.delete_masked_points(  # type: ignore
                xs, ys, zs, sizes_list, color_list, kwargs.get("color", None)
            )

            if sizes_list is None:
                sizes_list = itertools.repeat(None)
            if isinstance(sizes_list, (np.generic, float, int)):
                sizes_list = [sizes_list] * len(xs)

            trace: List[ScatterTrace3D | LineTrace3D | SurfaceTrace3D] = []
            datapoints: List[Point3D] = []
            for index, (xi, yi, zi, s) in enumerate(zip(xs, ys, zs, sizes_list)):
                c = color_list[index] if len(color_list) > index else None
                datapoints.append(Point3D(x=xi, y=yi, z=zi, color=c, size=s))

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
        x_values: Any,
        y_values: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Path3DCollection:
        """
        Serialized parameters: x, y, color, linestyle, linewidth, marker, label.

        ----------------
        Original matplotlib documentation:

        Plot 2D or 3D data.

        Parameters
        ----------
        xs : 1D array-like
            x coordinates of vertices.
        ys : 1D array-like
            y coordinates of vertices.
        zs : float or 1D array-like
            z coordinates of vertices; either one for all points or one for
            each point.
        zdir : {'x', 'y', 'z'}, default: 'z'
            When plotting 2D data, the direction to use as z.
        **kwargs
            Other arguments are forwarded to `matplotlib.axes.Axes.plot`.
        """
        try:
            path = self.delegate.plot(x_values, y_values, *args, **kwargs)
        except Exception as e:
            add_msg = " - This error was thrown by Matplotlib and is independent of PlotSerializer!"
            e.args = (e.args[0] + add_msg,) + e.args[1:] if e.args else (add_msg,)
            raise

        try:
            mpl_line = path[0]
            xdata, ydata, zdata = mpl_line.get_data_3d()
            label = mpl_line.get_label()
            thickness = mpl_line.get_linewidth()
            linestyle = mpl_line.get_linestyle()
            marker = kwargs.get("marker")
            color_list = kwargs.get("color")
            c = kwargs.get("c")
            if c is not None and color_list is None:
                color_list = c

            color_list = _convert_matplotlib_color(color_list, len(x_values), "viridis", "linear")[0]

            datapoints: List[Point3D] = []
            for i in range(len(xdata)):
                datapoints.append(Point3D(x=xdata[i], y=ydata[i], z=zdata[i]))

            trace: List[ScatterTrace3D | LineTrace3D | SurfaceTrace3D] = []
            trace.append(
                LineTrace3D(
                    type="line3D",
                    color=color_list[0],
                    linewidth=thickness,
                    linestyle=linestyle,
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
        x: Any,
        y: Any,
        z: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Poly3DCollection:
        """
        Serialized parameters: x, y, z, label.

        ----------------
        Original matplotlib documentation:

        Create a surface plot.

        By default, it will be colored in shades of a solid color, but it also
        supports colormapping by supplying the *cmap* argument.

        .. note::

           The *rcount* and *ccount* kwargs, which both default to 50,
           determine the maximum number of samples used in each direction.  If
           the input data is larger, it will be downsampled (by slicing) to
           these numbers of points.

        .. note::

           To maximize rendering speed consider setting *rstride* and *cstride*
           to divisors of the number of rows minus 1 and columns minus 1
           respectively. For example, given 51 rows rstride can be any of the
           divisors of 50.

           Similarly, a setting of *rstride* and *cstride* equal to 1 (or
           *rcount* and *ccount* equal the number of rows and columns) can use
           the optimized path.

        Parameters
        ----------
        X, Y, Z : 2D arrays
            Data values.

        rcount, ccount : int
            Maximum number of samples used in each direction.  If the input
            data is larger, it will be downsampled (by slicing) to these
            numbers of points.  Defaults to 50.

        rstride, cstride : int
            Downsampling stride in each direction.  These arguments are
            mutually exclusive with *rcount* and *ccount*.  If only one of
            *rstride* or *cstride* is set, the other defaults to 10.

            'classic' mode uses a default of ``rstride = cstride = 10`` instead
            of the new default of ``rcount = ccount = 50``.

        color : :class:`color`
            Color of the surface patches.

        cmap : Colormap, optional
            Colormap of the surface patches.

        facecolors : list of :class:`color`
            Colors of each individual patch.

        norm : `~matplotlib.colors.Normalize`, optional
            Normalization for the colormap.

        vmin, vmax : float, optional
            Bounds for the normalization.

        shade : bool, default: True
            Whether to shade the facecolors.  Shading is always disabled when
            *cmap* is specified.

        lightsource : `~matplotlib.colors.LightSource`, optional
            The lightsource to use when *shade* is True.

        **kwargs
            Other keyword arguments are forwarded to `.Poly3DCollection`.
        """

        try:
            surface = self.delegate.plot_surface(x, y, z, *args, **kwargs)
        except Exception as e:
            add_msg = " - This error was thrown by Matplotlib and is independent of PlotSerializer!"
            e.args = (e.args[0] + add_msg,) + e.args[1:] if e.args else (add_msg,)
            raise

        try:
            color = kwargs.get("color")
            c = kwargs.get("c")
            if c is not None and color is None:
                color = c
            label = surface.get_label()

            length = len(x)
            width = len(x[0])

            z = cbook._to_unmasked_float_array(z)  # type: ignore
            x, y, z = np.broadcast_arrays(x, y, z)

            traces: List[ScatterTrace3D | LineTrace3D | SurfaceTrace3D] = []
            datapoints: List[Point3D] = []
            for xi, yi, zi in zip(x, y, z):
                for xj, yj, zj in zip(xi, yi, zi):
                    datapoints.append(
                        Point3D(
                            x=xj,
                            y=yj,
                            z=zj,
                            color=color,
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
            xscale = self.delegate.get_xscale()

            self._plot.x_axis.label = xlabel
            self._plot.x_axis.scale = xscale
            if not self.delegate.get_autoscalex_on():
                self._plot.x_axis.limit = self.delegate.get_xlim()

            ylabel = self.delegate.get_ylabel()
            yscale = self.delegate.get_yscale()

            self._plot.y_axis.label = ylabel
            self._plot.y_axis.scale = yscale
            if not self.delegate.get_autoscaley_on():
                self._plot.y_axis.limit = self.delegate.get_ylim()

            zlabel = self.delegate.get_zlabel()
            zscale = self.delegate.get_zscale()

            self._plot.z_axis.label = zlabel
            self._plot.z_axis.scale = zscale
            if not self.delegate.get_autoscalez_on():
                self._plot.z_axis.limit = self.delegate.get_zlim()

        self._figure.plots.append(self._plot)

    def __getattr__(self, __name: str) -> Any:
        if __name in PLOTTING_METHODS:
            logging.warning(f"{__name} is not supported by PlotSerializer, the Data will not be saved!")

        return super().__getattr__(__name)
