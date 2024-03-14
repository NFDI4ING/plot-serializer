Overview
========

Why PlotSerializer?
---------------------------------
PlotSerializer helps researchers and scientists of all kinds to store research data cleanly.
Specifically, the aim is to convert raw data published for graphs within published in scientific publications into a machine-readable format as easily as possible.
In the case of a scientific paper, for example, the data can be published directly together with the paper so that it can be used later by other researchers.
In a broader sense, this also contributes to the prevention of studies that cannot be reproduced, keyword: reproducibility crisis.
Access to the raw data of research enables scientists who want to build on existing work a much deeper insight into the original facts.


How PlotSerializer sees diagrams
---------------------------------

PlotSerializer uses its own data model for representing scientific diagrams.
The base class for this data model is ``plot_serializer.model.Figure``.
A full Json-Schema for this model is available in this documentation as well.

The basics are illustrated by the following diagram:

.. image:: static/data_structure.svg
  :width: 800
  :alt: PlotSerializer data structure
