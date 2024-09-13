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

from matplotlib.axes import Axes as MplAxes
from matplotlib.figure import Figure as MplFigure

from plot_serializer.serializer import Serializer

class MatplotlibSerializer(Serializer):
    # Fancy way of properly type hinting the subplots method...
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
        subplot_kw: None = None,
        gridspec_kw: Optional[Dict[str, Any]] = None,
        **fig_kw: Any,
    ) -> Tuple[MplFigure, MplAxes]: ...
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
