#!/usr/bin/env python3
"""
Instagram profile data parser.
Extracts specific information from Instagram profile data (Wolt, Google Maps, Website, Telegram, Address).
"""

import re
import json

def extract_wolt_url(profile_data):
    """
    Extract Wolt URL from profile data.
    Returns: Optional[str] - Wolt URL if found, None otherwise
    """
    if 'error' in profile_data:
        return None
    
    if 'data' not in profile_data or 'user' not in profile_data['data']:
        return None
    
    user = profile_data['data']['user']
    
    # Check external URL for Wolt
    if user.get('external_url') and 'wolt.com' in user['external_url']:
        return user['external_url']
    
    # Check bio links for Wolt URL
    if 'bio_links' in user:
        for link in user['bio_links']:
            url = link.get('url', '')
            if 'wolt.com' in url:
                return url
    
    return None

def extract_google_maps(profile_data):
    """
    Extract Google Maps URL from profile data.
    Returns: Optional[str] - Google Maps URL if found, None otherwise
    """
    if 'error' in profile_data:
        return None
    
    if 'data' not in profile_data or 'user' not in profile_data['data']:
        return None
    
    user = profile_data['data']['user']
    
    # Check bio links for Google Maps URL
    if 'bio_links' in user:
        for link in user['bio_links']:
            url = link.get('url', '')
            if 'maps.app.goo.gl' in url or 'google.com/maps' in url:
                return url
    
    return None

def extract_website_url(profile_data):
    """
    Extract website URL from profile data.
    Returns: Optional[str] - Website URL if found, None otherwise
    """
    if 'error' in profile_data:
        return None
    
    if 'data' not in profile_data or 'user' not in profile_data['data']:
        return None
    
    user = profile_data['data']['user']
    
    # Check external_url in user data (main website link)
    external_url = user.get('external_url')
    if external_url and external_url.strip():
        # Filter out Google Maps, Wolt, and Telegram links
        if not any(domain in external_url.lower() for domain in ['maps.app.goo.gl', 'google.com/maps', 'wolt.com', 't.me/']):
            return external_url
    
    # Check bio_links for website URLs
    if 'bio_links' in user:
        for link in user['bio_links']:
            url = link.get('url', '')
            if url and url.strip():
                # Filter out Google Maps, Wolt, and Telegram links
                if not any(domain in url.lower() for domain in ['maps.app.goo.gl', 'google.com/maps', 'wolt.com', 't.me/']):
                    return url
    
    return None

def extract_telegram_link(profile_data):
    """
    Extract Telegram link from profile data.
    Returns: Optional[str] - Telegram URL if found, None otherwise
    """
    if 'error' in profile_data:
        return None
    
    if 'data' not in profile_data or 'user' not in profile_data['data']:
        return None
    
    user = profile_data['data']['user']
    
    # Check external_url in user data for Telegram links
    external_url = user.get('external_url')
    if external_url and external_url.strip():
        if 't.me/' in external_url.lower():
            return external_url
    
    # Check bio_links for Telegram links
    if 'bio_links' in user:
        for link in user['bio_links']:
            url = link.get('url', '')
            if url and 't.me/' in url.lower():
                return url
    
    return None

