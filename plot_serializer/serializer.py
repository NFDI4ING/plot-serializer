import logging
import math
import sys
from pathlib import Path
from typing import Any, Callable, List, Mapping, Optional, TextIO, Union

from rocrate.rocrate import ROCrate  # type: ignore[import-untyped]

from plot_serializer.model import (
    BarTrace2D,
    BoxTrace2D,
    ErrorBar2DTrace,
    ErrorPoint2D,
    Figure,
    HistogramTrace,
    LineTrace2D,
    LineTrace3D,
    PiePlot,
    Plot3D,
    Point2D,
    Point3D,
    PointTrace,
    PointTraceNoBar,
    ScatterTrace2D,
    ScatterTrace3D,
    SurfaceTrace3D,
    Trace2D,
    Trace3D,
    Xyz,
)

_CURRENT_SPEC = "https://plot-serializer.readthedocs.io/en/latest/static/specification/plot-serializer-0.2.0.json"


class Serializer:
    """
    A Serializer is an object that has a subclass for different libraries
    (e.g. MatplotlibSerializer). The Serializer allows you to use a library like
    you would normally, while collecting all the data you specify inside the plotting
    library and providing methods for serializing that information to json.
    """

    def __init__(self) -> None:
        self._figure = Figure()
        self._collect_actions: List[Callable[[], None]] = []
        self._written_to_file: bool = False
        self._was_collected: bool = False

    def _add_collect_action(self, action: Callable[[], None]) -> None:
        # Internal method to register a function that will be run every time
        # the user accesses the current serializer state.
        self._collect_actions.append(action)

    def _cast_to_datapoint_trace(self, trace: Any) -> PointTrace | None:
        if (
            isinstance(trace, ScatterTrace2D)
            or isinstance(trace, ScatterTrace3D)
            or isinstance(trace, LineTrace2D)
            or isinstance(trace, LineTrace3D)
            or isinstance(trace, SurfaceTrace3D)
            or isinstance(trace, BarTrace2D)
            or isinstance(trace, ErrorBar2DTrace)
        ):
            return trace
        return None

    def _find_traces(
        self,
        traces: List[Trace2D] | List[Trace3D],
        trace_selector: tuple[float, float] | tuple[float, float, float],
        trace_rel_tol: float,
    ) -> List[PointTraceNoBar]:
        result_traces: List[PointTraceNoBar] = []
        for trace in traces:
            datapoint_trace = self._cast_to_datapoint_trace(trace)
            if datapoint_trace is None or isinstance(datapoint_trace, BarTrace2D):
                continue
            else:
                for datapoint in datapoint_trace.datapoints:
                    if isinstance(datapoint, Point2D) or isinstance(datapoint, ErrorPoint2D):
                        if len(trace_selector) != 2:
                            raise ValueError("Length of trace_selector needs to two when dealing with 2D-points")
                        elif math.isclose(datapoint.x, trace_selector[0], rel_tol=trace_rel_tol) and math.isclose(
                            datapoint.y, trace_selector[1], rel_tol=trace_rel_tol
                        ):
                            result_traces.append(datapoint_trace)
                            break
                    elif isinstance(datapoint, Point3D):
                        if len(trace_selector) != 3:
                            raise ValueError("Length of trace_selector needs to three when dealing with 3D-points")
                        elif (
                            math.isclose(datapoint.x, trace_selector[0], rel_tol=trace_rel_tol)
                            and math.isclose(datapoint.y, trace_selector[1], rel_tol=trace_rel_tol)
                            and math.isclose(datapoint.z, trace_selector[2], rel_tol=trace_rel_tol)
                        ):
                            result_traces.append(datapoint_trace)

        return result_traces

    def _find_points(
        self,
        trace: PointTrace,
        point_selector: tuple[float, float] | tuple[float, float, float],
        point_rel_tolerance: float,
    ) -> List[Point2D | ErrorPoint2D | Point3D]:
        result_points: List[Point2D | ErrorPoint2D | Point3D] = []
        if isinstance(trace, BarTrace2D):
            raise ValueError("Code Error, this should not be reached. Its relevance is for Mypy errors.")
        for datapoint in trace.datapoints:
            if isinstance(datapoint, Point2D) or isinstance(datapoint, ErrorPoint2D):
                if len(point_selector) != 2:
                    raise ValueError("Length of point_selector needs to two when dealing with 2D-points")
                elif math.isclose(datapoint.x, point_selector[0], rel_tol=point_rel_tolerance) and math.isclose(
                    datapoint.y, point_selector[1], rel_tol=point_rel_tolerance
                ):
                    result_points.append(datapoint)
            elif isinstance(datapoint, Point3D):
                if len(point_selector) != 3:
                    raise ValueError("Length of point_selector needs to three when dealing with 3D-points")
                elif (
                    math.isclose(datapoint.x, point_selector[0], rel_tol=point_rel_tolerance)
                    and math.isclose(datapoint.y, point_selector[1], rel_tol=point_rel_tolerance)
                    and math.isclose(datapoint.z, point_selector[2], rel_tol=point_rel_tolerance)
                ):
                    result_points.append(datapoint)

        return result_points

    def _update_points_metadata(
        self,
        trace: PointTrace,
        point_selector: int | tuple[float, float] | tuple[float, float, float],
        point_rel_tolerance: float,
        dict: Mapping[str, Union[int, float, str]],
    ) -> int:
        if isinstance(point_selector, int):
            trace.datapoints[point_selector].metadata.update(dict)
            return 1
        else:
            datapoints = self._find_points(trace, point_selector, point_rel_tolerance)
            for datapoint in datapoints:
                datapoint.metadata.update(dict)
            return len(datapoints)

    def check_collected_and_written(self) -> None:
        if self._written_to_file:
            raise NotImplementedError(
                "You have already written your JSON file, added metadata will not be represented in the JSON"
            )
        if not self._was_collected:
            self.serialized_figure()

    def add_custom_metadata_figure(self, dict: Mapping[str, Union[int, float, str]]) -> None:
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

    def add_custom_metadata_plot(
        self,
        dict: Mapping[str, Union[int, float, str]],
        plot_selector: int = 0,
    ) -> None:
        self.check_collected_and_written()

        plot = self._figure.plots[plot_selector]
        plot.metadata.update(dict)

    def add_custom_metadata_axis(
        self,
        dict: Mapping[str, Union[int, float, str]],
        axis: Xyz,
        plot_selector: int = 0,
    ) -> None:
        self.check_collected_and_written()

        plot = self._figure.plots[plot_selector]
        if isinstance(plot, PiePlot):
            raise ValueError("PiePlot has no axis to which metadata can be added")
        elif not isinstance(plot, Plot3D) and axis == "z":
            raise ValueError("cannot modify z axis, only x and y axis found, plot is not 3D")
        elif isinstance(plot, Plot3D) and axis == "z":
            plot.z_axis.metadata.update(dict)
        elif axis == "x":
            plot.x_axis.metadata.update(dict)
        elif axis == "y":
            plot.y_axis.metadata.update(dict)

    def add_custom_metadata_trace(
        self,
        dict: Mapping[str, Union[int, float, str]],
        plot_selector: int = 0,
        trace_selector: int | tuple[float, float] | tuple[float, float, float] = 0,
        trace_rel_tol: float = 0.000000001,
    ) -> None:
        self.check_collected_and_written()

        plot = self._figure.plots[plot_selector]
        count_traces_changed: int = 0
        if isinstance(plot, PiePlot):
            raise NotImplementedError(
                "Pieplot does not have any traces to add metadata to."
                + "Try add_custom_metadata_datapoints for adding metadata to slices"
            )
        else:
            if isinstance(trace_selector, int):
                trace = plot.traces[trace_selector]
                trace.metadata.update(dict)
                count_traces_changed += 1
            else:
                selected_traces = self._find_traces(plot.traces, trace_selector, trace_rel_tol)
                for trace in selected_traces:
                    trace.metadata.update(dict)
                count_traces_changed += len(selected_traces)

        logging.info(f"In total, {count_traces_changed} traces' metadata were updated")

    def add_custom_metadata_datapoints(
        self,
        dict: Mapping[str, Union[int, float, str]],
        point_selector: int | tuple[float, float] | tuple[float, float, float],
        trace_selector: int | tuple[float, float] | tuple[float, float, float],
        point_rel_tolerance: float = 0.000000001,
        plot_selector: int = 0,
        trace_rel_tol: float = sys.float_info.max,
    ) -> None:
        self.check_collected_and_written()

        plot = self._figure.plots[plot_selector]
        count_points_changed: int = 0
        if isinstance(plot, PiePlot):
            if isinstance(point_selector, int):
                plot.slices[point_selector].metadata.update(dict)
                count_points_changed += 1
            else:
                raise ValueError(
                    "Trying to access slices of Pie using tuples, not index."
                    + "Point selection via tuples only viable for real datapoints."
                )
        else:
            if isinstance(trace_selector, int):
                selected_trace = plot.traces[trace_selector]
                if isinstance(selected_trace, BoxTrace2D):
                    if isinstance(point_selector, int):
                        selected_trace.boxes[point_selector].metadata.update(dict)
                        count_points_changed += 1
                    else:
                        raise ValueError(
                            "Can not search for point in boxtrace as values might be strings. Try selecting by index."
                        )
                elif isinstance(selected_trace, HistogramTrace):
                    if isinstance(point_selector, int):
                        selected_trace.datasets[point_selector].metadata.update(dict)
                        count_points_changed += 1
                    else:
                        raise ValueError("Can not search for points in histtrace, try selecting by index")
                else:
                    trace = self._cast_to_datapoint_trace(plot.traces[trace_selector])
                    if trace is None:
                        raise ValueError("Selected Plot has no points! Verify plot- and trace-selector arguments.")
                    elif isinstance(trace, BarTrace2D):
                        if isinstance(point_selector, int):
                            trace.datapoints[point_selector].metadata.update(dict)
                        else:
                            raise ValueError(
                                "Can not search for point in bartrace as values might be strings."
                                + "Try searching by index."
                            )
                    else:
                        count_points_changed += self._update_points_metadata(
                            trace, point_selector, point_rel_tolerance, dict
                        )
            else:
                selected_traces = self._find_traces(plot.traces, trace_selector, trace_rel_tol)
                for trace in selected_traces:
                    count_points_changed += self._update_points_metadata(
                        trace, point_selector, point_rel_tolerance, dict
                    )
        logging.info(f"In total, {count_points_changed} datapoints' metadata were updated")

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
        if not self._was_collected:
            for collect_action in self._collect_actions:
                collect_action()
            self._was_collected = True
        else:
            raise NotImplementedError(
                "Attempted to convert the Plot two times into JSON." + "Check doubling of Serializer function calls"
            )

        return self._figure.model_copy(deep=True)

    def to_json(self, *, emit_warnings: bool = True) -> str:
        """
        Returns the data that has been collected so far as a json-encoded string.

        Args:
            emit_warnings (bool): If set to True (default), warnings about missing graph properties will be logged

        Returns:
            str: Json string
        """
        if not self._was_collected:
            self.serialized_figure()

        if emit_warnings:
            self._figure.emit_warnings()

        return self._figure.model_dump_json(indent=2, exclude_defaults=True)

    def write_json_file(self, file: Union[TextIO, str], *, emit_warnings: bool = True) -> None:
        """
        Writes the collected data as json to a file on disk.

        Args:
            file (Union[TextIO, str]): Either a filepath as string or a TextIO object
            emit_warnings (bool): If set to True (default), warnings about missing graph properties will be logged
        """
        if self._written_to_file:
            raise NotImplementedError("You can only write the figure into the JSON once! Multiple tries were attempted")
        if isinstance(file, str):
            with open(file, "w") as file:
                self.write_json_file(file)
        else:
            file.write(self.to_json(emit_warnings=emit_warnings))
            self._written_to_file = True
