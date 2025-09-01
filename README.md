# Tarot Cards Repository

A curated collection of tarot card decks with high-quality images and comprehensive documentation.

## Overview

This repository contains various tarot card decks sourced from public domain and Creative Commons licensed materials. Each deck is organized in its own directory with proper attribution and source information.

## Available Decks

### Rider-Waite Tarot Deck
- **Location**: `tarot/rider-waite/`
- **Source**: Wikimedia Commons
- **License**: Public Domain
- **Description**: The classic Rider-Waite-Smith tarot deck, one of the most influential and widely used tarot decks in the world.
- **Formats**: Full resolution (720px) and optimized versions
- **Complete deck**: 78 cards (22 Major Arcana + 56 Minor Arcana)

### Soimoi Tarot Deck
- **Location**: `tarot/soimoi/`
- **Description**: Alternative tarot deck collection
- **Format**: JPG images in full resolution

## Repository Structure

```
TarotCards/
├── README.md
├── LICENSE
├── SOURCES.md
├── requirements.txt
├── tarot/
│   ├── rider-waite/
│   │   ├── 720px/        # Full resolution cards
│   │   ├── full/         # Original downloads
│   │   ├── gif/          # Generated GIF animations
│   │   └── metadata.json
│   └── soimoi/
│       └── full/         # Full resolution cards
├── decks_config.json      # Configuration file for all decks
└── scripts/
    ├── download_tarot_cards.py
    ├── resize_cards.py
    ├── create_tarot_gif.py
    ├── convert_to_jpg.py
    └── deck_manager.py    # Deck management utility
```

## Installation

### Prerequisites

Install required Python packages:

```bash
pip install -r requirements.txt
```

Required packages:
- `Pillow` - Image processing and manipulation
- `requests` - HTTP library for downloading files
- `beautifulsoup4` - Web scraping (optional, for download scripts)

## Scripts Documentation

### 1. download_tarot_cards.py
**Purpose**: Downloads tarot card images from Wikimedia Commons or other sources.

**Usage**:
```bash
python scripts/download_tarot_cards.py
```

**Features**:
- Downloads complete Rider-Waite deck from Wikimedia Commons
- Handles Major and Minor Arcana cards
- Automatic retry on failed downloads
- Progress tracking

### 2. resize_cards.py
**Purpose**: Universal script for resizing tarot card images to different resolutions.

**Usage**:
```bash
# Resize Rider-Waite cards to 720px width
python scripts/resize_cards.py --source tarot/rider-waite/full --output tarot/rider-waite/720px --width 720

# Create thumbnails for Soimoi deck (200px height)
python scripts/resize_cards.py -s tarot/soimoi/full -o tarot/soimoi/thumbs --height 200 -q 85

# Resize without preserving aspect ratio
python scripts/resize_cards.py -s tarot/new_deck/full -o tarot/new_deck/400x600 -w 400 -h 600 --no-preserve-aspect
```

**Arguments**:
- `-s, --source`: Source directory with cards (required)
- `-o, --output`: Output directory for resized cards (required)
- `-w, --width`: Target width in pixels
- `-H, --height`: Target height in pixels
- `-q, --quality`: JPEG quality (1-100, default: 95)
- `--no-preserve-aspect`: Don't preserve aspect ratio

**Features**:
- Batch resize all cards in a directory
- Maintains original aspect ratio by default
- Creates optimized versions for web/mobile use
- Supports multiple output formats
- Configurable for any tarot deck

### 3. create_tarot_gif.py
**Purpose**: Universal script for creating animated GIF files from tarot cards.

**Usage**:
```bash
# Create single card animation
python scripts/create_tarot_gif.py --source tarot/rider-waite/720px --output tarot/rider-waite/gif --type single

# Create three cards layout for Soimoi deck
python scripts/create_tarot_gif.py -s tarot/soimoi/720px -o tarot/soimoi/gif -t three --pool 20

# Create Celtic Cross spread with custom settings
python scripts/create_tarot_gif.py -s tarot/new_deck/images -o tarot/new_deck/gif -t celtic --frames 15 --duration 600

# Create Telegram-optimized GIF
python scripts/create_tarot_gif.py -s tarot/rider-waite/720px -o tarot/rider-waite/gif -t telegram

# Create random cards GIF
python scripts/create_tarot_gif.py -s tarot/soimoi/full -o tarot/soimoi/gif -t random --cards 30 --name my_random
```

**Arguments**:
- `-s, --source`: Source directory with cards (required)
- `-o, --output`: Output directory for GIF (required)
- `-t, --type`: Type of GIF to create (required)
  - `single`: Single changing card
  - `three`: Three cards side by side
  - `celtic`: Celtic Cross spread (10 cards)
  - `telegram`: Optimized for Telegram
  - `random`: Random sequence of cards
  - `all`: All cards in sequence
  - `filtered`: Filtered cards (e.g., major arcana only)
- `--name`: Custom output filename (without extension)
- `--frames`: Number of frames in animation
- `--duration`: Duration of each frame in ms (default: 500)
- `--pool`: Size of card pool for random selection
- `--cards`: Number of cards for random type
- `--width`: Card width in pixels
- `--height`: Card height in pixels
- `--loop`: Number of loops (0 = infinite)
- `--filter`: Filter for cards (for filtered type)

