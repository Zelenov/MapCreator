#!/usr/bin/env python3
"""
Helper script to extract Instagram authentication tokens from browser cookies.
This script helps you get the required csrftoken, sessionid, and mid values.
"""

import webbrowser
import time
import json

def print_instructions():
    """Print detailed instructions for getting Instagram tokens."""
    print("🔑 INSTAGRAM AUTHENTICATION TOKEN EXTRACTOR")
    print("=" * 60)
    print()
    print("This script will help you get the required authentication tokens.")
    print()
    print("📋 STEP-BY-STEP INSTRUCTIONS:")
    print()
    print("1. 🌐 The script will open Instagram in your default browser")
    print("2. 🔐 Log in to your Instagram account")
    print("3. 🔧 Open Developer Tools (press F12)")
    print("4. 📱 Go to the 'Application' tab (Chrome) or 'Storage' tab (Firefox)")
    print("5. 🍪 Find 'Cookies' section and click on 'https://www.instagram.com'")
    print("6. 📋 Copy the following cookie values:")
    print("   - csrftoken")
    print("   - sessionid") 
    print("   - mid (optional but recommended)")
    print()
    print("7. 💾 Save these values and use them with place_parser.py")
    print()
    print("⚠️  IMPORTANT NOTES:")
    print("- These tokens are tied to your Instagram session")
    print("- They will expire when you log out or after some time")
    print("- Keep them secure and don't share them")
    print("- You may need to refresh them periodically")
    print()
    
    input("Press Enter when you're ready to open Instagram...")
    
    # Open Instagram
    print("🌐 Opening Instagram in your browser...")
    webbrowser.open("https://www.instagram.com")
    
    print()
    print("📝 After you get the tokens, use them like this:")
    print("python place_parser.py <username> <csrftoken> <sessionid> [mid]")
    print()
    print("Example:")
    print("python place_parser.py boyar.rs abc123def456 xyz789session")
    print()

def create_token_template():
    """Create a template file for storing tokens."""
    template = {
        "csrftoken": "YOUR_CSRF_TOKEN_HERE",
        "sessionid": "YOUR_SESSION_ID_HERE", 
        "mid": "YOUR_MID_HERE_OPTIONAL",
        "instructions": [
            "1. Replace the placeholder values above with your actual tokens",
            "2. Save this file as 'place_tokens.cookies'",
            "3. Use the tokens with place_parser.py",
            "4. Keep this file secure and don't commit it to version control"
        ]
    }
    
    with open("place_tokens_template.cookies", "w") as f:
        json.dump(template, f, indent=2)
    
    print("📄 Created 'place_tokens_template.cookies' for your convenience")
    print("   You can fill in your tokens and reference them later")

if __name__ == "__main__":
    print_instructions()
    create_token_template()
    
    print("✅ Setup complete! You can now get your Instagram tokens.")
    print("   Remember to use them with the place_parser.py script.")
