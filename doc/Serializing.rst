
Serialized parameters
----------------------------------------

PlotSerializer always reads out the main arguments of the plot. Further serialized keyword parameters will be specifically noted.
As a rule of thumb most options to change the style and look of a diagram will not be serialized and can even distort the data inside the JSON file.
Similarly beware of modifying diagrams after creating them.
An example of this would be you taking the returned objects of these methods and calling further functions on them, modyfying their attributes.
This will not be caught upon by PlotSerializer and the change will be ignored.

Plot Serializer currently supports the following plot types. Supported arguments that will get serialized are noted below.
See `here <https://matplotlib.org/stable/plot_types/index.html>`_ for an explanation of these parameters.

**Axes**:
    * title
    * x_label, y_label, z_label
    * x_scale, y_scale, z_scale
    * x_lim, y_lim, z_lim
    * spines


**Line2D**:
    * x
    * y
Optional:
    * label
    * linestyle
    * linewidth
    * color
    * marker

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
    * color

**Boxplot**:
    * x
Optional:
    * tick_labels
    * notch
    * whis
    * bootstrap
    * usermedians
    * conf_intervals

**ErrorBar**
    * x
    * y
Optional:
    * xerr
    * yerr
    * color
    * ecolor
    * label
    * marker

**Histogram**
    * x
Optional:
    * bins
    * label
    * color
    * density
    * cumulative

**2D-Scatter**:
    * x
    * y
Optional:
    * label
    * s
    * c
    * cmap
    * norm
    * marker

3D-Plots
---------------------------------

**3D-Line**:
    * x
    * y
Optional:
    * label
    * color as a string, or rgb/rgba tuple
    * linewidth
    * linestyle
    * marker

**3D-Surface**:
    * x, as a 2D float array
    * y, as a 2D float array
    * z, as a 2D float array
Optional:
    * label
    * marker

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
    * marker



Metadata
---------------------------------

In case of data that can not be plotted or serialized, PlotSerializer provides the option of adding it to the JSON file regardless.
There are five places inside the JSON's hierachy that metadata can be added:
To the entire figure of plots, individual plots, their axis if existent, their traces, and the traces datapoints/slices/boxes. For an Introduction on the Hierachy see Overview.
Metadata is always added via a dict parameter.
A full example:

.. code-block:: python

    from plot_serializer.matplotlib.serializer import MatplotlibSerializer
    import logging

    # set logging to info to get feedback how many traces/datapoints get selected
    logging.basicConfig(level=logging.INFO)
    serializer = MatplotlibSerializer()
    _, ax = serializer.subplots()

    x = [1, 4]
    y = [7, 4]
    z = [10, 4]
    ax.plot(x, y)
    ax.plot(y, z)

    serializer.add_custom_metadata_figure({'date_created' : "10.01.2023"})
    serializer.add_custom_metadata_plot({'group_traces' : "data for longevity in mice"})
    serializer.add_custom_metadata_axis({'axis_information' : "link to unit: example_unit.html"}, axis="y")
    serializer.add_custom_metadata_trace({'collected_data' : "from 08.01.2023"}, trace_selector=0)
    serializer.add_custom_metadata_datapoints(
        {'information' : "the data of this point might be faulty"}, trace_selector=0, point_selector= 1
        )

To understand where each metadata gets added you can take a look at the JSON output:

.. image:: static/custom_metadata_example.png
  :width: 400
  :alt: JSON file with custom metadata



**Selecting Traces:**
There are two options to select traces: By index and by distance.
Selecting by index is done by passing trace_selector an integer. It selects the trace corresponding to the i-th plot plotted.
Selecting by distance can be done via a tuple and relative tolerance. It selects the traces which have a datapoint near the given point.

.. code-block:: python

    serializer.add_custom_metadata_trace(
        {'data1' : "from 08.01.2023"}, trace_selector=0
        )
    serializer.add_custom_metadata_trace(
        {'data2' : "from 17.07.2023"}, trace_selector=(3,3), trace_rel_tolerance=0.0001
        )

**Selecting Points:**
Selecting points is done similarily to selecting traces. By index or distance. You can however also narrow the traces down via the same rules given in the paragraph above.
Selecting by index is done by passing point selector an integer. It selects the datapoint corresponding to the index of your input data.
Pie Plots slices, Bar plots bars, Boxplots boxes and Histograms datasets are also considered as "points" in this specific regard and can be supplemented with metadata.
Selecting by distance is only viable for datapoints where all axes units are numbers, like scatter, lines, surface, etc.

.. code-block:: python

    serializer.add_custom_metadata_datapoints(
        {'info1' : "point might be faulty"}, trace_selector=0, point_selector= 1
        )
    serializer.add_custom_metadata_datapoints(
        {'info2' : "point might be faulty"}, trace_selector=(1,1), trace_rel_tolerance=0.2, point_selector= 1
        )
    serializer.add_custom_metadata_datapoints(
        {'info3' : "point might be faulty"}, trace_selector=0, point_selector=point_selector= (4,4), point_rel_tolerance= 0.0001
        )
    serializer.add_custom_metadata_datapoints(
        {'info4' : "point might be faulty"}, trace_selector=(1,1), trace_rel_tolerance=0.2, point_selector= (4,4), point_rel_tolerance= 0.1
        )
    #specifying no trace will lead to searching above all traces
    serializer.add_custom_metadata_datapoints({'info1' : "point might be faulty"}, point_selector= 1)
