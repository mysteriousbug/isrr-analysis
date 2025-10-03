"""
Logic Package
Contains all business logic modules for ISRR analysis
"""

from .data_loader import DataLoader
from .variable_analyzer import VariableAnalyzer
from .interim_isrr_calculator import InterimISRRCalculator
from .final_isrr_calculator import FinalISRRCalculator
from .comparator import ISRRComparator

__all__ = [
    'DataLoader',
    'VariableAnalyzer',
    'InterimISRRCalculator',
    'FinalISRRCalculator',
    'ISRRComparator'
]

__version__ = '2.0.0'