**Features**:
- **Single Card Animation**: Creates GIF with one changing card
  - Default: 12 frames, 500ms per frame, 232x360px
  
- **Three Cards Layout**: Shows 3 random cards side by side
  - Default: 640x360px (doubled resolution)
  - Random selection from card pool
  
- **Celtic Cross Spread**: Traditional 10-card tarot spread
  - Frame size: 500x600px
  - Card size: 72x120px
  - Proper card positioning with overlay effects
  
- **Telegram Optimization**: Creates small, fast GIFs
  - Optimized file size (<1MB)
  - Fast animation (100ms per frame)
  - Reduced palette for better compression

### 4. convert_to_jpg.py
**Purpose**: Universal script for converting all images to JPG format.

**Usage**:
```bash
# Convert images in Soimoi deck to JPG
python scripts/convert_to_jpg.py --dir tarot/soimoi/full

# Convert with custom quality
python scripts/convert_to_jpg.py -d tarot/new_deck/images --quality 90

# Convert but keep original files
python scripts/convert_to_jpg.py -d tarot/backup --keep-originals
```

**Arguments**:
- `-d, --dir, --directory`: Directory with images (default: tarot/soimoi/full)
- `-q, --quality`: JPEG quality (1-100, default: 95)
- `--keep-originals`: Don't delete original files after conversion

**Features**:
- Converts PNG, GIF, BMP, TIFF, WEBP to JPG
- Handles transparency with white background
- Maintains high quality (95% JPEG quality by default)
- Optionally deletes source files after conversion
- Renames .jpeg extensions to .jpg for consistency
- Works with any directory

### 5. deck_manager.py
**Purpose**: Centralized management utility for tarot decks and their configurations.

**Usage**:
```bash
# List all configured decks
python scripts/deck_manager.py --list

# Add a new deck
python scripts/deck_manager.py --add marseille --name "Tarot de Marseille" --source tarot/marseille

# Get information about a deck
python scripts/deck_manager.py --info rider-waite

# Generate processing scripts for a deck
python scripts/deck_manager.py --deck soimoi --scripts resize
python scripts/deck_manager.py --deck soimoi --scripts gif
python scripts/deck_manager.py --deck soimoi --scripts convert

# Remove a deck from configuration
python scripts/deck_manager.py --remove old_deck
```

**Features**:
- Centralized deck configuration management
- Automatic directory structure creation
- Script generation for batch processing
- Easy deck addition and removal
- Configuration stored in `decks_config.json`

## Configuration File

The `decks_config.json` file stores configuration for all tarot decks:

```json
{
  "decks": {
    "rider-waite": {
      "name": "Rider-Waite",
      "source_dir": "tarot/rider-waite",
      "full_size_dir": "tarot/rider-waite/full",
      "resized_dirs": {
        "720px": "tarot/rider-waite/720px",
        "360px": "tarot/rider-waite/360px",
        "thumbs": "tarot/rider-waite/thumbs"
      },
      "gif_dir": "tarot/rider-waite/gif",
      "card_count": 78
    }
  },
  "default_settings": {
    "gif": {...},
    "resize": {...}
  }
}
```

## Workflow Examples

### Adding a New Tarot Deck

1. **Place card images in a directory**:
   ```bash
   mkdir -p tarot/new_deck/full
   # Copy your card images to tarot/new_deck/full/
   ```

2. **Register the deck**:
   ```bash
   python scripts/deck_manager.py --add new_deck --name "My New Deck" --source tarot/new_deck
   ```

3. **Convert images to JPG if needed**:
   ```bash
   python scripts/convert_to_jpg.py --dir tarot/new_deck/full
   ```

4. **Create resized versions**:
   ```bash
   # 720px width version
   python scripts/resize_cards.py -s tarot/new_deck/full -o tarot/new_deck/720px -w 720
   
   # Thumbnails
   python scripts/resize_cards.py -s tarot/new_deck/full -o tarot/new_deck/thumbs --height 200
   ```

5. **Generate GIF animations**:
   ```bash
   # Single card GIF
   python scripts/create_tarot_gif.py -s tarot/new_deck/720px -o tarot/new_deck/gif -t single
   
   # Three cards GIF
   python scripts/create_tarot_gif.py -s tarot/new_deck/720px -o tarot/new_deck/gif -t three
   
   # Celtic Cross spread
   python scripts/create_tarot_gif.py -s tarot/new_deck/720px -o tarot/new_deck/gif -t celtic
   ```

### Batch Processing with Deck Manager

```bash
# Get all commands for processing a deck
python scripts/deck_manager.py --deck new_deck --scripts resize
python scripts/deck_manager.py --deck new_deck --scripts gif

# The deck manager will output ready-to-use commands for batch processing
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add new decks with proper attribution
4. Update the README and SOURCES.md files
5. Submit a pull request

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0) - see the [LICENSE](LICENSE) file for details.

**This means**:
- ✅ You can use, modify, and share this project for non-commercial purposes
- ✅ You must give appropriate credit
- ❌ You cannot use this project for commercial purposes
- ❌ You cannot sell or monetize the content

## Sources and Attribution

All images are sourced from public domain or Creative Commons licensed materials. See [SOURCES.md](SOURCES.md) for detailed attribution information.

## Disclaimer

This repository is for educational and research purposes. All images are used in accordance with their respective licenses and copyright terms. 