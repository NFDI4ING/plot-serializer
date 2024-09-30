# Overview
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

[[_TOC_]]

## Installation
Install PlotSerializer by running

```cmd
pip install plot-serializer
```

## Documentation

View Plot Serializer's documentation on [Read the Docs](https://plot-serializer.readthedocs.io/en/latest/)

## License
View used License on [Show License](https://plot-serializer.readthedocs.io/en/latest/license.html)

## Citing
Plot Serializer comes with a citation file: [CITATION.cff](https://git.rwth-aachen.de/rdm-tools/plot-serializer/-/blob/main/CITATION.cff).
Find out how to use it [here](https://book.the-turing-way.org/communication/citable/citable-cff.html#how-to-cite-using-citation-cff>).
<br>
Please cite:
Leštáková, M., & Xia, N. (2024, September 18). Plot Serializer. NFDI4ing Conference 2024, virtual. Zenodo. https://doi.org/10.5281/zenodo.13785916

## Acknowledgements
The Authors would like to thank the Federal Government and the Heads of Government of the Länder,
as well as the Joint Science Conference (GWK), for their funding and support within the framework
of the NFDI4Ing consortium. Funded by the German Research Foundation (DFG) - project number 442146713.

Many thanks to the contributors listed in [CONTRIBUTORS.md](https://git.rwth-aachen.de/rdm-tools/plot-serializer/-/blob/main/CONTRIBUTORS.md).

## Contributing
An introduction and rules for contributing can be found in [CONTRIBUTING.md](https://git.rwth-aachen.de/rdm-tools/plot-serializer/-/blob/main/CONTRIBUTING.md).
