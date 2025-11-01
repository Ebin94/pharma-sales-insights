"""Utility functions for the Pharma Sales Insights project.

This module contains small helper functions that are used across
the ETL pipeline and notebooks. Keeping these utilities in a
separate module allows for reuse and simplifies testing.
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt

def save_figure(fig, path: str | Path) -> None:
    """Save a matplotlib figure to disk, creating parent directories if needed.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure object to save.
    path : str or pathlib.Path
        Destination file path. Relative paths are resolved from the
        repository root when running scripts in the project root.
    """
    # Convert to Path and ensure parent directories exist
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, bbox_inches="tight")
