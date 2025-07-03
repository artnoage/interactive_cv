"""
Agents for the Interactive CV project

This package contains specialized agents for analyzing and extracting information:
- academic_analyzer: Analyzes papers following the How_to_analyze.md methodology
- academic_extractor: Extracts entities and relationships from paper analyses
- chronicle_extractor: Extracts metadata from daily, weekly, and monthly notes
"""

from .chronicle_extractor import SimpleChronicleMetadata, SimpleMetadataExtractor
from .academic_extractor import AcademicMetadata, AcademicExtractor
from .academic_analyzer import PaperAnalysis, AcademicAnalyzer

__all__ = [
    'SimpleChronicleMetadata',
    'SimpleMetadataExtractor', 
    'AcademicMetadata',
    'AcademicExtractor',
    'PaperAnalysis',
    'AcademicAnalyzer'
]