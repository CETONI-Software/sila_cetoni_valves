# Generated by sila2.code_generator; sila2.__version__: 0.8.0
# -----
# This class does not do anything useful at runtime. Its only purpose is to provide type annotations.
# Since sphinx does not support .pyi files (yet?), so this is a .py file.
# -----

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from sila2.client import ClientMetadata, ClientUnobservableProperty


class ValveGatewayServiceClient:
    """
    Provides means to access individual valves of a valve terminal
    """

    NumberOfValves: ClientUnobservableProperty[int]
    """
    The number of valves of a terminal
    """

    ValveIndex: ClientMetadata[int]
    """
    The index of a single valve of a valve terminal. This value is 0-indexed, i.e. the first valve has index 0, the second one index 1 and so on.
    """
