"""
A project template for the sdPy effort..
"""

__version__: str = "1.0.0"

from .tdms import read_tdms, write_tdms


__all__ = ["__version__", "read_tdms", "write_tdms"]
