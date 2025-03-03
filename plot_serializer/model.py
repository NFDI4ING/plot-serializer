import logging
from typing import Annotated, Any, Dict, List, Literal, Optional, Sequence, Tuple, Union

import numpy as np
from matplotlib.colors import Colormap, Normalize
from matplotlib.scale import ScaleBase
from numpy.typing import ArrayLike
from pydantic import BaseModel, ConfigDict, Field, model_validator

# --------------------
#  General classes


Scale = Union[ScaleBase, str]

Metadata = Dict[Any, Any]

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

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


# --------------------
#  2D Plot


class Point2D(BaseModel):
    metadata: Metadata = {}
    x: Any
    y: Any
    color: Optional[Color] = None
    size: Any = None

    def emit_warnings(self) -> None:
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Point2D.", msg)

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


class Point3D(BaseModel):
    metadata: Metadata = {}
    x: Any
    y: Any
    z: Any
    color: Optional[Color] = None
    size: Any = None

    def emit_warnings(self) -> None:
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Point3D.", msg)

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


class ScatterTrace2D(BaseModel):
    type: Literal["scatter"]
    metadata: Metadata = {}
    cmap: Optional[str | Colormap] = None
    norm: Optional[Normalize | str] = None
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

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


class ScatterTrace3D(BaseModel):
    type: Literal["scatter3D"]
    metadata: Metadata = {}
    cmap: Optional[str | Colormap] = None
    norm: Optional[Normalize | str] = None
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

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


class LineTrace2D(BaseModel):
    type: Literal["line"]
    metadata: Metadata = {}
    color: Optional[Color] = None
    linewidth: Optional[float] = None
    linestyle: Optional[str] = None
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

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


class LineTrace3D(BaseModel):
    type: Literal["line3D"]
    metadata: Metadata = {}
    color: Optional[Color] = None
    linewidth: Optional[float] = None
    linestyle: Optional[str] = None
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

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


class SurfaceTrace3D(BaseModel):
    type: Literal["surface3D"]
    metadata: Metadata = {}
    length: int
    width: int
    label: Optional[str] = None
    datapoints: List[Point3D]

    def emit_warnings(self) -> None:
        msg: List[str] = []

        for point in self.datapoints:
            point.emit_warnings()

        if len(msg) > 0:
            logging.warning("%s is not set for SurfaceTrace3D.", msg)

    @model_validator(mode="after")
    def check_dimension_matches_dataponts(self) -> "SurfaceTrace3D":
        return self

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    def dict(self, *args: Any, **kwargs: Any) -> Any:
        kwargs.setdefault("exclude", set()).update({"length", "width"})
        return super().model_dump(*args, **kwargs)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Bar2D(BaseModel):
    metadata: Metadata = {}
    height: Any
    x_i: Any
    color: Optional[Color] = None

    def emit_warnings(self) -> None:
        # TODO: Switch to a better warning system
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Bar2D.", msg)

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


class BarTrace2D(BaseModel):
    type: Literal["bar"]
    metadata: Metadata = {}
    datapoints: List[Bar2D]

    def emit_warnings(self) -> None:
        for datapoint in self.datapoints:
            datapoint.emit_warnings()

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


class Box(BaseModel):
    metadata: Metadata = {}
    x_i: Any
    tick_label: Any = None
    usermedian: Any = None
    conf_interval: Any = None

    def emit_warnings(self) -> None:
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Box.", msg)

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


class BoxTrace2D(BaseModel):
    type: Literal["box"]
    metadata: Metadata = {}
    notch: Optional[bool] = None
    whis: Optional[float | Tuple[float, float] | ArrayLike] = None
    bootstrap: Optional[int] = None
    x: List[Box]

    def emit_warnings(self) -> None:
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Box.", msg)

        for box in self.x:
            box.emit_warnings()

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


class ErrorPoint2D(BaseModel):
    metadata: Metadata = {}
    x: Any
    y: Any
    xerr: Any
    yerr: Any

    def emit_warnings(self) -> None:
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Box.", msg)

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


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

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


class HistDataset(BaseModel):
    metadata: Metadata = {}
    x_i: Any  # should always be: List[Number], however matplotlib stub does not specify
    color: Optional[str]
    label: Optional[str]

    def emit_warnings(self) -> None:
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Box.", msg)

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


class HistogramTrace(BaseModel):
    type: Literal["histogram"]
    metadata: Metadata = {}
    bins: int | Sequence[Any] | str  # used to be: int | List[float]
    density: bool
    cumulative: bool | Literal[-1]
    x: List[HistDataset]

    def emit_warnings(self) -> None:
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Box.", msg)

        for dataset in self.x:
            dataset.emit_warnings()

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


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

    model_config = {"arbitrary_types_allowed": True}


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

    model_config = {"arbitrary_types_allowed": True}


class Slice(BaseModel):
    metadata: Metadata = {}
    x: float
    explode: Optional[Any] = None
    label: Optional[str] = None
    color: Optional[Color] = None

    def emit_warnings(self) -> None:
        msg = []

        if self.label is None or len(self.label.lstrip()) == 0:
            msg.append("label")

        if len(msg) > 0:
            logging.warning("%s is not set for Slice object.", msg)

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


class PiePlot(BaseModel):
    type: Literal["pie"]
    metadata: Metadata = {}
    title: Optional[str] = None
    radius: Optional[float] = None
    slices: List[Slice]

    def emit_warnings(self) -> None:
        msg = []

        if self.title is None or len(self.title.lstrip()) == 0:
            msg.append("title")

        if len(msg) > 0:
            logging.warning("%s is not set for PiePlot object.", msg)

        for slice in self.slices:
            slice.emit_warnings()

    @model_validator(mode="before")
    def cast_numpy_types(cls: Any, values: Any) -> Any:  # noqa: N805
        def convert(value: Any) -> Any:
            if isinstance(value, np.generic):
                return value.item()
            elif isinstance(value, np.ndarray):
                return value.tolist()
            return value

        return {key: convert(value) for key, value in values.items()}

    model_config = {"arbitrary_types_allowed": True}


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

    model_config = {"arbitrary_types_allowed": True}
