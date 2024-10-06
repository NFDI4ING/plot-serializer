Unique PlotID
===============
To make the JSON data Findable ``(`` **F** AIR data ``)``,
Plot Serializer can be used in conjunction with the `PlotID <https://git.rwth-aachen.de/plotid/plotid_python>`_ project.
PlotID takes a matplotlib figure and returns a unique identifier for it.

.. code-block:: python

    from plot_serializer.matplotlib.serializer import MatplotlibSerializer

    serializer = MatplotlibSerializer()
    fig, ax = serializer.subplots()

    ax.plot([1, 2, 3, 4], [1, 4, 9, 16])
    figs_and_ids = tag_plot(fig, "matplotlib")
    serializer.add_custom_metadata_figure({"PLOT_ID" : figs_and_ids.figure_ids[0]})
