#!/usr/bin/env python3
"""
JSON outputter for PlaceData.

This module contains the JsonOutputter class that creates JSON files
from PlaceData instances.
"""

import json
from pathlib import Path
from place_data import PlaceData


class JsonOutputter:
    """
    Outputter class that creates JSON files from PlaceData.
    """
    
    def __init__(self):
        self.name = "JSON"
    
    def can_output(self, place_data: PlaceData) -> bool:
        """
        Check if this outputter can create output (always can).
        
        Args:
            place_data: PlaceData instance to check
            
        Returns:
            bool: True if can output, False otherwise
        """
        return True
    
    def output(self, place_data: PlaceData, output_folder: str) -> bool:
        """
        Create JSON file from PlaceData.
        
        Args:
            place_data: PlaceData instance to output
            output_folder: Path to the output folder
            
        Returns:
            bool: True if output was successful, False otherwise
        """
        try:
            json_path = Path(output_folder) / "place_data.json"
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(place_data.to_dict(), f, indent=2, ensure_ascii=False)
            
            print(f"✅ Created place_data.json in: {json_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating JSON file: {e}")
            return False
