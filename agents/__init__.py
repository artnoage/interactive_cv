"""
Agents for the Interactive CV project

This package contains specialized agents for analyzing and extracting information:
- academic_analyzer: Analyzes papers following the How_to_analyze.md methodology
- academic_metadata_extractor: Extracts metadata from paper analyses to JSON
- chronicle_metadata_extractor: Extracts metadata from personal notes to JSON
"""

from .chronicle_metadata_extractor import ChronicleMetadata, ChronicleMetadataExtractor
from .academic_metadata_extractor import AcademicMetadata, AcademicExtractor
from .academic_analyzer import PaperAnalysis, AcademicAnalyzer

__all__ = [
    'ChronicleMetadata',
    'ChronicleMetadataExtractor', 
    'AcademicMetadata',
    'AcademicExtractor',
    'PaperAnalysis',
    'AcademicAnalyzer'
]