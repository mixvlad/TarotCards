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
# Download a public-domain deck from Wikimedia Commons
python scripts/download_commons_deck.py --deck sola-busca

# Resize cards to different resolutions
python scripts/resize_cards.py

# Generate animated GIFs
python scripts/create_tarot_gif.py

# Convert images to JPG format
python scripts/convert_to_jpg.py
```

## Architecture and Key Components

### Image Processing Pipeline
1. **Download Stage**: `download_commons_deck.py` fetches public-domain decks from Wikimedia Commons (Rider-Waite images are already in the repo; their original download script was removed)
2. **Processing Stage**: `resize_cards.py` creates optimized versions at different resolutions
3. **Conversion Stage**: `convert_to_jpg.py` standardizes formats
4. **Animation Stage**: `create_tarot_gif.py` generates various GIF layouts

### Directory Structure Conventions
- Original images: `tarot/{deck_name}/full/`
- Resized versions: `tarot/{deck_name}/720px/`
- Rider-Waite only: lossless PNG originals in `tarot/rider-waite/full-png/` (`full/` holds JPG copies)
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
- **rider-waite**: Complete 78-card deck (steve-p.org, public domain)
- **soimoi**: Original deck by Mike Koz, generated with an image model, JPG, licensed CC BY 4.0 (`tarot/soimoi/LICENSE`)
- **sola-busca**: 78 cards `00.jpg`–`77.jpg` (Wikimedia Commons, public domain)
- **marseille**: 78 PNG cards, historical trump numbering (Wikimedia Commons, public domain)
- **etteilla**: 75 cards in Etteilla's own 1–78 numbering, `NN_<Title>.jpg` (BnF via Commons, public domain)
- **vieville**: 78 cards, Marseille-style names (BnF via Commons, public domain)
- **visconti-sforza**: 73 surviving cards, RWS-style names (Commons, public domain)
- **oswald-wirth**: 22 major arcana only (BnF via Commons, public domain)
- **tarot-nouveau**: 78-card French-suited game deck, suits Hearts/Diamonds/Clubs/Spades (BnF via Commons, public domain)

Card backs are stored as `Cover.jpg` next to the cards; `create_tarot_gif.py` skips them.

Licensing: scripts are MIT (`LICENSE`), each deck carries its own license — keep README.md and SOURCES.md in sync when adding a deck.

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

`download_commons_deck.py` uses only the standard library (`urllib`).