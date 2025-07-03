"""
Metadata extractors for the Interactive CV system.

Uses normalized database schema with:
- Unified relationships table
- Enhanced entity tables with attributes  
- Pre-computed graph structures
- No redundant data storage
"""

from .base import BaseExtractor
from .chronicle import ChronicleExtractor
from .academic import AcademicExtractor

__all__ = [
    'BaseExtractor',
    'ChronicleExtractor', 
    'AcademicExtractor'
]