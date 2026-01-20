"""
MCP Space Life Sciences Knowledge Graph Integration

Integrates GeneLab, PrimeKG, and SPOKE-OKN knowledge graphs for 
comprehensive space life sciences research.
"""

__version__ = "0.1.0"
__author__ = "MCP Space Life Sciences Contributors"

from .client import IntegratedKGClient

__all__ = ["IntegratedKGClient", "__version__"]
