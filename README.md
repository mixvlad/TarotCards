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
- **Cards**: 7 verified working cards available
- **Status**: ✅ Working cards downloaded
- **Available Cards**:
  - 00_Fool (The Fool)
  - 10_Wheel_of_Fortune (Wheel of Fortune)
  - 12_Hanged_Man (The Hanged Man)
  - 13_Death (Death)
  - 14_Temperance (Temperance)
  - 17_Star (The Star)
  - 19_Sun (The Sun)

## Repository Structure

```
TarotCards/
├── README.md
├── LICENSE
├── SOURCES.md
├── tarot/
│   └── rider-waite/
│       ├── cards/
│       └── metadata.json
└── scripts/
    ├── download_rider_waite.sh
    ├── download_rider_waite_curl.sh
    ├── download_rider_waite_complete.sh
    ├── download_rider_waite_alternative.sh
    ├── download_rider_waite_simple.sh
    └── download_rider_waite_manual.sh
```

## Usage

### Downloading Decks

To download the verified working Rider-Waite cards (7 cards, macOS compatible):

```bash
./scripts/download_rider_waite_final.sh
```

### Available Scripts

The repository includes several download scripts:

1. **`download_rider_waite_final.sh`** - Verified working cards (7 cards, recommended)
2. **`download_rider_waite_complete.sh`** - Complete deck attempt (78 cards)
3. **`download_rider_waite_curl.sh`** - Major Arcana only (22 cards)
4. **`download_rider_waite.sh`** - Original script (requires wget)
5. **`download_rider_waite_alternative.sh`** - Alternative approach
6. **`download_rider_waite_simple.sh`** - Simple API-based approach
7. **`download_rider_waite_manual.sh`** - Manual URL list approach

### Manual Download Script

For the Rider-Waite deck, you can use this script (requires wget):

```bash
#!/bin/bash

wikiget() {
    wget -nc -P tarot/rider-waite/cards/ "$1"
}

curl -s "https://commons.wikimedia.org/wiki/Category:Rider-Waite_Tarot_cards" \
| grep -o 'href="[^"]*\.jpg"' \
| sed 's/href="//' \
| sed 's/"//' \
| sed 's/^/https:/' \
| while read -r url; do
    full="${url/\/thumb\//}"
    full="${full%%/256-*/800px-*.jpg}.jpg"
    wikiget "$full"
done
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add new decks with proper attribution
4. Update the README and SOURCES.md files
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Sources and Attribution

All images are sourced from public domain or Creative Commons licensed materials. See [SOURCES.md](SOURCES.md) for detailed attribution information.

## Disclaimer

This repository is for educational and research purposes. All images are used in accordance with their respective licenses and copyright terms. 