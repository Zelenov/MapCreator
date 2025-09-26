#!/usr/bin/env python3
"""
Instagram profile data fetcher and parser.
Main entry point that coordinates profile fetching and data parsing.
"""

import json
from place_fetcher import fetch_profile_with_curl, extract_username_from_input
from place_data_parser import parse_profile_data

def main():
    """
    Main function to demonstrate the Instagram profile fetcher.
    """
    import sys
    
    print("Instagram Profile Fetcher")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage: python place_parser.py <username_or_url> [--debug]")
        print("\nExamples:")
        print("  python place_parser.py instagram")
        print("  python place_parser.py @instagram")
        print("  python place_parser.py https://www.instagram.com/instagram/")
        print("  python place_parser.py instagram --debug")
        print("\nAUTHENTICATION:")
        print("The script will automatically extract authentication tokens from Firefox or Chrome.")
        print("Make sure you're logged into Instagram in one of these browsers before running the script.")
        print("\nUse --debug to see the complete JSON response.")
        sys.exit(1)
    
    user_input = sys.argv[1]
    debug_mode = '--debug' in sys.argv
    
    # Extract username from input (handles URLs, @username, or plain username)
    try:
        username = extract_username_from_input(user_input)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    
    print(f"Fetching profile for @{username}...")
    
    profile_data = fetch_profile_with_curl(username)
    
    # Check for errors in the response
    if 'error' in profile_data:
        print(f"\nERROR: {profile_data['error']}")
        print("\n" + "="*60)
        print("EXTRACTED INFORMATION")
        print("="*60)
        print("Wolt URL: Not found")
        print("Google Maps: Not found")
        print("Website: Not found")
        print("Telegram: Not found")
        print("Address: Not found")
        print("="*60)
        return
    
    # Debug mode: Show complete JSON response
    if debug_mode:
        print("\n" + "="*60)
        print("DEBUG - COMPLETE JSON RESPONSE")
        print("="*60)
        print(json.dumps(profile_data, indent=2, ensure_ascii=False))
        print("="*60)
    
    # Parse profile data using the parser module
    parsed_data = parse_profile_data(profile_data)
    
    print("\n" + "="*60)
    print("EXTRACTED INFORMATION")
    print("="*60)
    
    if parsed_data['wolt_url']:
        print(f"Wolt URL: {parsed_data['wolt_url']}")
    else:
        print("Wolt URL: Not found")
    
    if parsed_data['google_maps']:
        print(f"Google Maps: {parsed_data['google_maps']}")
    else:
        print("Google Maps: Not found")
    
    if parsed_data['website_url']:
        print(f"Website: {parsed_data['website_url']}")
    else:
        print("Website: Not found")
    
    if parsed_data['telegram_link']:
        print(f"Telegram: {parsed_data['telegram_link']}")
    else:
        print("Telegram: Not found")
    
    if parsed_data['address_text']:
        print(f"Address: {parsed_data['address_text']}")
    else:
        print("Address: Not found")
    
    print("="*60)

if __name__ == "__main__":
    main()