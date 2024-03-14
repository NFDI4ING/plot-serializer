Supported Plot Types
===========================================

Plot Serializer currently supports the following plot types. Supported arguments that will get serialized are noted below.
See `here <https://matplotlib.org/stable/plot_types/index.html>`_ for an explanation of these parameters.

1D/2D Plots
---------------------------------
**Line**:
    * x
    * y
Optional:
    * label
    * linestyle
    * linewidth
    * color, given as a string

**Pie**:
    * x
Optional:
    * labels
    * explode
    * color, given as a list of strings

**Bar**:
    * x
    * height
Optional
    * color, given as a list of strings

**Boxplot**:
    * x
Optional:
    * labels
    * notch
    * whis
    * bootstrap
    * usermedians
    * conf_intervals

**2D-Scatter**:
    * x
    * y
Optional:
    * label
    * s
    * c
    * cmap
    * norm
Note that the scatter plot has increased support for colors. The following inputs types are allowed:
    * string
    * list of strings
    * list of rgb/rgba tuples
    * list of scalar values in combination with a cmap and normalization

3D-Plots
---------------------------------

**3D-Line**:
    * x
    * y
Optional:
    * label
    * color
    * linewidth
    * linestyle

**3D-Surface**:
    * x, as a 2D float array
    * y, as a 2D float array
    * z, as a 2D float array
Optional:
    * label

**3D-Scatter**:
    * x
    * y
    * z
Optional:
    * label
    * s
    * c
    * cmap
    * norm

Note that the scatter plot has increased support for colors. The following inputs types are allowed:
    * string
    * list of strings
    * list of rgb/rgba tuples
    * list of scalar values in combination with a cmap and normalization