What gets serialized
====================
PlotSerializer always reads out the main arguments of the plot. Further serialized keyword parameters will be specifically noted.
As a rule of thumb most options to change the style and look of a diagram will not be serialized and can even distort the data inside the JSON file.
Similarly beware of modifying diagrams after creating them.
An example of this would be you taking the returned objects of these methods and calling further functions on them, modyfying their attributes.
This will not be caught upon by PlotSerializer and the change will be ignored.

Plot Serializer currently supports the following plot types. Supported arguments that will get serialized are noted below.
See `here <https://matplotlib.org/stable/plot_types/index.html>`_ for an explanation of these parameters.

Axes
----
Serialized arguments:
    * title
    * x_label, y_label, z_label
    * x_scale, y_scale, z_scale
    * x_lim, y_lim, z_lim
    * spines


Line2D
------
Serialized arguments:
    * x
    * y
Optional:
    * label
    * linestyle
    * linewidth
    * color
    * marker

Pie
---
Serialized arguments:
    * x
Optional:
    * labels
    * explode
    * color, given as a list of strings

Bar
---
Serialized arguments:
    * x
    * height
Optional
    * color

Boxplot
-------
Serialized arguments:
    * x
Optional:
    * tick_labels
    * notch
    * whis
    * bootstrap
    * usermedians
    * conf_intervals

ErrorBar
--------
Serialized arguments:
    * x
    * y
Optional:
    * xerr
    * yerr
    * color
    * ecolor
    * label
    * marker

Histogram
---------
Serialized arguments:
    * x
Optional:
    * bins
    * label
    * color
    * density
    * cumulative

2D-Scatter
----------
Serialized arguments:
    * x
    * y
Optional:
    * label
    * s
    * c
    * cmap
    * norm
    * marker

3D-Line
-------
Serialized arguments:
    * x
    * y
Optional:
    * label
    * color as a string, or rgb/rgba tuple
    * linewidth
    * linestyle
    * marker

3D-Surface
----------
Serialized arguments:
    * x, as a 2D float array
    * y, as a 2D float array
    * z, as a 2D float array
Optional:
    * label
    * marker

3D-Scatter
----------
Serialized arguments:
    * x
    * y
    * z
Optional:
    * label
    * s
    * c
    * cmap
    * norm
    * marker






