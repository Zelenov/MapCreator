# Instagram Content Parser

This script downloads Instagram page content and extracts Google Maps links and other relevant information.

## Features

- Downloads Instagram page content
- Extracts Google Maps links (both direct and Instagram redirect links)
- Extracts other relevant links
- Searches for address information in the content
- Provides formatted output

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Usage

```bash
python instagram_parser.py <instagram_url>
```

Example:
```bash
python instagram_parser.py "https://www.instagram.com/p/example/"
```

### Using as a Module

```python
from instagram_parser import InstagramParser

parser = InstagramParser()
results = parser.parse_instagram_page("https://www.instagram.com/p/example/")
parser.print_results(results)
```

### Test Script

Run the test script with the provided sample URL:
```bash
python test_parser.py
```

## Output

The script will output:
- Google Maps links found (both direct and Instagram redirect links)
- Other relevant links
- Address information if found
- Summary statistics

## Notes

- The script uses browser-like headers to avoid being blocked
- Instagram redirect links are automatically decoded
- The script handles both direct Google Maps links and Instagram redirect links
- Address extraction uses common patterns like "Address:", "Location:", and location emojis