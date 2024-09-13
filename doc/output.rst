Serialization Output
====================
Serializing to JSON
-------------------
The JSON string can be accessed via the ``to_json()``-Method on the serializer or written to a file via the ``write_json_file()``-Method.

.. code-block:: python

    serializer.to_json()
    serializer.write_json_file("test_plot.json")

Serializing to RO-Crate
-----------------------
PlotSerializer is able to integrate with `RO-Crates <https://www.researchobject.org/ro-crate/>`_.
This means that you can add the serialized diagrams to an RO-Crate as a file with appropriate metadata.
You can accomplish this through the ``add_to_ro_crate()``-Method.
The first argument is the file path to the ro-crate directory and the second argument is the location where the file should be placed within the crate.
When the specified RO-Crate does not exist, a new one is created (this can also be controlled through the ``create`` parameter).
PlotSerializer will try to figure out an appropriate name for the object, but can also be explicitly specified with the ``name`` parameter.