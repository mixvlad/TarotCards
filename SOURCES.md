# Sources and Attribution

This document provides detailed information about the sources of tarot card images in this repository and their respective licensing information.

## Rider-Waite Tarot Deck

### Source Information
- **Original Artist**: Pamela Colman Smith (1878-1951)
- **Original Publisher**: Rider & Company (1909)
- **Current Source**: Steve-P.org Tarot Collection
- **Scans**: Third-party scans of an original 1909 "Pam-A" deck, cleaned up and restored by Steve P. ([steve-p.org](https://steve-p.org/cards/RWSa.html))
- **License**: Public Domain (copyright expired)

### Image Details
- **Source URL**: https://steve-p.org/cards/RWSa.html
- **Download Method**: One-time download; the images are stored in this repository
- **Image Format**: Lossless PNG originals in `full-png/`; JPG copies (quality 95) in `full/` and `720px/`
- **Resolution**: High quality scans from original deck

### Copyright Status
The Rider-Waite-Smith tarot deck was published in 1909 and is now in the public domain in most countries. The original artwork by Pamela Colman Smith and the deck design by Arthur Edward Waite are no longer under copyright protection.

### Attribution Requirements
While the images are in the public domain, it's good practice to acknowledge:
- **Artist**: Pamela Colman Smith
- **Publisher**: Rider & Company
- **Year**: 1909
- **Scan restoration**: Steve P. (steve-p.org)

## Soimoi Tarot Deck

### Source Information
- **Author**: Mike Koz ([koz.tv](https://koz.tv/))
- **Year**: 2025
- **Method**: Original deck created with a generative image model
- **License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — see [tarot/soimoi/LICENSE](tarot/soimoi/LICENSE)

### Image Details
- **Cards**: 78 (`00_Fool.jpg`–`21_World.jpg`, `{Suit}{01-14}.jpg`) plus `Cover.jpg`
- **Format**: JPG, full resolution and 720px

### Copyright Status
An original deck made for this repository. It is released under CC BY 4.0 and
may be used for any purpose, including commercial projects. Copyright protection
for AI-generated images differs between jurisdictions; to the extent any rights
exist, they are licensed under CC BY 4.0.

### Attribution Requirements
Attribution is required. Suggested credit (an About / Credits screen is fine):

> "Soimoi Tarot" by Mike Koz (https://koz.tv/), licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)

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
- **Format**: PNG, ~813×1536 px (clean reconstructions)
- **Note**: Uses the **historical Marseille trump numbering** — VIII is Justice
  (`08_La_Justice`) and XI is Force (`11_La_Force`), the reverse of Rider-Waite.

### Copyright Status
The Tarot de Marseille pattern dates to the 17th–18th centuries and is in the
public domain. Each file's licence is checked individually at download time.

### Attribution Requirements
Public domain — attribution to Wikimedia Commons is appreciated but not required.

## Grand Etteilla

### Source Information
- **System**: Etteilla (Jean-Baptiste Alliette, 1789) — the first tarot designed for divination
- **Edition**: H. Pussey, Paris, c. 1880–1890
- **Current Source**: Bibliothèque nationale de France (Gallica, `btv1b105111415`) via Wikimedia Commons — [Category:Etteilla I tarot deck](https://commons.wikimedia.org/wiki/Category:Etteilla_I_tarot_deck)
- **License**: Public Domain (every downloaded file verified as PD via the Commons API)
- **Download Method**: `scripts/download_commons_deck.py --deck etteilla`

### Image Details
- **Cards**: 75 of 78, named `NN_<Title>.jpg` with Etteilla's own 1–78 numbering (e.g. `77_Parfait_Contentement.jpg`)
- **Missing**: 49, 63 and 78 (Folie) are not on Commons; 16 and 17 come from a lower-resolution copy of the same edition (800×1416)
- **Format**: JPG, ~1600×2800 px
- **Note**: Not RWS or Marseille — each card carries an upright meaning at the top and a reversed one at the bottom

### Attribution Requirements
Public domain — credit to the Bibliothèque nationale de France / Gallica is appreciated.

## Tarot de Viéville

### Source Information
- **Maker**: Jacques Viéville, Paris, c. 1650
- **Current Source**: Bibliothèque nationale de France (Gallica, `btv1b10510963k`) via Wikimedia Commons — [Category:Jeu de tarot à enseignes italiennes dit "tarot Viéville"](https://commons.wikimedia.org/wiki/Category:Jeu_de_tarot_%C3%A0_enseignes_italiennes_dit_%22tarot_Vi%C3%A9ville%22_-_jeu_de_cartes,_estampe_-_btv1b10510963k)
- **License**: Public Domain
- **Download Method**: `scripts/download_commons_deck.py --deck vieville`

### Image Details
- **Cards**: 78 plus `Cover.jpg`; Marseille-style names (`00_Le_Mat.jpg`, `Cups01.jpg`, …)
- **Format**: JPG, ~1706×3040 px
- **Note**: Files keep the number printed on each card, which differs from Marseille:
  VII is Justice, VIII the Chariot, IX Force and XI the Hermit. Several trumps also have
  their own imagery (XVI is a tree struck by fire rather than a tower, XIX a rider with a banner).

### Attribution Requirements
Public domain — credit to the Bibliothèque nationale de France / Gallica is appreciated.

## Oswald Wirth Tarot

### Source Information
- **Artist**: Oswald Wirth (1860–1943)
- **Origin**: Paris, 1889 ("Les 22 Arcanes du Tarot Kabbalistique")
- **Current Source**: Bibliothèque nationale de France (Gallica) via Wikimedia Commons — [Category:Oswald Wirth tarot deck](https://commons.wikimedia.org/wiki/Category:Oswald_Wirth_tarot_deck)
- **License**: Public Domain (the artist died in 1943)
- **Download Method**: `scripts/download_commons_deck.py --deck oswald-wirth`

### Image Details
- **Cards**: 22 major arcana only (`00_Le_Fou.jpg`–`21_Le_Monde.jpg`)
- **Format**: JPG, ~910×1536 px

### Attribution Requirements
Public domain — credit to the Bibliothèque nationale de France / Gallica is appreciated.

## Tarot Nouveau

### Source Information
- **Publisher**: B.-P. Grimaud, France, 1898
- **Type**: French-suited game tarot (for playing the card game, not for divination)
- **Current Source**: Bibliothèque nationale de France (Gallica, `btv1b10510159t`) via Wikimedia Commons — [Category:Tarot nouveau - Grimaud - 1898](https://commons.wikimedia.org/wiki/Category:Tarot_nouveau_-_Grimaud_-_1898)
- **License**: Public Domain
- **Download Method**: `scripts/download_commons_deck.py --deck tarot-nouveau`

### Image Details
- **Cards**: 78 — `00_Excuse.jpg`, trumps `01_Atout.jpg`–`21_Atout.jpg` (numbered genre scenes), suits `Hearts`, `Diamonds`, `Clubs`, `Spades` `01`–`14` (Jack 11, Knight 12, Queen 13, King 14), plus `Cover.jpg`
- **Format**: JPG, ~1500×2655 px

### Attribution Requirements
Public domain — credit to the Bibliothèque nationale de France / Gallica is appreciated.

## Visconti-Sforza Tarot

### Source Information
- **Artist**: attributed to Bonifacio Bembo (workshop), Milan, c. 1450–1470
- **Originals**: Pierpont Morgan Library (New York), Accademia Carrara (Bergamo) and the Colleoni family
- **Current Source**: Wikimedia Commons — [Category:Pierpont Morgan-Bergamo Visconti-Sforza Tarot](https://commons.wikimedia.org/wiki/Category:Pierpont_Morgan-Bergamo_Visconti-Sforza_Tarot)
- **Scans**: David Madore (2003), scanned from an AGMüller facsimile edition
- **License**: Public Domain
- **Download Method**: `scripts/download_commons_deck.py --deck visconti-sforza`

### Image Details
- **Cards**: 73 of 78, RWS-style names (`00_Fool.jpg`, `Cups01.jpg`, …)
- **Missing**: the Devil, the Tower, the Knight of Coins and the Three of Swords are lost from the original deck; the King of Cups survives but is missing from this scan set
- **Format**: JPG, 512×1024 px

### Copyright Status
The artwork is 15th-century and in the public domain. The files are scans of a modern
facsimile printing; the facsimile's four reconstructed cards (drawn in the 20th century)
are not included.

### Attribution Requirements
Public domain — credit to David Madore for the scans is appreciated.

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