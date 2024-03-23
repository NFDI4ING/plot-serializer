from pathlib import Path
from typing import Callable, List, Optional, TextIO, Union
from plot_serializer.model import Figure, Metadata
from rocrate.rocrate import ROCrate  # type: ignore[import-untyped]
from abc import ABC


_CURRENT_SPEC = "https://plot-serializer.readthedocs.io/en/latest/static/specification/plot-serializer-0.2.0.json"


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

    def add_to_ro_crate(
        self,
        crate_path: Union[str, Path],
        file_path: str,
        *,
        create: bool = True,
        name: Optional[str] = None,
    ) -> None:
        """
        Adds the figure from this serializer to the specified ro-crate as a json file.
        If the specified ro-crate does not exist, by default, a new one will be created.

        If no name is explicitly specified, the name of the figure is used instead.
        If the figure has no name, the name of the file specified in file path is used.

        Args:
            crate_path (Union[str, Path]): Path to the root folder of the ro-crate.
            file_path (str): File path within the ro-crate where the file is placed
                             (excluding the path to the ro-crate itself).
            create (bool): Whether to create the ro-crate if it doesn't exist. Defaults to True.
            name (Optional[str], optional): Name of the ro-crate. Defaults to None.
        """

        _temporary_file_name = "_temporary_plotserializer_output.json"
        crate_path = Path(crate_path)

        if not file_path.endswith(".json"):
            file_path += ".json"

        if name is None:
            name = self.serialized_figure().title

        if name is None:
            name = Path(file_path).stem

        # Load crate
        if create:
            crate_path.mkdir(parents=True, exist_ok=True)

            try:
                crate = ROCrate(crate_path)
            except ValueError:
                crate = ROCrate(crate_path, init=True)
        else:
            crate = ROCrate(crate_path)

        try:
            # Write temporary json file
            self.write_json_file(_temporary_file_name)

            # Add file to rocrate
            crate.add_file(
                source=_temporary_file_name,
                dest_path=file_path,
                properties={
                    "name": name,
                    "encodingFormat": "application/json",
                    "conformsTo": {
                        "@id": _CURRENT_SPEC,
                    },
                },
            )

            # Write the changed crate
            crate.write(crate_path)
        finally:
            # Remove temporary file
            Path(_temporary_file_name).unlink()

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