def extract_address_text(profile_data):
    """
    Extract actual address text from profile data.
    Returns: Optional[str] - Address text if found, None otherwise
    """
    if 'error' in profile_data:
        return None
    
    if 'data' not in profile_data or 'user' not in profile_data['data']:
        return None
    
    user = profile_data['data']['user']
    
    # First, check for business_address_json (most reliable)
    if 'business_address_json' in user and user['business_address_json']:
        try:
            address_data = json.loads(user['business_address_json'])
            # Format: "Street Address, City, Zip Code"
            street_address = address_data.get('street_address', '')
            city_name = address_data.get('city_name', '')
            zip_code = address_data.get('zip_code', '')
            
            if street_address and city_name:
                address_parts = [street_address, city_name]
                if zip_code:
                    address_parts.append(zip_code)
                return ', '.join(address_parts)
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
    
    # Check bio text for address patterns
    bio = user.get('biography', '')
    if bio:
        # Pattern for addresses with city, country, postal code
        address_patterns = [
            r'[A-Za-z\s°]+\s+bar,\s*[A-Za-z\s]+,\s*[A-Za-z\s]+\s*\d{5}',  # Specific for bar format with postal code
            r'[A-Za-z\s°]+\s+bar,\s*[A-Za-z\s]+,\s*[A-Za-z\s]+',  # Bar format without postal code
            r'[A-Za-z\s°]+,\s*[A-Za-z\s]+,\s*[A-Za-z\s]+\s*\d{5}',  # Name, City, Country, Postal Code
            r'[A-Za-z\s°]+,\s*[A-Za-z\s]+,\s*[A-Za-z\s]+',  # Name, City, Country
            r'[A-Za-z\s°]+,\s*[A-Za-z\s]+',  # Name, City
        ]
        
        for pattern in address_patterns:
            matches = re.findall(pattern, bio)
            if matches:
                # Return the longest match (most complete address)
                return max(matches, key=len).strip()
    
    # Check bio links for address in title
    if 'bio_links' in user:
        for link in user['bio_links']:
            title = link.get('title', '')
            if any(keyword in title.lower() for keyword in ['address', 'adresa', 'location', 'lokacija', 'mapa']):
                return title
    
    # Check recent posts for address information
    if 'edge_owner_to_timeline_media' in user and 'edges' in user['edge_owner_to_timeline_media']:
        posts = user['edge_owner_to_timeline_media']['edges']
        
        # Address patterns to look for in post captions
        address_patterns = [
            r'📍\s*bar\s+[A-Za-z\s°]+[^\n]*\n[A-Za-z\s,]+,\s*[A-Za-z\s]+',  # Bar with location pin
            r'bar\s+[A-Za-z\s°]+,\s*[A-Za-z\s]+,\s*[A-Za-z\s]+',  # Bar format
            r'[A-Za-z\s°]+\s+bar,\s*[A-Za-z\s]+,\s*[A-Za-z\s]+',  # Name bar, City, Country
        ]
        
        for post in posts[:10]:  # Check first 10 posts
            node = post.get('node', {})
            
            # Check post caption
            if 'edge_media_to_caption' in node and 'edges' in node['edge_media_to_caption']:
                for caption_edge in node['edge_media_to_caption']['edges']:
                    caption_text = caption_edge.get('node', {}).get('text', '')
                    for pattern in address_patterns:
                        matches = re.findall(pattern, caption_text, re.MULTILINE | re.DOTALL)
                        if matches:
                            # Clean up the match and return
                            address = matches[0].strip().replace('\n', ', ')
                            return address
            
            # Check accessibility caption
            accessibility_caption = node.get('accessibility_caption', '')
            if accessibility_caption:
                for pattern in address_patterns:
                    matches = re.findall(pattern, accessibility_caption)
                    if matches:
                        return matches[0].strip()
    
    return None

def extract_place_name(profile_data):
    """
    Extract the place name (full_name) from profile data.
    Returns: Optional[str] - Place name if found, None otherwise
    """
    if 'error' in profile_data:
        return None
    
    if 'data' not in profile_data or 'user' not in profile_data['data']:
        return None
    
    user = profile_data['data']['user']
    
    # Get the full name from the profile
    full_name = user.get('full_name')
    if full_name and full_name.strip():
        return full_name.strip()
    
    # If no full_name, try to extract from biography
    biography = user.get('biography', '')
    if biography:
        # Look for common patterns that might indicate a place name
        # Remove common prefixes/suffixes and extract the main name
        bio_lines = biography.split('\n')
        for line in bio_lines:
            line = line.strip()
            if line and not line.startswith(('📍', '🌐', '📱', '🍽️', '📞', '📧', 'http', 'www.')):
                # This might be the place name
                return line
    
    return None

def extract_instagram_handle(profile_data):
    """
    Extract the Instagram handle (username) from profile data.
    Returns: Optional[str] - Instagram handle if found, None otherwise
    """
    if 'error' in profile_data:
        return None
    
    if 'data' not in profile_data or 'user' not in profile_data['data']:
        return None
    
    user = profile_data['data']['user']
    
    # Get the username from the profile
    username = user.get('username')
    if username and username.strip():
        return username.strip()
    
    return None

def parse_profile_data(profile_data):
    """
    Parse all profile data and return a dictionary with extracted information.
    Returns: dict - Dictionary with all extracted information
    """
    return {
        'instagram_handle': extract_instagram_handle(profile_data),
        'place_name': extract_place_name(profile_data),
        'wolt_url': extract_wolt_url(profile_data),
        'google_maps': extract_google_maps(profile_data),
        'website_url': extract_website_url(profile_data),
        'telegram_link': extract_telegram_link(profile_data),
        'address_text': extract_address_text(profile_data)
    }


