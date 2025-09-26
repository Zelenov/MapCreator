#!/usr/bin/env python3
"""
Token extraction module for Instagram authentication.
Extracts authentication tokens from Firefox and Chrome browsers.
"""

import os
import sqlite3
import shutil
import tempfile
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

def extract_instagram_tokens_from_firefox():
    """Extract Instagram tokens from Firefox cookies."""
    try:
        # Find Firefox profile
        profile_path = find_firefox_profile()
        
        # Copy cookies database
        cookies_path = os.path.join(profile_path, 'cookies.sqlite')
        if not os.path.exists(cookies_path):
            raise FileNotFoundError(f"Cookies database not found: {cookies_path}")
        
        # Create a temporary copy
        temp_dir = tempfile.mkdtemp()
        temp_cookies_path = os.path.join(temp_dir, 'cookies.sqlite')
        shutil.copy2(cookies_path, temp_cookies_path)
        
        # Extract tokens
        conn = sqlite3.connect(temp_cookies_path)
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
        
        # Clean up temporary file
        os.remove(temp_cookies_path)
        os.rmdir(temp_dir)
        
        # Organize cookies by name
        tokens = {}
        for name, value, host in cookies:
            if 'instagram.com' in host:
                tokens[name] = value
        
        return tokens
        
    except Exception as e:
        return None

def get_chrome_profile_path():
    """Get the path to the Chrome profile directory."""
    system = platform.system()
    
    if system == "Windows":
        # Windows Chrome profile path
        localappdata = os.environ.get('LOCALAPPDATA', '')
        chrome_path = os.path.join(localappdata, 'Google', 'Chrome', 'User Data', 'Default')
    elif system == "Darwin":  # macOS
        home = os.path.expanduser("~")
        chrome_path = os.path.join(home, 'Library', 'Application Support', 'Google', 'Chrome', 'Default')
    else:  # Linux
        home = os.path.expanduser("~")
        chrome_path = os.path.join(home, '.config', 'google-chrome', 'Default')
    
    if not os.path.exists(chrome_path):
        raise FileNotFoundError(f"Chrome profile directory not found: {chrome_path}")
    
    return chrome_path

def find_chrome_profile():
    """Find the active Chrome profile directory."""
    system = platform.system()
    
    if system == "Windows":
        localappdata = os.environ.get('LOCALAPPDATA', '')
        chrome_base = os.path.join(localappdata, 'Google', 'Chrome', 'User Data')
    elif system == "Darwin":  # macOS
        home = os.path.expanduser("~")
        chrome_base = os.path.join(home, 'Library', 'Application Support', 'Google', 'Chrome')
    else:  # Linux
        home = os.path.expanduser("~")
        chrome_base = os.path.join(home, '.config', 'google-chrome')
    
    if not os.path.exists(chrome_base):
        raise FileNotFoundError(f"Chrome directory not found: {chrome_base}")
    
    # Look for profile directories
    profiles = []
    for item in os.listdir(chrome_base):
        item_path = os.path.join(chrome_base, item)
        if os.path.isdir(item_path) and (item == 'Default' or item.startswith('Profile')):
            profiles.append(item_path)
    
    if not profiles:
        raise FileNotFoundError("No Chrome profiles found")
    
    # Return the Default profile first, then others
    default_profile = os.path.join(chrome_base, 'Default')
    if os.path.exists(default_profile):
        return default_profile
    else:
        return profiles[0]

def extract_instagram_tokens_from_chrome():
    """Extract Instagram tokens from Chrome cookies."""
    try:
        # Find Chrome profile
        profile_path = find_chrome_profile()
        
        # Copy cookies database
        cookies_path = os.path.join(profile_path, 'Cookies')
        if not os.path.exists(cookies_path):
            raise FileNotFoundError(f"Cookies database not found: {cookies_path}")
        
        # Create a temporary copy
        temp_dir = tempfile.mkdtemp()
        temp_cookies_path = os.path.join(temp_dir, 'Cookies')
        shutil.copy2(cookies_path, temp_cookies_path)
        
        # Extract tokens
        conn = sqlite3.connect(temp_cookies_path)
        cursor = conn.cursor()
        
        # Query for Instagram cookies
        query = """
        SELECT name, value, host_key 
        FROM cookies 
        WHERE host_key LIKE '%instagram.com%' 
        AND name IN ('csrftoken', 'sessionid', 'mid')
        ORDER BY name
        """
        
        cursor.execute(query)
        cookies = cursor.fetchall()
        conn.close()
        
        # Clean up temporary file
        os.remove(temp_cookies_path)
        os.rmdir(temp_dir)
        
        # Organize cookies by name
        tokens = {}
        for name, value, host in cookies:
            if 'instagram.com' in host:
                tokens[name] = value
        
        return tokens
        
    except Exception as e:
        return None

def extract_instagram_tokens():
    """Extract Instagram tokens from available browsers (Firefox first, then Chrome)."""
    # Try Firefox first
    tokens = extract_instagram_tokens_from_firefox()
    if tokens and 'csrftoken' in tokens and 'sessionid' in tokens:
        return tokens
    
    # Try Chrome if Firefox failed
    tokens = extract_instagram_tokens_from_chrome()
    if tokens and 'csrftoken' in tokens and 'sessionid' in tokens:
        return tokens
    
    return None


