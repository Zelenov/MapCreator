# MapCreator

Extract Instagram place information and create organized folders with detailed data.

## Installation

```bash
pip install -r requirements.txt
```

Make sure you're logged into Instagram in Firefox or Chrome.

## Usage

### make_place - Main Tool

Extract place information from Instagram and create organized folders:

```bash
python src/make_place/make_place.py -i <instagram_input> -o <output_folder>
```

**Examples**:
```bash
# Instagram URL
python src/make_place/make_place.py -i https://www.instagram.com/boyar.rs/ -o ./places

# Handle with @
python src/make_place/make_place.py -i @boyar.rs -o ./my_places

# Plain username
python src/make_place/make_place.py -i boyar.rs -o /path/to/output
```

## Output

Creates organized folders with:
- **README.md** - Human-readable place information
- **place_data.json** - Structured JSON data

```
places/
└── boyar.rs/
    ├── README.md
    └── place_data.json
```

## Testing

```bash
python run_tests.py
```

## Notes

- Automatically extracts Instagram tokens from Firefox/Chrome
- Works on Windows, macOS, and Linux
- Must be logged into Instagram in your browser
