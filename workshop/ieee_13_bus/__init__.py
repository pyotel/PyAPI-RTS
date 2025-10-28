"""
IEEE 13 Node Test Feeder Implementation

This package provides a complete implementation of the IEEE 13 bus test system
using the PyAPI-RTS library for RSCAD modeling.

Example:
    >>> from workshop.ieee_13_bus import IEEE13BusBuilder
    >>> builder = IEEE13BusBuilder()
    >>> draft = builder.build()
    >>> draft.write_file("ieee_13_bus.dfx")
"""

from .builder import IEEE13BusBuilder
from . import config

__version__ = "1.0.0"
__all__ = ["IEEE13BusBuilder", "config"]
