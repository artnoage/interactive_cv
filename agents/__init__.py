"""
Agents for the Interactive CV project

This package contains specialized agents for analyzing and extracting information:
- academic_analyzer: Analyzes papers following the How_to_analyze.md methodology
- academic_metadata_extractor: Extracts metadata from paper analyses to JSON
- chronicle_metadata_extractor: Extracts metadata from personal notes to JSON
"""

# Import only available modules
try:
    from .academic_analyzer import PaperAnalysis, AcademicAnalyzer
    __all__ = ['PaperAnalysis', 'AcademicAnalyzer']
except ImportError:
    __all__ = []

# Note: extractor.py uses blueprint_loader which is legacy
# Only import if needed for specific database building operations

try:
    from .entity_deduplicator import *
except ImportError:
    pass