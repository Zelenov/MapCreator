#!/usr/bin/env python3
"""
Instagram profile data fetcher using the same API as curl commands.
Handles authentication and API requests to Instagram.
"""

import requests
import json
import re
import sys
import os

# Add the token_extractors directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'token_extractors'))
from place_token_extractor import extract_instagram_tokens

def extract_username_from_input(user_input):
    """
    Extract username from either a username or full Instagram URL.
    Returns: str - Clean username
    """
    # If it's a full URL, extract the username
    if user_input.startswith('http'):
        # Pattern to match Instagram URLs
        pattern = r'instagram\.com/([^/?]+)'
        match = re.search(pattern, user_input)
        if match:
            return match.group(1)
        else:
            raise ValueError(f"Invalid Instagram URL format: {user_input}")
    
    # If it starts with @, remove it
    if user_input.startswith('@'):
        return user_input[1:]
    
    # Otherwise, assume it's already a username
    return user_input

def fetch_profile_with_curl(username, csrftoken=None, sessionid=None, mid=None):
    """
    Fetches Instagram profile data using the same API as the curl command.
    Automatically extracts tokens from browsers if authentication fails.
    """
    
    # The exact API endpoint from your curl command
    api_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    
    # Headers exactly as in your curl command
    headers = {
        'x-ig-app-id': '936619743392459',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': f'https://www.instagram.com/{username}/',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    
    # Try with provided tokens first, or extract from browsers
    if csrftoken and sessionid:
        # Use provided tokens
        headers['x-csrftoken'] = csrftoken
        cookies = {
            'csrftoken': csrftoken,
            'sessionid': sessionid
        }
        if mid:
            cookies['mid'] = mid
    else:
        # Extract tokens from available browsers
        print("No authentication tokens provided. Extracting from browsers...")
        tokens = extract_instagram_tokens()
        
        if not tokens or 'csrftoken' not in tokens or 'sessionid' not in tokens:
            return {
                "error": "Authentication required. Please log into Instagram in Firefox or Chrome, or provide tokens manually."
            }
        
        print("Successfully extracted tokens from browser.")
        headers['x-csrftoken'] = tokens['csrftoken']
        cookies = {
            'csrftoken': tokens['csrftoken'],
            'sessionid': tokens['sessionid']
        }
        if 'mid' in tokens:
            cookies['mid'] = tokens['mid']
    
    try:
        response = requests.get(api_url, headers=headers, cookies=cookies)
        
        # If we get 401, try to extract fresh tokens from browsers
        if response.status_code == 401:
            print("Authentication failed (401). Trying to extract fresh tokens from browsers...")
            tokens = extract_instagram_tokens()
            
            if tokens and 'csrftoken' in tokens and 'sessionid' in tokens:
                print("Retrying with fresh tokens from browser...")
                headers['x-csrftoken'] = tokens['csrftoken']
                cookies = {
                    'csrftoken': tokens['csrftoken'],
                    'sessionid': tokens['sessionid']
                }
                if 'mid' in tokens:
                    cookies['mid'] = tokens['mid']
                
                response = requests.get(api_url, headers=headers, cookies=cookies)
            else:
                return {"error": "Authentication failed. Please log into Instagram in Firefox or Chrome and try again."}
        
        if response.status_code == 200:
            data = response.json()
            
            # Check for strange empty responses that only contain status
            if data == {"status": "ok"} or (len(data) == 1 and "status" in data):
                return {"error": "Profile data not accessible - empty response (profile may be private or restricted)"}
            
            return data
        else:
            return {"error": f"API request failed: {response.status_code}"}
            
    except Exception as e:
        return {"error": str(e)}


