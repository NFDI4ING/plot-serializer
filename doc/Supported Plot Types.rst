Supported Plot Types
===========================================

Plot Serializer currently supports the following plot types. Additional supported keyword arguments are noted here.
See `here <https://matplotlib.org/stable/plot_types/index.html>`_ for an explanation of these arguments.

.. list-table:: PlotTypes
    :widths: 25 25 50
    :header-rows: 1

    * - Heading row 1, column 1
      - Heading row 1, column 2
      - Heading row 1, column 3
    * - Row 1, column 1
      -
      - Row 1, column 3
    * - Row 2, column 1
      - Row 2, column 2
      - Row 2, column 3

    +---------------------+---------------------+
    |    Column 1         |       Column 2      |
    +=====================+=====================+
    |    Row 1, Col 1     |    Row 1, Col 2     |
    +---------------------+---------------------+
    |    Row 2, Col 1     |    Row 2, Col 2     |
    +---------------------+---------------------+

1D/2D Plots
---------------------------------
**Line**:
    * label
    * linestyle
    * linewidth
    * color, given as a string

**Pie**:
    * labels
    * explode
    * color, given as a list of strings

**Bar**:
    * color, given as a list of strings

**Boxplot**:
    * labels
    * notch
    * whis
    * bootstrap
    * usermedians
    * conf_intervals

**2D-Scatter**:
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
    * label
    * color
    * linewidth
    * linestyle

**3D-Surface**:
    * label

**3D-Scatter**:
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