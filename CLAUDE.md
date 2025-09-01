# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a tarot card collection and processing system with high-quality images from public domain sources. The project focuses on image manipulation, batch processing, and animated GIF generation for tarot cards.

## Common Commands

### Setup Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running Scripts
All scripts are located in the `scripts/` directory and should be run from the project root:

```bash
# Download tarot cards from sources
python scripts/download_tarot_cards.py

# Resize cards to different resolutions
python scripts/resize_cards.py

# Generate animated GIFs
python scripts/create_tarot_gif.py

# Convert images to JPG format
python scripts/convert_to_jpg.py
```

## Architecture and Key Components

### Image Processing Pipeline
1. **Download Stage**: `download_tarot_cards.py` fetches images from Wikimedia Commons
2. **Processing Stage**: `resize_cards.py` creates optimized versions at different resolutions
3. **Conversion Stage**: `convert_to_jpg.py` standardizes formats
4. **Animation Stage**: `create_tarot_gif.py` generates various GIF layouts

### Directory Structure Conventions
- Original images: `tarot/{deck_name}/full/`
- Resized versions: `tarot/{deck_name}/720px/`
- Generated GIFs: `tarot/{deck_name}/gif/`
- All scripts must be in `scripts/` directory

### Key Functions in create_tarot_gif.py

The GIF creation module contains specialized functions for different layouts:

- `create_single_card_gif()`: Single card animation (116x180px)
- `create_three_cards_gif()`: Three cards side-by-side (320x180px)
- `create_celtic_cross_gif()`: 10-card Celtic Cross spread (500x600px)
- `create_telegram_optimized_gif()`: Optimized for Telegram (<1MB, 256x144px)

Each function accepts standard parameters:
- `cards_dir`: Source directory for card images
- `output_path`: Where to save the GIF
- `num_frames`: Number of animation frames
- `duration`: Milliseconds per frame
- `loop`: 0 for infinite loop

### Image Naming Conventions

Cards follow specific naming patterns:
- Major Arcana: `00_Fool.jpg`, `01_Magician.jpg`, etc.
- Minor Arcana: `{Suit}{Number}.jpg` where:
  - Suits: `Wands`, `Cups`, `Swords`, `Pents`
  - Numbers: `01`-`14` (Ace through King)

## Working with Tarot Decks

### Available Decks
- **rider-waite**: Complete 78-card deck with multiple resolutions
- **soimoi**: Alternative deck, all images in JPG format

### Adding New Decks
1. Create directory: `tarot/{deck_name}/full/`
2. Place original images there
3. Run `convert_to_jpg.py` if needed (modify target directory in script)
4. Use `resize_cards.py` to create standard resolutions
5. Update README.md with deck information

## Important Paths and Constants

### Default Paths
- Virtual environment: `venv/`
- Requirements: `requirements.txt`
- Main image directory: `tarot/`

### Image Processing Defaults
- JPG quality: 95%
- GIF optimization: Adaptive palette with 32-128 colors
- Standard card aspect ratio: 0.6 (width/height)
- Telegram GIF limits: <8MB file size

## Testing and Validation

When modifying scripts:
1. Test with a small subset of images first
2. Verify output formats match expected conventions
3. Check file sizes for GIFs (especially Telegram-optimized ones)
4. Ensure no files are overwritten without intention

## Dependencies

Core dependencies (from requirements.txt):
- `Pillow`: Image processing
- `requests`: HTTP downloads
- `beautifulsoup4`: Web scraping (optional)