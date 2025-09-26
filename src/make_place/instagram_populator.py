#!/usr/bin/env python3
"""
Instagram populator for PlaceData.

This module contains the InstagramPopulator class that populates PlaceData
with information extracted from Instagram profiles.
"""

import sys
import os
from typing import Optional

# Add the instagram_place_parser to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'instagram_place_parser'))

from place_fetcher import fetch_profile_with_curl, extract_username_from_input
from place_data_parser import parse_profile_data
from place_data import PlaceData


class InstagramPopulator:
    """
    Populator class that extracts place information from Instagram profiles.
    """
    
    def __init__(self):
        self.name = "Instagram"
    
    def populate_from_args(self, place_data: PlaceData, input_string: str) -> bool:
        """
        Populate instagram_url from input string if it's an Instagram link.
        
        Args:
            place_data: PlaceData instance to populate
            input_string: Input string that might contain Instagram URL
            
        Returns:
            bool: True if instagram_url was set, False otherwise
        """
        if not input_string:
            return False
        
        # Check if it's an Instagram URL
        if 'instagram.com' in input_string.lower():
            try:
                # Extract username from the input
                username = extract_username_from_input(input_string)
                if username:
                    place_data.instagram_url = f"https://www.instagram.com/{username}/"
                    place_data.instagram_handle = username
                    return True
            except ValueError:
                pass
        
        return False
    
    def can_populate(self, place_data: PlaceData) -> bool:
        """
        Check if this populator can populate data (either instagram_url or instagram_handle is set).
        
        Args:
            place_data: PlaceData instance to check
            
        Returns:
            bool: True if can populate, False otherwise
        """
        # Can populate if we have either instagram_url or instagram_handle
        return bool(place_data.instagram_url or place_data.instagram_handle)
    
    def populate(self, place_data: PlaceData) -> bool:
        """
        Populate place data from Instagram profile.
        
        Args:
            place_data: PlaceData instance to populate
            
        Returns:
            bool: True if population was successful, False otherwise
        """
        if not self.can_populate(place_data):
            return False
        
        try:
            # Determine which field to use and set the other one
            if place_data.instagram_handle:
                handle = place_data.instagram_handle
                if not place_data.instagram_url:
                    place_data.instagram_url = f"https://www.instagram.com/{handle}/"
            elif place_data.instagram_url:
                # Extract handle from URL
                try:
                    handle = extract_username_from_input(place_data.instagram_url)
                    place_data.instagram_handle = handle
                except ValueError:
                    print(f"❌ Error extracting handle from URL: {place_data.instagram_url}")
                    return False
            else:
                return False
            
            # Fetch profile data from Instagram
            profile_data = fetch_profile_with_curl(handle)
            
            # Check for errors
            if 'error' in profile_data:
                print(f"❌ Error fetching Instagram profile: {profile_data['error']}")
                return False
            
            # Parse the profile data
            parsed_data = parse_profile_data(profile_data)
            
            # Update place_data with parsed information (only if current data is None)
            if not place_data.place_name and parsed_data.get('place_name'):
                place_data.place_name = parsed_data['place_name']
            
            if not place_data.wolt_url and parsed_data.get('wolt_url'):
                place_data.wolt_url = parsed_data['wolt_url']
            
            if not place_data.google_maps and parsed_data.get('google_maps'):
                place_data.google_maps = parsed_data['google_maps']
            
            if not place_data.website_url and parsed_data.get('website_url'):
                place_data.website_url = parsed_data['website_url']
            
            if not place_data.telegram_link and parsed_data.get('telegram_link'):
                place_data.telegram_link = parsed_data['telegram_link']
            
            if not place_data.address_text and parsed_data.get('address_text'):
                place_data.address_text = parsed_data['address_text']
            
            return True
            
        except Exception as e:
            print(f"❌ Error populating from Instagram: {e}")
            return False
