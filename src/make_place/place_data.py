#!/usr/bin/env python3
"""
PlaceData class for representing Instagram place information.

This module contains the PlaceData dataclass that represents all the information
extracted from an Instagram profile for a place.
"""

from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass
class PlaceData:
    """
    Data class representing place information extracted from various sources.
    """
    instagram_handle: Optional[str] = None
    instagram_url: Optional[str] = None
    extracted_at: str = None
    place_name: Optional[str] = None
    wolt_url: Optional[str] = None
    google_maps: Optional[str] = None
    website_url: Optional[str] = None
    telegram_link: Optional[str] = None
    address_text: Optional[str] = None
    
    def __post_init__(self):
        """Set extracted_at if not provided."""
        if self.extracted_at is None:
            self.extracted_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """
        Convert PlaceData to dictionary.
        
        Returns:
            Dictionary representation of PlaceData
        """
        return asdict(self)
    
    def get_display_name(self) -> str:
        """
        Get display name for the place (place_name or instagram_handle).
        
        Returns:
            Display name string
        """
        return self.place_name or self.instagram_handle
