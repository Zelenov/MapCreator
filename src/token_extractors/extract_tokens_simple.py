#!/usr/bin/env python3
"""
Simple Instagram token extractor for Firefox and Chrome browsers.
This script automatically tries to extract tokens from both browsers.
"""

import os
import sys
import subprocess

def run_script(script_name):
    """Run a script and return its exit code."""
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def main():
    """Main function to extract tokens from available browsers."""
    print("INSTAGRAM TOKEN EXTRACTOR")
    print("=" * 40)
    print()
    print("This script will try to extract Instagram tokens from your browsers.")
    print()
    
    # List of available extractors
    extractors = [
        ("Firefox", "extract_firefox_tokens.py"),
        ("Chrome", "extract_chrome_tokens.py")
    ]
    
    success_count = 0
    results = []
    
    for browser_name, script_name in extractors:
        print(f"Trying {browser_name}...")
        print("-" * 30)
        
        if not os.path.exists(script_name):
            print(f"ERROR: {browser_name} extractor not found: {script_name}")
            print()
            continue
        
        exit_code, stdout, stderr = run_script(script_name)
        
        if exit_code == 0:
            print(f"SUCCESS: {browser_name} extraction successful!")
            print(stdout)
            success_count += 1
            results.append((browser_name, True, stdout))
        else:
            print(f"ERROR: {browser_name} extraction failed")
            if stderr:
                print(f"Error: {stderr}")
            results.append((browser_name, False, stderr))
        
        print()
    
    # Summary
    print("EXTRACTION SUMMARY")
    print("=" * 40)
    
    if success_count == 0:
        print("ERROR: No tokens were extracted from any browser.")
        print()
        print("TROUBLESHOOTING:")
        print("1. Make sure you're logged into Instagram in at least one browser")
        print("2. Close all browser instances before running the extractor")
        print("3. Try running the individual extractors manually:")
        print("   - python extract_firefox_tokens.py")
        print("   - python extract_chrome_tokens.py")
        print("4. Check if you have permission to access browser data")
    else:
        print(f"SUCCESS: Extracted tokens from {success_count} browser(s)")
        print()
        print("NEXT STEPS:")
        print("1. Use the extracted tokens with instagram_fetcher.py")
        print("2. Example: python instagram_fetcher.py <username> <csrftoken> <sessionid>")
        print("3. The tokens are also saved to JSON files for reference")
    
    print()
    print("MANUAL EXTRACTION:")
    print("If automatic extraction fails, you can manually get tokens:")
    print("1. Open Instagram in your browser and log in")
    print("2. Open Developer Tools (F12)")
    print("3. Go to Application/Storage tab")
    print("4. Find Cookies section for instagram.com")
    print("5. Copy csrftoken, sessionid, and mid values")

if __name__ == "__main__":
    main()



