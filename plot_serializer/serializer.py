from typing import Callable, List, TextIO, Union
from plot_serializer.model import Figure, Metadata
from abc import ABC


class Serializer(ABC):
    """
    A Serializer is an object that has a subclass for different libraries
    (e.g. MatplotlibSerializer). The Serializer allows you to use a library like
    you would normally, while collecting all the data you specify inside the plotting
    library and providing methods for serializing that information to json.
    """

    def __init__(self) -> None:
        self._figure = Figure()
        self._collect_actions: List[Callable[[], None]] = []

    def _add_collect_action(self, action: Callable[[], None]) -> None:
        # Internal method to register a function that will be run every time
        # the user accesses the current serializer state.
        self._collect_actions.append(action)

    def add_custom_metadata(self, dict: Metadata) -> None:
        """
        Adds a piece of custom metadata to the generated figure object. All metadata
        for each object is uniquely identified by a name for that piece of metadata.
        If a name that already exists on this object is provided, the previously
        set value will be overridden.

        Args:
            name (str): Unique name of this piece of metadata
            value (MetadataValue): Value that this piece of metadata should have
        """
        self._figure.metadata.update(dict)

    # FIXME: if to_json is used twice or write_to_json the output it producec is wierd, maybe add warning!!!
    def serialized_figure(self) -> Figure:
        """
        Returns a figure object that contains all the data that has been captured
        by this serializer so far. The figure object is guaranteed to not change
        further after it has been returned.

        Returns:
            Figure: Figure object
        """
        for collect_action in self._collect_actions:
            collect_action()

        return self._figure.model_copy(deep=True)

    def to_json(self, *, emit_warnings: bool = True) -> str:
        """
        Returns the data that has been collected so far as a json-encoded string.

        Args:
            emit_warnings (bool): If set to True (default), warnings about missing graph properties will be logged

        Returns:
            str: Json string
        """
        figure = self.serialized_figure()

        if emit_warnings:
            figure.emit_warnings()

        return figure.model_dump_json(indent=2, exclude_defaults=True)

    def write_json_file(
        self, file: Union[TextIO, str], *, emit_warnings: bool = True
    ) -> None:
        """
        Writes the collected data as json to a file on disk.

        Args:
            file (Union[TextIO, str]): Either a filepath as string or a TextIO object
            emit_warnings (bool): If set to True (default), warnings about missing graph properties will be logged
        """
        if isinstance(file, str):
            with open(file, "w") as file:
                self.write_json_file(file)
        else:
            file.write(self.to_json(emit_warnings=emit_warnings))
