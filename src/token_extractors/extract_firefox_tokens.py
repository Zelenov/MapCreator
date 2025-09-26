#!/usr/bin/env python3
"""
Extract Instagram authentication tokens from Firefox browser cookies.
This script automatically reads Firefox cookies and extracts the required tokens.
"""

import os
import sqlite3
import json
import shutil
import tempfile
from pathlib import Path
import platform

def get_firefox_profile_path():
    """Get the path to the Firefox profile directory."""
    system = platform.system()
    
    if system == "Windows":
        # Windows Firefox profile path
        appdata = os.environ.get('APPDATA', '')
        firefox_path = os.path.join(appdata, 'Mozilla', 'Firefox', 'Profiles')
    elif system == "Darwin":  # macOS
        home = os.path.expanduser("~")
        firefox_path = os.path.join(home, 'Library', 'Application Support', 'Firefox', 'Profiles')
    else:  # Linux
        home = os.path.expanduser("~")
        firefox_path = os.path.join(home, '.mozilla', 'firefox')
    
    if not os.path.exists(firefox_path):
        raise FileNotFoundError(f"Firefox profile directory not found: {firefox_path}")
    
    return firefox_path

def find_firefox_profile():
    """Find the active Firefox profile directory."""
    firefox_path = get_firefox_profile_path()
    
    # Look for profile directories
    profiles = []
    for item in os.listdir(firefox_path):
        item_path = os.path.join(firefox_path, item)
        if os.path.isdir(item_path) and (item.endswith('.default') or item.endswith('.default-release')):
            profiles.append(item_path)
    
    if not profiles:
        raise FileNotFoundError("No Firefox profiles found")
    
    # Return the first profile (usually the default one)
    return profiles[0]

def copy_cookies_db(profile_path):
    """Copy the cookies database to a temporary location."""
    cookies_path = os.path.join(profile_path, 'cookies.sqlite')
    
    if not os.path.exists(cookies_path):
        raise FileNotFoundError(f"Cookies database not found: {cookies_path}")
    
    # Create a temporary copy
    temp_dir = tempfile.mkdtemp()
    temp_cookies_path = os.path.join(temp_dir, 'cookies.sqlite')
    shutil.copy2(cookies_path, temp_cookies_path)
    
    return temp_cookies_path

def extract_instagram_tokens(cookies_db_path):
    """Extract Instagram tokens from the cookies database."""
    try:
        conn = sqlite3.connect(cookies_db_path)
        cursor = conn.cursor()
        
        # Query for Instagram cookies
        query = """
        SELECT name, value, host 
        FROM moz_cookies 
        WHERE host LIKE '%instagram.com%' 
        AND name IN ('csrftoken', 'sessionid', 'mid')
        ORDER BY name
        """
        
        cursor.execute(query)
        cookies = cursor.fetchall()
        
        conn.close()
        
        # Organize cookies by name
        tokens = {}
        for name, value, host in cookies:
            if 'instagram.com' in host:
                tokens[name] = value
        
        return tokens
        
    except sqlite3.Error as e:
        raise Exception(f"Error reading cookies database: {e}")

def main():
    """Main function to extract Instagram tokens from Firefox."""
    print("FIREFOX INSTAGRAM TOKEN EXTRACTOR")
    print("=" * 50)
    print()
    
    try:
        # Find Firefox profile
        print("🔍 Looking for Firefox profile...")
        profile_path = find_firefox_profile()
        print(f"✅ Found Firefox profile: {os.path.basename(profile_path)}")
        
        # Copy cookies database
        print("📋 Copying cookies database...")
        temp_cookies_path = copy_cookies_db(profile_path)
        print("✅ Cookies database copied successfully")
        
        # Extract tokens
        print("🍪 Extracting Instagram tokens...")
        tokens = extract_instagram_tokens(temp_cookies_path)
        
        # Clean up temporary file
        os.remove(temp_cookies_path)
        os.rmdir(os.path.dirname(temp_cookies_path))
        
        if not tokens:
            print("❌ No Instagram tokens found in Firefox cookies.")
            print("   Make sure you're logged into Instagram in Firefox.")
            return
        
        # Display results
        print()
        print("🎉 SUCCESS! Found Instagram tokens:")
        print("=" * 50)
        
        for name, value in tokens.items():
            print(f"{name:12}: {value}")
        
        print()
        print("📋 USAGE INSTRUCTIONS:")
        print("=" * 50)
        print("Now you can use these tokens with instagram_fetcher.py:")
        print()
        
        if 'csrftoken' in tokens and 'sessionid' in tokens:
            print("python instagram_fetcher.py <username> \\")
            print(f"  {tokens['csrftoken']} \\")
            print(f"  {tokens['sessionid']}", end="")
            if 'mid' in tokens:
                print(f" \\")
                print(f"  {tokens['mid']}")
            else:
                print()
        else:
            print("❌ Missing required tokens (csrftoken or sessionid)")
        
        print()
        print("📝 EXAMPLE:")
        print("python instagram_fetcher.py boyar.rs \\")
        print(f"  {tokens.get('csrftoken', 'YOUR_CSRF_TOKEN')} \\")
        print(f"  {tokens.get('sessionid', 'YOUR_SESSION_ID')}")
        
        # Save tokens to file
        tokens_file = "instagram_tokens_firefox.cookies"
        with open(tokens_file, 'w') as f:
            json.dump(tokens, f, indent=2)
        
        print()
        print(f"💾 Tokens saved to: {tokens_file}")
        print("   You can reference this file later")
        
    except FileNotFoundError as e:
        print(f"❌ ERROR: {e}")
        print()
        print("💡 TROUBLESHOOTING:")
        print("- Make sure Firefox is installed")
        print("- Make sure you've logged into Instagram in Firefox")
        print("- Try running Firefox at least once to create the profile")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print()
        print("💡 TROUBLESHOOTING:")
        print("- Make sure Firefox is not running (close it completely)")
        print("- Try logging into Instagram in Firefox first")
        print("- Check if you have permission to access Firefox data")

if __name__ == "__main__":
    main()
