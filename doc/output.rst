Serialization Output
====================
Serializing to JSON
-------------------
The JSON string can be accessed via the ``to_json()``-Method on the serializer or written to a file via the ``write_json_file()``-Method.

.. code-block:: python

    serializer.to_json()
    serializer.write_json_file("test_plot.json")

Writing to paths is also supported, with directories being created if they do not exist.

.. code-block:: python

    serializer.write_json_file("some_dir/test_plot.json")

Serializing to RO-Crate
-----------------------
PloSe allows you to store your plot as an `RO-Crate <https://www.researchobject.org/ro-crate/>`_.
You can do so using the ``add_to_ro_crate()`` method.
Let's say we want to save our example plot as ``"my-plot"`` in an RO-crate called ``"my-rocrate"``:

.. code-block:: python

    serializer.add_to_ro_crate("my-rocrate", "my-plot")

This will create a folder called ``my-rocrate`` containing the json file ``"my-plot"`` representing the plot, 
together with the RO-crate metadata file ``"ro-crate-metadata.json"``, the core piece of an RO-crate that looks like this:

.. code-block:: json
    
    {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@graph": [
            {
                "@id": "./",
                "@type": "Dataset",
                "datePublished": "2024-09-16T16:34:34+00:00",
                "hasPart": [
                    {
                        "@id": "my-plot.json"
                    }
                ]
            },
            {
                "@id": "ro-crate-metadata.json",
                "@type": "CreativeWork",
                "about": {
                    "@id": "./"
                },
                "conformsTo": {
                    "@id": "https://w3id.org/ro/crate/1.1"
                }
            },
            {
                "@id": "my-plot.json",
                "@type": "File",
                "conformsTo": {
                    "@id": "https://plot-serializer.readthedocs.io/en/latest/static/specification/plot-serializer-0.2.0.json"
                },
                "encodingFormat": "application/json",
                "name": "my-plot"
            }
        ]
    }