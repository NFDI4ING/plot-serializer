
Deserializer
===================

PlotSerializer also provides the functionality of converting the JSON file back into a diagram.
Only serialized attributes can influence the deserialized plot,
the created graph might thus look slightly different from the original, the data however will remain unchanged.
The following sections explain in detail the deserialize support for each plotting library.

Matplotlib-Deserializer
---------------------------------

We deserialize the JSON file created above as follows:

.. code-block:: python

    from plot_serializer.matplotlib.deserializer import deserialize_from_json_file
    from matplotlib.pyplot as plt

    fig = deserialize_from_json_file("test_plot.json")
    plt.show()

Hint for Jupyter Notebook users: Calling plt.show is unneccessary as the deserialize_from_json_file function returns a figure which gets automatically rendered!




