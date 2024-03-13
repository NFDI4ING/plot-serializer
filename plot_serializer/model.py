from typing import Annotated, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field

import logging


# --------------------
#  General classes


Scale = Union[Literal["linear"], Literal["logarithmic"]]


class Axis(BaseModel):
    label: Optional[str] = None
    scale: Optional[Scale] = None  # Defaults to linear

    def emit_warnings(self) -> None:
        msg = []

        if self.label is None or len(self.label.lstrip()) == 0:
            msg.append("label")

        if len(msg) > 0:
            logging.warning("%s is not set for Axis object.", msg)


MetadataValue = Union[int, float, str]
Metadata = Dict[str, MetadataValue]


# --------------------
#  2D Plot


class Point2D(BaseModel):
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
    label: Optional[str]
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
    label: Optional[str]
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
    line_color: Optional[str] = None
    line_thickness: Optional[float] = None
    line_style: Optional[str] = None
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


class Bar2D(BaseModel):
    y: float
    label: str
    color: Optional[str] = None

    def emit_warnings(self) -> None:
        # TODO: Switch to a better warning system
        msg: List[str] = []

        if len(msg) > 0:
            logging.warning("%s is not set for Bar2D.", msg)


class BarTrace2D(BaseModel):
    type: Literal["bar"]
    datapoints: List[Bar2D]

    def emit_warnings(self) -> None:
        for datapoint in self.datapoints:
            datapoint.emit_warnings()


Trace2D = Annotated[
    Union[ScatterTrace2D, LineTrace2D, BarTrace2D], Field(discriminator="type")
]

Trace3D = Annotated[Union[ScatterTrace3D], Field(discriminator="type")]


class Plot2D(BaseModel):
    type: Literal["2d"]
    title: Optional[str] = None
    x_axis: Axis
    y_axis: Axis
    traces: List[Trace2D]

    def emit_warnings(self) -> None:
        msg = []

        if self.title is None or len(self.title.lstrip()) == 0:
            msg.append("title")

        if len(msg) > 0:
            logging.warning("%s is not set for Plot2D.", msg)

        self.x_axis.emit_warnings()
        self.y_axis.emit_warnings()

        for trace in self.traces:
            trace.emit_warnings()


class Plot3D(BaseModel):
    type: Literal["3d"]
    title: Optional[str] = None
    x_axis: Axis
    y_axis: Axis
    z_axis: Axis
    traces: List[Trace3D]

    def emit_warnings(self) -> None:
        msg = []

        if self.title is None or len(self.title.lstrip()) == 0:
            msg.append("title")

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
    size: float
    radius: Optional[float] = None
    offset: Optional[float] = None
    name: Optional[str] = None
    color: Optional[str] = None

    def emit_warnings(self) -> None:
        msg = []

        if self.name is None or len(self.name.lstrip()) == 0:
            msg.append("name")

        if len(msg) > 0:
            logging.warning("%s is not set for Slice object.", msg)


class PiePlot(BaseModel):
    type: Literal["pie"]
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
    plots: List[Plot] = []
    metadata: Metadata = {}

    def emit_warnings(self) -> None:
        msg = []

        if self.plots is None or len(self.plots) == 0:
            msg.append("plots")

        if len(msg) > 0:
            logging.warning("%s is not set for Figure object.", msg)

        for plot in self.plots:
            plot.emit_warnings()
