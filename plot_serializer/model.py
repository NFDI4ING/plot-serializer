import logging
from typing import Annotated, Any, Dict, List, Literal, Optional, Tuple, Union

from pydantic import BaseModel, Field, model_validator

# --------------------
#  General classes


Scale = Union[Literal["linear"], Literal["logarithmic"]]

MetadataValue = Union[int, float, str]
Metadata = Dict[str, MetadataValue]

Color = Optional[str | Tuple[float, float, float] | Tuple[float, float, float, float]]

Xyz = Union[Literal["x", "y", "z"]]


class Axis(BaseModel):
    metadata: Metadata = {}
    label: Optional[str] = None
    scale: Optional[Scale] = None  # Defaults to linear
    limit: Optional[Tuple[float, float]] = None

    def emit_warnings(self) -> None:
        msg = []

        if self.label is None or len(self.label.lstrip()) == 0:
            msg.append("label")

        if len(msg) > 0:
            logging.warning("%s is not set for Axis object.", msg)


# --------------------
#  2D Plot


class Point2D(BaseModel):
    metadata: Metadata = {}
    x: float
    y: float
    color: Optional[str] = None
    size: Optional[float] = None

    def emit_warnings(self) -> None:
        msg: List[str] = []
        # TODO: Improve the warning system

        if len(msg) > 0:
            logging.warning("%s is not set for Point2D.", msg)


class Point3D(BaseModel):
    metadata: Metadata = {}
    x: float
    y: float
    z: float
    color: Optional[str] = None
    size: Optional[float] = None

    def emit_warnings(self) -> None:
        msg: List[str] = []
        # TODO: Improve the warning system

        if len(msg) > 0:
            logging.warning("%s is not set for Point3D.", msg)


class ScatterTrace2D(BaseModel):
    type: Literal["scatter"]
    metadata: Metadata = {}
    cmap: Any = None
    norm: Any = None
    label: Optional[str]
    marker: Optional[str]
    datapoints: List[Point2D]

    def emit_warnings(self) -> None:
        msg = []

        if self.label is None or len(self.label.lstrip()) == 0:
            msg.append("label")

        if len(msg) > 0:
            logging.warning("%s is not set for ScatterTrace2D.", msg)

        for datapoint in self.datapoints:
            datapoint.emit_warnings()


class ScatterTrace3D(BaseModel):
    type: Literal["scatter3D"]
    metadata: Metadata = {}
    cmap: Any = None
    norm: Any = None
    label: Optional[str]
    marker: Optional[str]
    datapoints: List[Point3D]

    def emit_warnings(self) -> None:
        msg = []

        if self.label is None or len(self.label.lstrip()) == 0:
            msg.append("label")

        if len(msg) > 0:
            logging.warning("%s is not set for ScatterTrace3D.", msg)

        for datapoint in self.datapoints:
            datapoint.emit_warnings()


class LineTrace2D(BaseModel):
    type: Literal["line"]
    metadata: Metadata = {}
    line_color: Optional[str | Tuple[float, float, float] | Tuple[float, float, float, float]] = None
    line_thickness: Optional[float] = None
    line_style: Optional[str] = None
    marker: Optional[str] = None
    label: Optional[str] = None
    datapoints: List[Point2D]

    def emit_warnings(self) -> None:
        msg = []

        if self.label is None or len(self.label.lstrip()) == 0:
            msg.append("label")

        if len(msg) > 0:
            logging.warning("%s is not set for LineTrace2D.", msg)

        for datapoint in self.datapoints:
            datapoint.emit_warnings()


class LineTrace3D(BaseModel):
    type: Literal["line3D"]
    metadata: Metadata = {}
    line_color: Optional[str | Tuple[float, float, float] | Tuple[float, float, float, float]] = None
    line_thickness: Optional[float] = None
    line_style: Optional[str] = None
    marker: Optional[str] = None
    label: Optional[str] = None
    datapoints: List[Point3D]

    def emit_warnings(self) -> None:
        msg = []

        if self.label is None or len(self.label.lstrip()) == 0:
            msg.append("label")

        for point in self.datapoints:
            point.emit_warnings()

        if len(msg) > 0:
            logging.warning("%s is not set for LineTrace3D.", msg)


class SurfaceTrace3D(BaseModel):
    type: Literal["surface3D"]
    metadata: Metadata = {}
    length: int
    width: int
    label: Optional[str] = None
    datapoints: List[Point3D]

    @model_validator(mode="after")
    def check_dimension_matches_dataponts(self) -> "SurfaceTrace3D":
        if self.length * self.width != len(self.datapoints):
            raise ValueError(
                "The dimensions of the surface must match the number of datapoints (length * width = len(datapoints))!"
            )

        return self

    def emit_warnings(self) -> None:
        msg: List[str] = []

        for point in self.datapoints:
            point.emit_warnings()

        if len(msg) > 0:
            logging.warning("%s is not set for SurfaceTrace3D.", msg)


class Bar2D(BaseModel):
    metadata: Metadata = {}
    y: str | float | int
    label: str | float | int
    color: Optional[str | Tuple[float, float, float] | Tuple[float, float, float, float]] = None

    def emit_warnings(self) -> None:
        # TODO: Switch to a better warning system
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Bar2D.", msg)


