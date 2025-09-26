#!/usr/bin/env python3
"""
README outputter for PlaceData.

This module contains the ReadmeOutputter class that creates README.md files
from PlaceData instances.
"""

from pathlib import Path
from place_data import PlaceData


class ReadmeOutputter:
    """
    Outputter class that creates README.md files from PlaceData.
    """
    
    def __init__(self):
        self.name = "README"
    
    def can_output(self, place_data: PlaceData) -> bool:
        """
        Check if this outputter can create output (always can).
        
        Args:
            place_data: PlaceData instance to check
            
        Returns:
            bool: True if can output, False otherwise
        """
        return True
    
    def format_place_data(self, place_data: PlaceData) -> str:
        """
        Format the place data into a readable markdown format.
        
        Args:
            place_data: PlaceData instance to format
            
        Returns:
            str: Formatted markdown content
        """
        # Use place name if available, otherwise use Instagram handle
        display_name = place_data.get_display_name()
        
        markdown_content = f"""# {display_name}

**Place Information**  
*Generated on: {place_data.extracted_at[:19].replace('T', ' ')}*

---

## 📍 Place Details

"""
        
        # Add each piece of information if available
        if place_data.wolt_url:
            markdown_content += f"### 🍽️ Wolt Delivery\n"
            markdown_content += f"**URL:** [{place_data.wolt_url}]({place_data.wolt_url})\n\n"
        else:
            markdown_content += f"### 🍽️ Wolt Delivery\n"
            markdown_content += f"*Not available*\n\n"
        
        if place_data.google_maps:
            markdown_content += f"### 🗺️ Google Maps\n"
            markdown_content += f"**URL:** [{place_data.google_maps}]({place_data.google_maps})\n\n"
        else:
            markdown_content += f"### 🗺️ Google Maps\n"
            markdown_content += f"*Not available*\n\n"
        
        if place_data.website_url:
            markdown_content += f"### 🌐 Website\n"
            markdown_content += f"**URL:** [{place_data.website_url}]({place_data.website_url})\n\n"
        else:
            markdown_content += f"### 🌐 Website\n"
            markdown_content += f"*Not available*\n\n"
        
        if place_data.telegram_link:
            markdown_content += f"### 📱 Telegram\n"
            markdown_content += f"**URL:** [{place_data.telegram_link}]({place_data.telegram_link})\n\n"
        else:
            markdown_content += f"### 📱 Telegram\n"
            markdown_content += f"*Not available*\n\n"
        
        if place_data.address_text:
            markdown_content += f"### 📍 Address\n"
            markdown_content += f"**Location:** {place_data.address_text}\n\n"
        else:
            markdown_content += f"### 📍 Address\n"
            markdown_content += f"*Not available*\n\n"
        
        # Add Instagram profile section if available
        if place_data.instagram_handle:
            markdown_content += f"""---

## 🔗 Instagram Profile

**Handle:** @{place_data.instagram_handle}  
**Profile URL:** [{place_data.instagram_url}]({place_data.instagram_url})

---

*This information was automatically extracted from various sources.*
"""
        else:
            markdown_content += f"""---

*This information was automatically extracted from various sources.*
"""
        
        return markdown_content
    
    def output(self, place_data: PlaceData, output_folder: str) -> bool:
        """
        Create README.md file from PlaceData.
        
        Args:
            place_data: PlaceData instance to output
            output_folder: Path to the output folder
            
        Returns:
            bool: True if output was successful, False otherwise
        """
        try:
            readme_path = Path(output_folder) / "README.md"
            
            # Generate markdown content
            markdown_content = self.format_place_data(place_data)
            
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"✅ Created README.md in: {readme_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating README file: {e}")
            return False
