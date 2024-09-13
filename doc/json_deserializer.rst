JSON Deserializer to Matplotlib
===============================
We deserialize the JSON file created above as follows:

.. code-block:: python

    from plot_serializer.matplotlib.deserializer import deserialize_from_json_file
    from matplotlib.pyplot as plt

    fig = deserialize_from_json_file("test_plot.json")
    plt.show()

Hint for Jupyter Notebook users: Calling plt.show is unneccessary as the deserialize_from_json_file function returns a figure which gets automatically rendered!

