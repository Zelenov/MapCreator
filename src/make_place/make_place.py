#!/usr/bin/env python3
"""
Make Place - Instagram Place Parser and Folder Creator

This script takes an Instagram link, extracts place information using the place parser,
and creates an organized folder structure with a README.md containing the parsed data.

Usage:
    python make_place.py -i <instagram_link> -o <output_folder>

Example:
    python make_place.py -i https://www.instagram.com/boyar.rs/ -o ./places
"""

import argparse
import os
import sys
import json
from datetime import datetime
from pathlib import Path

from place_data import PlaceData
from instagram_populator import InstagramPopulator
from json_outputter import JsonOutputter
from readme_outputter import ReadmeOutputter


def create_place_folder(output_folder, instagram_handle):
    """
    Create a folder for the Instagram place in the output directory.
    
    Args:
        output_folder (str): Base output directory
        instagram_handle (str): Instagram handle (without @)
        
    Returns:
        str: Path to the created folder
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create folder for this Instagram handle
    place_folder = output_path / instagram_handle
    place_folder.mkdir(exist_ok=True)
    
    return str(place_folder)




def main():
    """Main function to handle command line arguments and orchestrate the process."""
    parser = argparse.ArgumentParser(
        description="Extract place information and create organized folder structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python make_place.py -i https://www.instagram.com/boyar.rs/ -o ./places
  python make_place.py -i @boyar.rs -o ./my_places
  python make_place.py -i boyar.rs -o /path/to/output
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input string (Instagram URL, handle, etc.)'
    )
    
    parser.add_argument(
        '-o', '--output-folder',
        required=True,
        help='Output folder where the place folder will be created'
    )
    
    args = parser.parse_args()
    
    print("🏗️  Make Place - Place Information Extractor")
    print("=" * 50)
    
    # Create PlaceData instance
    print("📄 Creating PlaceData instance...")
    place_data = PlaceData()
    
    # Create list of populators
    print("🔧 Initializing populators...")
    populators = [InstagramPopulator()]
    
    # Track which populators have run (boolean array)
    populated = [False] * len(populators)
    
    # Run populate_from_args for all populators
    print("📝 Processing input with populators...")
    for populator in populators:
        if populator.populate_from_args(place_data, args.input):
            print(f"✅ {populator.name} populator processed input")
    
    # Get the handle for folder creation
    if not place_data.instagram_handle:
        print("❌ Error: Could not extract handle from input")
        sys.exit(1)
    
    # Create folder structure
    print(f"📁 Creating folder structure in: {args.output_folder}")
    place_folder = create_place_folder(args.output_folder, place_data.instagram_handle)
    print(f"✅ Created folder: {place_folder}")
    
    # Populate data using populators
    print("🔄 Populating place data...")
    max_iterations = 10  # Prevent infinite loops
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        any_populated = False
        
        for i, populator in enumerate(populators):
            # Check if this populator can populate and hasn't run yet
            if populator.can_populate(place_data) and not populated[i]:
                print(f"🔄 Running {populator.name} populator...")
                if populator.populate(place_data):
                    print(f"✅ {populator.name} populator completed")
                    populated[i] = True
                    any_populated = True
                else:
                    print(f"⚠️  {populator.name} populator failed")
        
        if not any_populated:
            break
    
    if iteration >= max_iterations:
        print("⚠️  Maximum iterations reached")
    
    # Create list of outputters
    print("🔧 Initializing outputters...")
    outputters = [JsonOutputter(), ReadmeOutputter()]
    
    # Run all outputters
    print("📄 Creating output files...")
    for outputter in outputters:
        if outputter.can_output(place_data):
            print(f"🔄 Running {outputter.name} outputter...")
            if outputter.output(place_data, place_folder):
                print(f"✅ {outputter.name} outputter completed")
            else:
                print(f"⚠️  {outputter.name} outputter failed")
    
    # Summary
    print("\n" + "=" * 50)
    print("🎉 SUCCESS! Place information extracted and organized:")
    print(f"📂 Folder: {place_folder}")
    print(f"📄 README: {place_folder}/README.md")
    print(f"📄 JSON: {place_folder}/place_data.json")


if __name__ == "__main__":
    main()
