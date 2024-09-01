


Deserializer
---------------------------------

PlotSerializer also provides the functionality of converting the JSON file back into a diagram.
Only serialized attributes can influence the deserialized plot,
the created graph might thus look slightly different from the original, the data however will remain unchanged.

We deserialize the JSON file created above as follows:

.. code-block:: python

    from plot_serializer.matplotlib.deserializer import deserialize_from_json_file
    from matplotlib.pyplot as plt

    fig = deserialize_from_json_file("test_plot.json")
    plt.show()

Hint for Jupyter Notebook users: Calling plt.show is unneccessary as the deserialize_from_json_file function returns a figure which gets automatically rendered!

Serializer -> JSON/RO Export -> Deserializer

RO-Crates
---------------------------------

PlotSerializer is able to integrate with `RO-Crates <https://www.researchobject.org/ro-crate/>`_.
This means that you can add the serialized diagrams to an RO-Crate as a file with appropriate metadata.
You can accomplish this through the ``add_to_ro_crate()``-Method.
The first argument is the file path to the ro-crate directory and the second argument is the location where the file should be placed within the crate.
When the specified RO-Crate does not exist, a new one is created (this can also be controlled through the ``create`` parameter).
PlotSerializer will try to figure out an appropriate name for the object, but can also be explicitly specified with the ``name`` parameter.