class BarTrace2D(BaseModel):
    type: Literal["bar"]
    metadata: Metadata = {}
    datapoints: List[Bar2D]

    def emit_warnings(self) -> None:
        for datapoint in self.datapoints:
            datapoint.emit_warnings()


class Box(BaseModel):
    metadata: Metadata = {}
    data: List[float]
    label: Optional[str] = None
    usermedian: Optional[float] = None
    conf_interval: Optional[Tuple[float, float]] = None

    def emit_warnings(self) -> None:
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Box.", msg)


class BoxTrace2D(BaseModel):
    type: Literal["box"]
    metadata: Metadata = {}
    notch: Optional[bool] = None
    whis: Optional[Union[float, Tuple[float, float]]] = None
    bootstrap: Optional[int] = None
    boxes: List[Box]

    def emit_warnings(self) -> None:
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Box.", msg)

        for box in self.boxes:
            box.emit_warnings()


class ErrorPoint2D(BaseModel):
    metadata: Metadata = {}
    x: float
    y: float
    x_error: Optional[Tuple[float, float]]
    y_error: Optional[Tuple[float, float]]

    def emit_warnings(self) -> None:
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Box.", msg)


class ErrorBar2DTrace(BaseModel):
    type: Literal["errorbar2d"]
    metadata: Metadata = {}
    label: Optional[str] = None
    marker: Optional[str] = None
    color: Optional[Color] = None
    ecolor: Optional[Color] = None
    datapoints: List[ErrorPoint2D]

    def emit_warnings(self) -> None:
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Box.", msg)

        for errorpoint in self.datapoints:
            errorpoint.emit_warnings()


class HistDataset(BaseModel):
    metadata: Metadata = {}
    data: List[float]
    color: Optional[str]
    label: Optional[str]

    def emit_warnings(self) -> None:
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Box.", msg)


class HistogramTrace(BaseModel):
    type: Literal["histogram"]
    metadata: Metadata = {}
    bins: int | List[float] | str
    density: bool
    cumulative: bool
    datasets: List[HistDataset]

    def emit_warnings(self) -> None:
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Box.", msg)

        for dataset in self.datasets:
            dataset.emit_warnings()


Trace2D = Annotated[
    Union[
        ScatterTrace2D,
        LineTrace2D,
        BarTrace2D,
        BoxTrace2D,
        HistogramTrace,
        ErrorBar2DTrace,
    ],
    Field(discriminator="type"),
]


Trace3D = Annotated[Union[ScatterTrace3D, LineTrace3D, SurfaceTrace3D], Field(discriminator="type")]

PointTrace = Union[
    ScatterTrace2D,
    LineTrace2D,
    ScatterTrace3D,
    LineTrace3D,
    BarTrace2D,
    SurfaceTrace3D,
    ErrorBar2DTrace,
]

PointTraceNoBar = Union[
    ScatterTrace2D,
    LineTrace2D,
    ScatterTrace3D,
    LineTrace3D,
    SurfaceTrace3D,
    ErrorBar2DTrace,
]


class Plot2D(BaseModel):
    type: Literal["2d"]
    metadata: Metadata = {}
    title: Optional[str] = None
    x_axis: Axis
    y_axis: Axis
    spines_removed: Optional[List[str]] = None
    traces: List[Trace2D]

    def emit_warnings(self) -> None:
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Plot2D.", msg)

        self.x_axis.emit_warnings()
        self.y_axis.emit_warnings()

        for trace in self.traces:
            trace.emit_warnings()


class Plot3D(BaseModel):
    type: Literal["3d"]
    metadata: Metadata = {}
    title: Optional[str] = None
    x_axis: Axis
    y_axis: Axis
    z_axis: Axis
    traces: List[Trace3D]

    def emit_warnings(self) -> None:
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Plot3D.", msg)

        self.x_axis.emit_warnings()
        self.y_axis.emit_warnings()
        self.z_axis.emit_warnings()

        for trace in self.traces:
            trace.emit_warnings()


# --------------------
#  Pie Plot


class Slice(BaseModel):
    metadata: Metadata = {}
    size: float
    radius: Optional[float] = None
    offset: Optional[float] = None
    name: Optional[str] = None
    color: Optional[str | Tuple[float, float, float] | Tuple[float, float, float, float]] = None

    def emit_warnings(self) -> None:
        msg = []

        if self.name is None or len(self.name.lstrip()) == 0:
            msg.append("name")

        if len(msg) > 0:
            logging.warning("%s is not set for Slice object.", msg)


class PiePlot(BaseModel):
    type: Literal["pie"]
    metadata: Metadata = {}
    title: Optional[str] = None
    slices: List[Slice]

    def emit_warnings(self) -> None:
        msg = []

        if self.title is None or len(self.title.lstrip()) == 0:
            msg.append("title")

        if len(msg) > 0:
            logging.warning("%s is not set for PiePlot object.", msg)

        for slice in self.slices:
            slice.emit_warnings()


# --------------------
#  Figure


Plot = Annotated[Union[PiePlot, Plot2D, Plot3D], Field(discriminator="type")]


class Figure(BaseModel):
    title: Optional[str] = None
    metadata: Metadata = {}
    plots: List[Plot] = []

    def emit_warnings(self) -> None:
        msg = []

        if self.plots is None or len(self.plots) == 0:
            msg.append("plots")

        if len(msg) > 0:
            logging.warning("%s is not set for Figure object.", msg)

        for plot in self.plots:
            plot.emit_warnings()
