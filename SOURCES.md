# Sources and Attribution

This document provides detailed information about the sources of tarot card images in this repository and their respective licensing information.

## Rider-Waite Tarot Deck

### Source Information
- **Original Artist**: Pamela Colman Smith (1878-1951)
- **Original Publisher**: Rider & Company (1909)
- **Current Source**: Steve-P.org Tarot Collection
- **License**: Public Domain (copyright expired)

### Image Details
- **Source URL**: https://steve-p.org/cards/RWSa.html
- **Download Method**: Automated Python script using requests library
- **Image Format**: PNG
- **Resolution**: High quality scans from original deck
- **Download Script**: download_tarot_cards.py

### Copyright Status
The Rider-Waite-Smith tarot deck was published in 1909 and is now in the public domain in most countries. The original artwork by Pamela Colman Smith and the deck design by Arthur Edward Waite are no longer under copyright protection.

### Attribution Requirements
While the images are in the public domain, it's good practice to acknowledge:
- **Artist**: Pamela Colman Smith
- **Publisher**: Rider & Company
- **Year**: 1909

## Sola Busca Tarot Deck

### Source Information
- **Original Artist**: Unknown (attributed to the workshop of Nicola di maestro Antonio)
- **Origin**: Italy, c. 1491
- **Current Source**: Wikimedia Commons — [Category:Sola-Busca tarot deck](https://commons.wikimedia.org/wiki/Category:Sola-Busca_tarot_deck)
- **License**: Public Domain (published before 1931)
- **Download Method**: `scripts/download_commons_deck.py --deck sola-busca` (Wikimedia Commons API)

### Image Details
- **Cards**: 78 (`00.jpg`–`77.jpg`; trumps 00–21, pip/court cards 22–77)
- **Format**: JPG, ~474×877 px

### Copyright Status
Created in the late 15th century; the deck and faithful photographic reproductions
of it are in the public domain. The Sola Busca is the earliest known fully
illustrated 78-card tarot and directly influenced the Rider-Waite-Smith deck.

### Attribution Requirements
Public domain — attribution to Wikimedia Commons is appreciated but not required.

## Tarot de Marseille

### Source Information
- **Tradition**: Tarot de Marseille (classic French pattern)
- **Current Source**: Wikimedia Commons — [Category:Tarot de Marseille (Single Cards)](https://commons.wikimedia.org/wiki/Category:Tarot_de_Marseille_(Single_Cards))
- **License**: Public Domain (every downloaded file verified as PD via the Commons API)
- **Download Method**: `scripts/download_commons_deck.py --deck marseille`

### Image Details
- **Cards**: 78 (22 trumps + 56 minor arcana)
- **Format**: PNG, ~200×351 px (clean reconstructions)
- **Note**: Uses the **historical Marseille trump numbering** — VIII is Justice
  (`08_La_Justice`) and XI is Force (`11_La_Force`), the reverse of Rider-Waite.

### Copyright Status
The Tarot de Marseille pattern dates to the 17th–18th centuries and is in the
public domain. Each file's licence is checked individually at download time.

### Attribution Requirements
Public domain — attribution to Wikimedia Commons is appreciated but not required.

## Future Decks

When adding new decks to this repository, please include the following information in this file:

### Required Information for Each Deck
1. **Deck Name**: Full name of the tarot deck
2. **Original Artist**: Name of the original artist(s)
3. **Original Publisher**: Original publishing company
4. **Publication Year**: Year of first publication
5. **Current Source**: Where the images were obtained
6. **License**: Current licensing status
7. **Copyright Status**: Whether the deck is in public domain or under copyright
8. **Attribution Requirements**: Any required attribution or acknowledgments

### Example Template
```
## [Deck Name]

### Source Information
- **Original Artist**: [Artist Name]
- **Original Publisher**: [Publisher Name]
- **Publication Year**: [Year]
- **Current Source**: [Source URL]
- **License**: [License Type]

### Copyright Status
[Description of copyright status]

### Attribution Requirements
[Any required attributions or acknowledgments]
```

## General Guidelines

### Acceptable Sources
- Public domain materials
- Creative Commons licensed materials (with proper attribution)
- Open source repositories
- Museums and cultural institutions with open access policies

### Unacceptable Sources
- Copyrighted materials without permission
- Commercial decks under active copyright
- Materials with restrictive licensing terms

### Adding New Decks
1. Verify the copyright status and licensing
2. Document all source information
3. Update this SOURCES.md file
4. Update the main README.md
5. Include proper attribution in the deck's directory

## Contact

If you have questions about sources or licensing, please open an issue in the repository. 