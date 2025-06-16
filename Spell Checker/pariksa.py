"""
Pariksa - A professional spell checker for Melayu (Ambon) language.

This code was made by Abdul Wahid Rukua - 2025
Licensed under MIT License
GitHub: https://github.com/Airukua/Pariksa
Email: your.email@example.com

This module provides spell checking functionality with support for multiple
dictionary formats and comprehensive error handling.
"""

import os
import json
import logging
from typing import Set, Optional, Union, List, Dict, Tuple
from pathlib import Path
import difflib
from functools import lru_cache

class Pariksa:
    """
    Advanced spell checker for Melayu (Ambon) language with comprehensive features.
    
    This code was made by Abdul Wahid Rukua - 2025
    Licensed under MIT License
    
    Features:
    - Single word and list processing
    - Levenshtein distance calculation
    - Intelligent spell suggestions
    - Case sensitivity options
    - Advanced error handling
    - Comprehensive logging
    - Multiple configuration options
    """

    SUPORTED_EXTENSIONS = {'.txt', '.json'}
    DEFAULT_ENCODING = 'utf-8'
    DEFAULT_DICTIONARY = 'Spellcheck/data/Melayu_Ambon_Wordlist.txt'
    DEFAULT_MAX_SUGGESTIONS = 3
    DEFAULT_MAX_DISTANCE = 2

    def __init__(self, 
                 input_data: Union[str, List[str]], 
                 dictionary_path: Union[str, Path] = 'Spellcheck/data/Melayu_Ambon_Wordlist.txt',
                 case_sensitive: bool = False,
                 max_suggestions: int = DEFAULT_MAX_SUGGESTIONS,
                 max_distance: int = DEFAULT_MAX_DISTANCE,
                 enable_fuzzy_matching: bool = True,
                 logger: Optional[logging.Logger] = None,
                 log_level: int = logging.WARNING):
        
        """
        Initialize the advanced Pariksa spell checker.
        
        Args:
            input_data (Union[str, List[str]]): Word or list of words to check
            dictionary_path (Union[str, Path]): Path to dictionary file
            case_sensitive (bool): Whether to perform case-sensitive checking
            max_suggestions (int): Maximum number of suggestions to return
            max_distance (int): Maximum Levenshtein distance for suggestions
            enable_fuzzy_matching (bool): Enable fuzzy matching for suggestions
            logger (Optional[logging.Logger]): Custom logger instance
            log_level (int): Logging level
        """

        self._validate_input(input_data)
        self._validate_configuration(max_suggestions, max_distance)


    def _validate_input(self, input_data: Union[str, List[str]]) -> None:
        """
        Validates the input data for spellchecking.
        Parameters:
            input_data (Union[str, List[str]]): The input to validate, which can be a single string or a list of strings.
        Raises:
            ValueError: If the input data is empty, not a string or list of strings, contains empty or whitespace-only strings,
                        contains strings longer than 50 characters, or if a list contains more than 1000 items.
        Notes:
            - For string input, ensures it is non-empty, not just whitespace, and no longer than 50 characters.
            - For list input, ensures all elements are non-empty strings, each no longer than 50 characters, and the list contains at most 1000 items.
        """
        if not input_data:
            raise ValueError("Input data cannot be empty")
        
        if isinstance(input_data, str):
            if not input_data.strip():
                raise ValueError("Word cannot be empty or just whitespace")
            if len(input_data.strip()) > 50:
                raise ValueError("Word is too long (max 50 characters)")
        elif isinstance(input_data, list):
            if len(input_data) > 1000:
                raise ValueError("Too many words (max 1000)")
            if not all(isinstance(word, str) and word.strip() for word in input_data):
                raise ValueError("All words must be non-empty strings")
            if any(len(word.strip()) > 50 for word in input_data):
                raise ValueError("Some words are too long (max 50 characters)")
        else:
            raise ValueError("Input must be a string or list of strings")
    
    def _validate_configuration(self, max_suggestions: int, max_distance: int) -> None:
        """
        Validates the configuration parameters for spellchecking.

        Ensures that the provided values for `max_suggestions` and `max_distance` are within acceptable ranges.
        Raises a ValueError if any parameter is out of bounds.

        Parameters:
            max_suggestions (int): The maximum number of suggestions to return. Must be between 0 and 10.
            max_distance (int): The maximum allowed edit distance for suggestions. Must be between 1 and 5.

        Raises:
            ValueError: If `max_suggestions` is not between 0 and 10, or if `max_distance` is not between 1 and 5.
        """
        if max_suggestions < 0 or max_suggestions > 10:
            raise ValueError("max_suggestions must be between 0 and 10")
        if max_distance < 1 or max_distance > 5:
            raise ValueError("max_distance must be between 1 and 5")
