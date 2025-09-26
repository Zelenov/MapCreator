#!/usr/bin/env python3
"""
Test suite for instagram_fetcher.py

This module contains tests for Instagram profile data extraction.
Each test represents one Instagram profile with saved JSON response as input.
"""

import unittest
import json
import sys
import os

# Add the current directory to the path so we can import place_data_parser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from place_data_parser import (
    extract_wolt_url,
    extract_google_maps,
    extract_website_url,
    extract_telegram_link,
    extract_address_text
)


class TestInstagramProfiles(unittest.TestCase):
    """Test cases for Instagram profile data extraction - one test per profile."""
    
    def test_boyar_rs_profile(self):
        """Test extraction for @boyar.rs profile."""
        # Saved JSON response from boyar.rs profile
        profile_data = {
            "data": {
                "user": {
                    "biography": "Pelmeni restaurant in Belgrade",
                    "external_url": "https://pelmeni-belgrade.ru/",
                    "bio_links": [
                        {
                            "url": "https://t.me/PELMENI_RS_BOT",
                            "title": "Telegram Bot"
                        }
                    ],
                    "business_address_json": None
                }
            }
        }
        
        # Extract all data
        wolt_url = extract_wolt_url(profile_data)
        google_maps = extract_google_maps(profile_data)
        website_url = extract_website_url(profile_data)
        telegram_link = extract_telegram_link(profile_data)
        address_text = extract_address_text(profile_data)
        
        # Assert expected outputs
        self.assertIsNone(wolt_url, "boyar.rs should not have Wolt URL")
        self.assertIsNone(google_maps, "boyar.rs should not have Google Maps URL")
        self.assertEqual(website_url, "https://pelmeni-belgrade.ru/", "boyar.rs should have website URL")
        self.assertEqual(telegram_link, "https://t.me/PELMENI_RS_BOT", "boyar.rs should have Telegram link")
        self.assertIsNone(address_text, "boyar.rs should not have address text")
    
    def test_ruske_palacinke_profile(self):
        """Test extraction for @ruske_palacinke profile."""
        # Saved JSON response from ruske_palacinke profile
        profile_data = {
            "data": {
                "user": {
                    "biography": "Russian pancakes in Belgrade",
                    "external_url": "https://wolt.com/sr/srb/belgrade/restaurant/ruske-palainke-2",
                    "bio_links": [
                        {
                            "url": "https://maps.app.goo.gl/X34vVWUyjpevKipX7?g_st=com.google.maps.preview.copy",
                            "title": "Google Maps"
                        }
                    ],
                    "business_address_json": None
                }
            }
        }
        
        # Extract all data
        wolt_url = extract_wolt_url(profile_data)
        google_maps = extract_google_maps(profile_data)
        website_url = extract_website_url(profile_data)
        telegram_link = extract_telegram_link(profile_data)
        address_text = extract_address_text(profile_data)
        
        # Assert expected outputs
        self.assertEqual(wolt_url, "https://wolt.com/sr/srb/belgrade/restaurant/ruske-palainke-2", "ruske_palacinke should have Wolt URL")
        self.assertEqual(google_maps, "https://maps.app.goo.gl/X34vVWUyjpevKipX7?g_st=com.google.maps.preview.copy", "ruske_palacinke should have Google Maps URL")
        self.assertIsNone(website_url, "ruske_palacinke should not have website URL")
        self.assertIsNone(telegram_link, "ruske_palacinke should not have Telegram link")
        self.assertIsNone(address_text, "ruske_palacinke should not have address text")
    
    def test_v_volne_beograd_profile(self):
        """Test extraction for @v_volne.beograd profile."""
        # Saved JSON response from v_volne.beograd profile
        profile_data = {
            "data": {
                "user": {
                    "biography": "VOL°NA bar - craft cocktails",
                    "external_url": "https://t.me/volnabeograd",
                    "bio_links": [],
                    "business_address_json": '{"city_name": "Belgrade, Serbia", "city_id": 109920975697736, "latitude": 44.8131, "longitude": 20.46329, "street_address": "VOL°NA bar", "zip_code": "11103"}'
                }
            }
        }
        
        # Extract all data
        wolt_url = extract_wolt_url(profile_data)
        google_maps = extract_google_maps(profile_data)
        website_url = extract_website_url(profile_data)
        telegram_link = extract_telegram_link(profile_data)
        address_text = extract_address_text(profile_data)
        
        # Assert expected outputs
        self.assertIsNone(wolt_url, "v_volne.beograd should not have Wolt URL")
        self.assertIsNone(google_maps, "v_volne.beograd should not have Google Maps URL")
        self.assertIsNone(website_url, "v_volne.beograd should not have website URL (has Telegram instead)")
        self.assertEqual(telegram_link, "https://t.me/volnabeograd", "v_volne.beograd should have Telegram link")
        self.assertEqual(address_text, "VOL°NA bar, Belgrade, Serbia, 11103", "v_volne.beograd should have address text")
    
    def test_pizzabarserbia_profile(self):
        """Test extraction for @pizzabarserbia profile."""
        # Saved JSON response from pizzabarserbia profile
        profile_data = {
            "data": {
                "user": {
                    "biography": "Pizza bar in Belgrade",
                    "external_url": "http://pizzabar.rs/",
                    "bio_links": [],
                    "business_address_json": '{"city_name": "Belgrade, Serbia", "city_id": 109920975697736, "latitude": 44.8131, "longitude": 20.46329, "street_address": "Bulevar Mihajla Pupina 165 V", "zip_code": "11070"}'
                }
            }
        }
        
        # Extract all data
        wolt_url = extract_wolt_url(profile_data)
        google_maps = extract_google_maps(profile_data)
        website_url = extract_website_url(profile_data)
        telegram_link = extract_telegram_link(profile_data)
        address_text = extract_address_text(profile_data)
        
        # Assert expected outputs
        self.assertIsNone(wolt_url, "pizzabarserbia should not have Wolt URL")
        self.assertIsNone(google_maps, "pizzabarserbia should not have Google Maps URL")
        self.assertEqual(website_url, "http://pizzabar.rs/", "pizzabarserbia should have website URL")
        self.assertIsNone(telegram_link, "pizzabarserbia should not have Telegram link")
        self.assertEqual(address_text, "Bulevar Mihajla Pupina 165 V, Belgrade, Serbia, 11070", "pizzabarserbia should have address text")
    
    def test_error_profile(self):
        """Test extraction for error case (user not found)."""
        # Error response data
        profile_data = {
            "error": "User not found"
        }
        
        # Extract all data
        wolt_url = extract_wolt_url(profile_data)
        google_maps = extract_google_maps(profile_data)
        website_url = extract_website_url(profile_data)
        telegram_link = extract_telegram_link(profile_data)
        address_text = extract_address_text(profile_data)
        
        # Assert expected outputs (all should be None for error case)
        self.assertIsNone(wolt_url, "Error case should return None for Wolt URL")
        self.assertIsNone(google_maps, "Error case should return None for Google Maps URL")
        self.assertIsNone(website_url, "Error case should return None for website URL")
        self.assertIsNone(telegram_link, "Error case should return None for Telegram link")
        self.assertIsNone(address_text, "Error case should return None for address text")
    
    def test_kulturacafe_restaurant_profile(self):

        """Test extraction for @kulturacafe.restaurant profile - empty response case."""
        # Empty response data (what kulturacafe.restaurant actually returns)
        profile_data = {
            "error": "Profile data not accessible - empty response (profile may be private or restricted)"
        }
        
        # Extract all data
        wolt_url = extract_wolt_url(profile_data)
        google_maps = extract_google_maps(profile_data)
        website_url = extract_website_url(profile_data)
        telegram_link = extract_telegram_link(profile_data)
        address_text = extract_address_text(profile_data)
        
        # Assert expected outputs (all should be None for error case)
        self.assertIsNone(wolt_url, "kulturacafe.restaurant should return None for Wolt URL (empty response)")
        self.assertIsNone(google_maps, "kulturacafe.restaurant should return None for Google Maps URL (empty response)")
        self.assertIsNone(website_url, "kulturacafe.restaurant should return None for website URL (empty response)")
        self.assertIsNone(telegram_link, "kulturacafe.restaurant should return None for Telegram link (empty response)")
        self.assertIsNone(address_text, "kulturacafe.restaurant should return None for address text (empty response)")
    
    def test_kulturacafe_restaurant_profile_with_data(self):
        """Test extraction for @kulturacafe.restaurant profile with expected data structure."""
        # Expected data structure if the profile was accessible
        profile_data = {
            "data": {
                "user": {
                    "biography": "Restaurant Kultura - Belgrade\n📍 Location: https://maps.app.goo.gl/6MAJpmSEH3R9qPPTA?g_st=com.google.maps.preview.copy\n🌐 Menu: restorankultura.com/menu",
                    "external_url": "https://restorankultura.com/menu",
                    "bio_links": [
                        {
                            "url": "https://maps.app.goo.gl/6MAJpmSEH3R9qPPTA?g_st=com.google.maps.preview.copy",
                            "title": "Location"
                        }
                    ],
                    "business_address_json": None
                }
            }
        }
        
        # Extract all data
        wolt_url = extract_wolt_url(profile_data)
        google_maps = extract_google_maps(profile_data)
        website_url = extract_website_url(profile_data)
        telegram_link = extract_telegram_link(profile_data)
        address_text = extract_address_text(profile_data)
        
        # Assert expected outputs
        self.assertIsNone(wolt_url, "kulturacafe.restaurant should not have Wolt URL")
        self.assertEqual(google_maps, "https://maps.app.goo.gl/6MAJpmSEH3R9qPPTA?g_st=com.google.maps.preview.copy", "kulturacafe.restaurant should have Google Maps URL")
        self.assertEqual(website_url, "https://restorankultura.com/menu", "kulturacafe.restaurant should have website URL")
        self.assertIsNone(telegram_link, "kulturacafe.restaurant should not have Telegram link")
        self.assertEqual(address_text, "Location", "kulturacafe.restaurant should extract 'Location' from bio_links title")
    
    def test_empty_profile(self):
        """Test extraction for empty profile data."""
        # Empty response data
        profile_data = {}
        
        # Extract all data
        wolt_url = extract_wolt_url(profile_data)
        google_maps = extract_google_maps(profile_data)
        website_url = extract_website_url(profile_data)
        telegram_link = extract_telegram_link(profile_data)
        address_text = extract_address_text(profile_data)
        
        # Assert expected outputs (all should be None for empty case)
        self.assertIsNone(wolt_url, "Empty case should return None for Wolt URL")
        self.assertIsNone(google_maps, "Empty case should return None for Google Maps URL")
        self.assertIsNone(website_url, "Empty case should return None for website URL")
        self.assertIsNone(telegram_link, "Empty case should return None for Telegram link")
        self.assertIsNone(address_text, "Empty case should return None for address text")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
