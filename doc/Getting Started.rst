Getting Started
===============

Installation
------------
Install PlotSerializer by running

.. code-block:: bash

    pip install plot-serializer


Serializing your first plot
---------------------------
We will serialize an example matplotlib plot that we have created as follows:

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    np.random.seed(19680801)

    X = np.round(np.linspace(0.5, 3.5, 100), 3)
    Y1 = 3 + np.cos(X)
    Y2 = 1 + np.cos(1 + X / 0.75) / 2

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)

    ax.tick_params(which="major", width=1.0, length=10, labelsize=14)
    ax.tick_params(which="minor", width=1.0, length=5, labelsize=10, labelcolor="0.25")

    ax.grid(linestyle="--", linewidth=0.5, color=".25", zorder=-10)

    ax.plot(X, Y1, c="C0", lw=2.5, label="Blue signal", zorder=10)
    ax.plot(X, Y2, c="C1", lw=2.5, label="Orange signal")

    ax.set_title("Example figure", fontsize=20, verticalalignment="bottom")
    ax.set_xlabel("TIME in s", fontsize=14)
    ax.set_ylabel("DISTANCE in m", fontsize=14)
    ax.legend(loc="upper right", fontsize=14)

    plt.show()


Of particular interest are the two following lines:

.. code-block:: python

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

To collect the data from the plot, we want to serialize, we first need to create a ``Serializer`` object.
Specifically, since we're looking at matplotlib in this case, we need to create a ``MatplotlibSerializer``.
The ``MatplotlibSerializer`` also exposes a ``subplots()``-Method.
This way the ``Serializer`` is able to capture everything you do with the returned objects.

In concrete terms, we replace the two lines above with the following code:

.. code-block:: python

    from plot_serializer.matplotlib.serializer import MatplotlibSerializer

    serializer = MatplotlibSerializer()
    fig, ax = serializer.subplots()

Finally, get the resulting Json string, we can invoke the ``json()``-Method on the serializer:

.. code-block:: python

    serializer.to_json()

We can also write the plot to a file directly:

.. code-block:: python

    serializer.write_json_file("test_plot.json")

Adding custom metadata
----------------------------------------
In case of data that can not be plotted or can not be serialized, PlotSerializer provides the option of adding it to the JSON file regardless.
This is done as follows:

.. code-block:: python

    serializer.add_custom_metadata({'date_created' : "10.01.2023"})

The metadata will be shown at the very top of the JSON, as this clipping illustrates:

.. image:: static/custom_metadata_example.png
  :width: 400
  :alt: JSON file with custom metadata

You can also add metadata to the top of the axis and points/slice/bar. For this you need to specify which data-trace you want to select and which point/slice/bar to add to.
Always remember to put these serializers functions after creating all plots and convert to JSON at the very end.
A full example:

.. code-block:: python

    from plot_serializer.matplotlib.serializer import MatplotlibSerializer

    serializer = MatplotlibSerializer()
    fig, ax = serializer.subplots()

    x = [1,2,3,4]
    y = [4,3,2,1]
    ax.scatter(x, y, marker="<")



What does, what does not get serialized?
----------------------------------------

PlotSerializer always reads out the main data for the plot. Further supported parameters will be specifically noted in this documentation, see "Supported Plot Types".
Note that parameters which are used to make the diagram more appealing are not extracted by PlotSerializer. Instead they might distort the data inside the JSON file.
Because of this we recommend to run PlotSerializer first once with your raw data, and simply add the all stylish choices for the plot afterwards.
Similarly beware of modifying the diagram anywhere else besides the creation methods, such as plot,pie,scatter.
An example of this would be you taking the returned objects of these methods and calling further functions on them, modyfying their attributes.
This will not be caught upon by PlotSerializer and the change will be ignored.

Besides the data of the plots, the title label and scales of the axes as well as the title of the whole figure combining them will be serialized.

Integrating with RO-Crates
--------------------------

PlotSerializer is able to integrate with `RO-Crates <https://www.researchobject.org/ro-crate/>`_.
This means that you can add the serialized diagrams to an RO-Crate as a file with appropriate metadata.
You can accomplish this through the ``add_to_ro_crate()``-Method.
The first argument is the file path to the ro-crate directory and the second argument is the location where the file should be placed within the crate.
When the specified RO-Crate does not exist, a new one is created (this can also be controlled through the ``create`` parameter).
PlotSerializer will try to figure out an appropriate name for the object, but can also be explicitly specified with the ``name`` parameter.

.. code-block:: python

    serializer.add_to_ro_crate("crate", "my-plot-2.json")

Deserializing a plot from JSON
------------------------------

PlotSerializer also provides the functionality of converting the JSON file back into a diagram.
Only serialized attributes can influence the deserialized plot,
the created graph might thus look slightly different from the original, the data however will remain unchanged.

We deserialize the JSON file created above as follows:

.. code-block:: python

    from plot_serializer.matplotlib.deserializer import deserialize_from_json_file
    from matplotlib.pyplot as plt

    deserialize_from_json_file("test_plot.json")
    plt.show()


