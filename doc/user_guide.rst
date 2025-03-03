User Guide
==========
Plot Serializer (PloSe) is a tool for converting scientific diagrams into (FAIR) data.

Many scientific publications are based on data. To fight the reproducibility crisis in science, 
many researchers are adopting the practice of sharing data. This is more and more often required 
by journals, conferences and funding bodies.

The PloSe team considers scientific diagrams an entry point to the research objects behind a publication.
Typically, the data depicted in a diagram within a scientific publication is of great interest to the reader. 
The diagrams sometimes contain experimental or simulation results, in other cases secondary, processed data.
PloSe enables to quickly extract the data from the diagram, describe it with customizable metadata 
(which can, for example, link to the primary dataset) and share it with the scientific community. 
Hence, PloSe can assist you in making your data FAIR!

PloSe currently allows for serialization from matplotlib to JSON and RO-Crate. It is still **under development**, limited to certain 
plot types. 

PloSe also allows for deserialization of JSON-ized plots into matplotlib.


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Introduction

   overview
   diagrams
   installation
   getting_started

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Serializing Diagrams with PloSe

   howitworks
   supported_plots
   custom_metadata
   plotID
   3d_serializing
   output

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Deserializing with PloSe

   deserializer
   json_deserializer

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Backmatter

   license
   acknowledgement
   citing
