# -*- coding: utf-8 -*-
"""
GitHerd — Real-time Git branch synchronizer

Keeps multiple Git branches aligned in real-time.
Ideal for parallel AI coding sessions (Claude Code, Cursor, etc.)
or any workflow with multiple active branches.

Copyright (c) 2026 InZeMobile
Licensed under the MIT License. See LICENSE file for details.

https://github.com/Jacques66/GitHerd
"""

from .config import apply_theme_settings
from .app import App


def main():
    """Main entry point for GitHerd."""
    apply_theme_settings()
    App().mainloop()


__all__ = ["main", "App"]
__version__ = "1.0.0"
