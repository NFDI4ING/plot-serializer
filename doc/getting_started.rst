Getting Started
===============
Let's serialize the following simple matplotlib diagram:

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    x = [1,2,3,4]
    y = [1,4,9,16]

    ax.plot(x, y)

    plt.show()

To serialize this diagram with PloSe, i.e. to convert it to a format that enables storing and sharing, 
we first need to create a ``MatplotlibSerializer`` object.
``MatplotlibSerializer`` contains a ``subplots()`` method that wraps the ``matplotlib.pyplot.subplots()`` method,
allowing to extract the data passed to it immedialy after passing them to the method. This way, ``MatplotlibSerializer``
can ensure that the serialized data match the input data that is plotted.

To use ``MatplotlibSerializer``, substitute the ``plt.subplots()`` method with ``MatplotlibSerializer.subplots()`` as follows:

.. code-block:: python

    from plot_serializer.matplotlib.serializer import MatplotlibSerializer

    serializer = MatplotlibSerializer()
    fig, ax = serializer.subplots()

    x = [1, 2, 3, 4]
    y = [3, 5, 6, 6.5]

    ax.plot(x, y)

It is, of course, good (essential!) practice to tell the viewer what the data describes. The bare minimum is providing axis labels.
PloSe will warn you if you don't provide axis labels, so let's specify them:

.. code-block:: python

    ax.set_xlabel("number of cookies eaten")
    ax.set_ylabel("happiness level")


Finally, to serialize the diagram and write it into a JSON file, we invoke the ``write_json_file()`` method:

.. code-block:: python

    serializer.write_json_file("test_plot.json")

Let's inspect the result:

.. code-block:: json

    {
      "plots": [
        {
          "type": "2d",
          "title": "",
          "x_axis": {
            "label": "number of cookies eaten",
            "scale": "linear"
          },
          "y_axis": {
            "label": "happiness level",
            "scale": "linear"
          },
          "traces": [
            {
              "type": "line",
              "line_thickness": 1.5,
              "line_style": "-",
              "marker": "None",
              "label": "_child0",
              "datapoints": [
                {
                  "x": 1.0,
                  "y": 3.0
                },
                {
                  "x": 2.0,
                  "y": 5.0
                },
                {
                  "x": 3.0,
                  "y": 6.0
                },
                {
                  "x": 4.0,
                  "y": 6.5
                }
              ]
            }
          ]
        }
      ]
    }

The diagram is to be found under ``plots``. 