from typing import (
    Any,
    Dict,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Union,
    overload,
)

from matplotlib.figure import Figure as MplFigure

from plot_serializer.matplotlib.axesproxy import AxesProxy, AxesProxy3D
from plot_serializer.serializer import Serializer

class MatplotlibSerializer(Serializer):
    # Overload for when subplot_kw is provided, in our case when 3d axes is create
    # as subplot_kw is used for a manner of attributes this only holds for the dimension specification and with other
    # settings falsely flags the type as AxesProxy3D
    @overload
    def subplots(
        self,
        nrows: Literal[1] = 1,
        ncols: Literal[1] = 1,
        *,
        sharex: Union[bool, Literal["none", "all", "row", "col"]] = False,
        sharey: Union[bool, Literal["none", "all", "row", "col"]] = False,
        squeeze: bool = True,
        width_ratios: Optional[Sequence[float]] = None,
        height_ratios: Optional[Sequence[float]] = None,
        subplot_kw: Dict[str, Any],
        gridspec_kw: Optional[Dict[str, Any]] = None,
        **fig_kw: Any,
    ) -> Tuple[MplFigure, AxesProxy3D]: ...
    @overload
    def subplots(
        self,
        nrows: Literal[1] = 1,
        ncols: Literal[1] = 1,
        *,
        sharex: Union[bool, Literal["none", "all", "row", "col"]] = False,
        sharey: Union[bool, Literal["none", "all", "row", "col"]] = False,
        squeeze: bool = True,
        width_ratios: Optional[Sequence[float]] = None,
        height_ratios: Optional[Sequence[float]] = None,
        subplot_kw: Optional[Dict[str, Any]] = None,
        gridspec_kw: Optional[Dict[str, Any]] = None,
        **fig_kw: Any,
    ) -> Tuple[MplFigure, AxesProxy]: ...
    @overload
    def subplots(
        self,
        nrows: int = 1,
        ncols: int = 1,
        *,
        sharex: Union[bool, Literal["none", "all", "row", "col"]] = False,
        sharey: Union[bool, Literal["none", "all", "row", "col"]] = False,
        squeeze: bool = True,
        width_ratios: Optional[Sequence[float]] = None,
        height_ratios: Optional[Sequence[float]] = None,
        subplot_kw: Optional[Dict[str, Any]] = None,
        gridspec_kw: Optional[Dict[str, Any]] = None,
        **fig_kw: Any,
    ) -> Tuple[MplFigure, Any]: ...
    def show(self, *, block: Optional[bool] = None) -> None: ...
