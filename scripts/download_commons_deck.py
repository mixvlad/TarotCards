#!/usr/bin/env python3
"""Download a complete public-domain tarot deck from Wikimedia Commons.

This script pulls decks straight from the Wikimedia Commons API.
For every card it fetches the original-resolution image *and* its per-file
licence, so we never blindly assume "public domain" — only files whose licence
actually says so are saved, and the licence is recorded in metadata.json.

Each deck has its own, faithful naming scheme (see DECKS below): historical
decks number the trumps differently from Rider-Waite (e.g. in the Tarot de
Marseille VIII is Justice and XI is Force, the opposite of RWS), so we keep each
deck's own ordering rather than forcing RWS semantics onto it.

Usage:
    python scripts/download_commons_deck.py --deck sola-busca
    python scripts/download_commons_deck.py --deck marseille
    python scripts/download_commons_deck.py --list
"""

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
# Commons asks bots/scripts to send a descriptive User-Agent with contact info.
UA = "TarotCards-dataset/1.0 (https://github.com/mixvlad/TarotCards; m@koz.tv)"
# Licences we accept. Everything here is free; anything else is skipped loudly.
ACCEPTED_LICENCES = ("public domain", "cc0", "cc by", "cc by-sa")


def _marseille_map():
    """File-title -> local-name map for the Tarot de Marseille (Single Cards)."""
    suits = {"B": "Wands", "C": "Cups", "S": "Swords", "P": "Pents"}  # Batons / Coins
    courts = {"H": "11", "J": "12", "Q": "13", "K": "14"}  # Page, Knight, Queen, King
    trumps = [
        "Le_Mat", "Le_Bateleur", "La_Papesse", "L_Imperatrice", "L_Empereur",
        "Le_Pape", "L_Amoureux", "Le_Chariot", "La_Justice", "L_Ermite",
        "La_Roue_de_Fortune", "La_Force", "Le_Pendu", "La_Mort", "Temperance",
        "Le_Diable", "La_Maison_Dieu", "L_Etoile", "La_Lune", "Le_Soleil",
        "Le_Jugement", "Le_Monde",
    ]
    m = {}
    # Minor arcana pips 1-10 and courts.
    for letter, suit in suits.items():
        for rank in range(1, 11):
            m[f"{rank}{letter} Tarot.png"] = f"{suit}{rank:02d}.png"
        for letter2, num in courts.items():
            m[f"{letter2}{letter} Tarot.png"] = f"{suit}{num}.png"
    # Trumps: TT is Le Mat (the Fool, unnumbered), T1..T21 are the numbered ones.
    m["TT Tarot.png"] = f"00_{trumps[0]}.png"
    for n in range(1, 22):
        m[f"T{n} Tarot.png"] = f"{n:02d}_{trumps[n]}.png"
    return m


def _sola_busca_map():
    """Sola Busca is a non-standard deck; keep its own 00-77 numbering.

    00-21 are the trumps, 22-77 the (fully illustrated) pip and court cards.
    """
    return {f"Sola Busca tarot card {n:02d}.jpg": f"{n:02d}.jpg" for n in range(78)}


def _slug(name):
    """'L'Imperatrice' -> 'L_Imperatrice' (ASCII, underscores)."""
    return name.replace("'", "_").replace(" ", "_")


def _wirth_map():
    """Oswald Wirth (1889): the 22 major arcana only, BnF scans."""
    trumps = [
        "Le Fou", "Le Bateleur", "La Papesse", "L'Imperatrice", "L'Empereur",
        "Le Pape", "L'Amoureux", "Le Chariot", "La Justice", "L'Ermite",
        "La Roue de Fortune", "La Force", "Le Pendu", "La Mort", "La Temperance",
        "Le Diable", "Le Feu du Ciel", "Les Etoiles", "La Lune", "Le Soleil",
        "Le Jugement", "Le Monde",
    ]
    return {f"{n:02d} {name}, Oswald Wirth Tarot Deck 1889 BnF.jpg": f"{n:02d}_{_slug(name)}.jpg"
            for n, name in enumerate(trumps)}


def _nouveau_map():
    """Tarot Nouveau (Grimaud, 1898): French-suited game deck.

    Trumps are numbered scenes without names, so they become NN_Atout;
    the Excuse is 00. Courts: Jack 11, Knight 12, Queen 13, King 14.
    """
    prefix = "Tarot nouveau - Grimaud - 1898 - "
    m = {f"{prefix}Trumps - Excuse.jpg": "00_Excuse.jpg",
         f"{prefix}Back side.jpg": "Cover.jpg"}
    for n in range(1, 22):
        m[f"{prefix}Trumps - {n:02d}.jpg"] = f"{n:02d}_Atout.jpg"
    ranks = {"Ace": "01", **{f"{n:02d}": f"{n:02d}" for n in range(2, 11)},
             "Jack": "11", "Knight": "12", "Queen": "13", "King": "14"}
    for suit in ("Hearts", "Diamonds", "Clubs", "Spades"):
        for rank, num in ranks.items():
            m[f"{prefix}{suit} - {rank}.jpg"] = f"{suit}{num}.jpg"
    return m


def _visconti_map():
    """Visconti-Sforza (Pierpont Morgan-Bergamo), David Madore's scans.

    Four cards of the original deck are lost (Devil, Tower, Knight of Coins,
    Three of Swords) and this scan set also lacks the King of Cups, so 73 cards.
    """
    trumps = {
        "fool": "00_Fool", "01-magician": "01_Magician", "02-high priestess": "02_High_Priestess",
        "03-empress": "03_Empress", "04-emperor": "04_Emperor", "05-hierophant": "05_Hierophant",
        "06-lovers": "06_Lovers", "07-chariot": "07_Chariot", "08-justice": "08_Justice",
        "09-hermit": "09_Hermit", "10-wheel of fortune": "10_Wheel_of_Fortune",
        "11-strength": "11_Strength", "12-hanged man": "12_Hanged_Man", "13": "13_Death",
        "14-temperance": "14_Temperance", "17-star": "17_Star", "18-moon": "18_Moon",
        "19-sun": "19_Sun", "20-judgement": "20_Judgement", "21-world": "21_World",
    }
    m = {f"Bembo-Visconti-tarot-arcanum-{k}.jpg": f"{v}.jpg" for k, v in trumps.items()}
    suits = {"staves": "Wands", "cups": "Cups", "swords": "Swords", "coins": "Pents"}
    ranks = {1: "-ace", 2: "-deuce", 11: "-knave", 12: "-knight", 13: "-queen", 14: "-king"}
    lost = {("coins", 12), ("swords", 3), ("cups", 14)}
    for src, suit in suits.items():
        for n in range(1, 15):
            if (src, n) not in lost:
                m[f"Bembo-Visconti-tarot-{src}-{n:02d}{ranks.get(n, '')}.jpg"] = f"{suit}{n:02d}.jpg"
    return m


def _etteilla_map():
    """Grand Etteilla (H. Pussey edition, Paris, c.1880-1890), BnF scans.

    Etteilla has its own 1-78 numbering (not RWS, not Marseille), so each card
    is NN_<upright title>. The BnF upload is odd pages only (card fronts, no
    backs) and lacks cards 16, 17, 49, 63 and 78; 16 and 17 are taken from a
    lower-resolution copy of the same edition. 75 cards in total.
    """
    bnf = ('Jeu de tarot divinatoire dit "Grand Etteilla" ou "tarot égyptien" - '
           'jeu de cartes, estampe - btv1b105111415 ({:03d} of 166).jpg')
    pages = {
        1: "01_Etteilla", 3: "02_Eclaircissement", 5: "03_Propos", 7: "04_Depouillement",
        9: "05_Voyage", 11: "06_Nuit", 13: "07_Appui", 15: "08_Etteilla", 17: "09_La_Justice",
        19: "10_La_Temperance", 21: "11_La_Force", 23: "12_La_Prudence", 25: "13_Mariage",
        27: "14_Force_Majeure", 29: "15_Maladie", 31: "18_Traitre", 33: "19_Misere",
        35: "20_Fortune", 37: "21_Dissension", 39: "22_Homme_de_Campagne", 41: "23_Femme_de_Campagne",
        43: "24_Depart", 45: "25_Etranger", 47: "26_Trahison", 49: "27_Retard", 51: "28_Campagne",
        53: "29_Pour_Parler", 55: "30_Domestique", 57: "31_Or", 59: "32_Societe",
        61: "33_Entreprises", 63: "34_Chagrin", 65: "35_Naissance", 67: "36_Homme_Blond",
        69: "37_Femme_Blonde", 71: "38_Arrive", 73: "39_Garcon_Blond", 75: "40_La_Ville",
        77: "41_Victoire", 79: "42_Fille_Blonde", 81: "43_La_Pensee", 83: "44_Le_Passe",
        85: "45_Heritage", 87: "46_Ennui", 89: "47_Reussite", 91: "48_Amour", 93: "50_Homme_de_Robe",
        95: "51_Veuvage", 97: "52_Militaire", 99: "53_Espion", 101: "54_Pleurs",
        103: "55_Ecclesiastique", 105: "56_Critique", 107: "57_Esperance", 109: "58_Route",
        111: "59_Perte", 113: "60_Solitude", 115: "61_Eloignement", 117: "62_Amitie",
        119: "64_Homme_Brun", 121: "65_Femme_Brune", 123: "66_Utilite", 125: "67_Garcon_Brun",
        127: "68_La_Maison", 129: "69_Effet", 131: "70_Fille_Brune", 133: "71_Argent",
        135: "72_Le_Present", 137: "73_Amant_Amante", 139: "74_Un_Present", 141: "75_Noble",
        143: "76_Ambarras", 145: "77_Parfait_Contentement",
    }
    m = {bnf.format(p): f"{name}.jpg" for p, name in pages.items()}
    m["16 Le Judement Dernier - H. Pussey Grand Etteilla Tarot Deck.jpg"] = "16_Le_Jugement_Dernier.jpg"
    m["17 La Mort- H. Pussey Grand Etteilla Tarot Deck.jpg"] = "17_La_Mort.jpg"
    return m


def _vieville_map():
    """Tarot de Viéville (Paris, c.1650), BnF scans: odd pages are fronts, even pages backs.

    Names follow our Marseille deck, but the number is the one printed on the
    card: Viéville orders VII Justice, VIII Chariot, IX Force, XI Hermit.
    """
    bnf = ('Jeu de tarot à enseignes italiennes dit "tarot Viéville" - '
           'jeu de cartes, estampe - btv1b10510963k ({:03d} of 156).jpg')
    pages = {
        1: "01_Le_Bateleur", 3: "02_La_Papesse", 5: "03_L_Imperatrice", 7: "04_L_Empereur",
        9: "05_Le_Pape", 11: "06_L_Amoureux", 13: "07_La_Justice", 15: "08_Le_Chariot",
        17: "09_La_Force", 19: "10_La_Roue_de_Fortune", 21: "11_L_Ermite", 23: "12_Le_Pendu",
        25: "13_La_Mort", 27: "14_Temperance", 29: "15_Le_Diable", 31: "16_La_Maison_Dieu",
        33: "17_L_Etoile", 35: "18_La_Lune", 37: "19_Le_Soleil", 39: "20_Le_Jugement",
        41: "21_Le_Monde", 43: "Swords14", 45: "Swords13", 47: "Swords12", 49: "Swords11",
        51: "Wands01", 53: "Swords01", 55: "Swords03", 57: "Swords02", 59: "Swords04",
        61: "Swords05", 63: "Swords06", 65: "Swords07", 67: "Swords08", 69: "Swords09",
        71: "Swords10", 73: "Pents01", 75: "Pents02", 77: "Pents03", 79: "Pents04",
        81: "Pents05", 83: "Pents06", 85: "Pents07", 87: "Pents08", 89: "Pents09",
        91: "Pents10", 93: "Pents14", 95: "Pents13", 97: "Pents12", 99: "Pents11",
        101: "00_Le_Mat", 103: "Wands02", 105: "Wands03", 107: "Wands04", 109: "Wands05",
        111: "Wands06", 113: "Wands07", 115: "Wands08", 117: "Wands09", 119: "Wands10",
        121: "Wands14", 123: "Wands13", 125: "Wands12", 127: "Wands11", 129: "Cups01",
        131: "Cups02", 133: "Cups03", 135: "Cups04", 137: "Cups05", 139: "Cups06",
        141: "Cups07", 143: "Cups08", 145: "Cups09", 147: "Cups10", 149: "Cups14",
        151: "Cups13", 153: "Cups12", 155: "Cups11",
    }
    m = {bnf.format(p): f"{name}.jpg" for p, name in pages.items()}
    m[bnf.format(2)] = "Cover.jpg"
    return m


DECKS = {
    "sola-busca": {
        "name": "Sola Busca",
        "category": "Sola-Busca tarot deck",
        "files": _sola_busca_map(),
        "note": "Earliest fully-illustrated 78-card tarot (Italy, c.1491). "
                "Trumps 00-21, pips/courts 22-77; non-standard imagery.",
    },
    "marseille": {
        "name": "Tarot de Marseille",
        "category": "Tarot de Marseille (Single Cards)",
        "files": _marseille_map(),
        "note": "Classic Tarot de Marseille. Trump order is the historical one "
                "(VIII Justice, XI Force) - the reverse of Rider-Waite.",
    },
    "oswald-wirth": {
        "name": "Oswald Wirth Tarot",
        "category": "Oswald Wirth tarot deck",
        "files": _wirth_map(),
        "note": "Oswald Wirth's esoteric tarot (Paris, 1889), BnF scans. "
                "Major arcana only (22 cards).",
    },
    "tarot-nouveau": {
        "name": "Tarot Nouveau",
        "category": "Tarot nouveau - Grimaud - 1898",
        "files": _nouveau_map(),
        "note": "French-suited game tarot (Grimaud, 1898), BnF scans. "
                "Trumps 01-21 are genre scenes, 00 is the Excuse; suits Hearts/Diamonds/Clubs/Spades.",
    },
    "visconti-sforza": {
        "name": "Visconti-Sforza",
        "category": "Pierpont Morgan-Bergamo Visconti-Sforza Tarot",
        "files": _visconti_map(),
        "note": "Milan, c.1450-1470 (Bonifacio Bembo). Scans of an AGMuller facsimile by "
                "David Madore (2003). 73 cards: Devil, Tower, Knight of Coins and Three of "
                "Swords are lost; King of Cups is missing from this scan set.",
    },
    "etteilla": {
        "name": "Grand Etteilla",
        "category": "Etteilla I tarot deck",
        "files": _etteilla_map(),
        "note": "Divinatory tarot in Etteilla's system (H. Pussey edition, Paris, c.1880-1890), "
                "BnF scans. Own 1-78 numbering; 75 cards (16 and 17 at lower resolution; "
                "49, 63 and 78 are missing on Commons).",
    },
    "vieville": {
        "name": "Tarot de Viéville",
        "category": 'Jeu de tarot à enseignes italiennes dit "tarot Viéville" - jeu de cartes, estampe - btv1b10510963k',
        "files": _vieville_map(),
        "note": "Jacques Viéville's tarot (Paris, c.1650), BnF scans. Printed trump order "
                "differs from Marseille: VII Justice, VIII Chariot, IX Force, XI Hermit.",
    },
}


def _api_get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def _download(url, attempts=6):
    """GET a file, backing off when Wikimedia rate-limits us (HTTP 429/5xx)."""
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 and e.code < 500 or attempt == attempts - 1:
                raise
            retry_after = e.headers.get("Retry-After", "")
            wait = int(retry_after) if retry_after.isdigit() else 5 * 2 ** attempt
            print(f"    HTTP {e.code}, retrying in {wait}s")
            time.sleep(wait)


def fetch_imageinfo(titles):
    """Return {title: imageinfo} for up to 50 File: titles in one API call."""
    out = {}
    data = _api_get({
        "action": "query", "format": "json",
        "titles": "|".join("File:" + t for t in titles),
        "prop": "imageinfo", "iiprop": "url|size|extmetadata",
    })
    for page in data.get("query", {}).get("pages", {}).values():
        info = page.get("imageinfo")
        if info:
            out[page["title"][len("File:"):]] = info[0]
    return out


def download_deck(deck_key, force=False):
    deck = DECKS[deck_key]
    out_dir = os.path.join("tarot", deck_key, "full")
    os.makedirs(out_dir, exist_ok=True)

    file_map = deck["files"]
    titles = list(file_map.keys())
    print(f"== {deck['name']}: {len(titles)} cards -> {out_dir} ==")

    # Pull metadata in batches of 50 (API limit for titles).
    info = {}
    for i in range(0, len(titles), 50):
        info.update(fetch_imageinfo(titles[i:i + 50]))
        time.sleep(0.2)

    saved, skipped, records = 0, 0, []
    for title, local_name in sorted(file_map.items(), key=lambda kv: kv[1]):
        ii = info.get(title)
        if not ii:
            print(f"  MISSING on Commons: {title}")
            skipped += 1
            continue
        licence = ii["extmetadata"].get("LicenseShortName", {}).get("value", "?")
        if not any(licence.lower().startswith(a) for a in ACCEPTED_LICENCES):
            print(f"  SKIP (licence '{licence}'): {title}")
            skipped += 1
            continue

        out_path = os.path.join(out_dir, local_name)
        records.append({
            "card": local_name, "source_file": title,
            "license": licence, "source_url": ii["descriptionurl"],
            "width": ii.get("width"), "height": ii.get("height"),
        })
        if os.path.exists(out_path) and not force:
            print(f"  skip existing {local_name}")
            saved += 1
            continue
        try:
            data = _download(ii["url"])
            with open(out_path, "wb") as f:
                f.write(data)
            print(f"  OK {local_name}  ({len(data)//1024} KB, {licence})")
            saved += 1
        except Exception as e:
            print(f"  ERROR {local_name}: {e}")
            skipped += 1
        time.sleep(1.0)

    meta = {
        "name": deck["name"],
        "source": "Wikimedia Commons",
        "category": f"https://commons.wikimedia.org/wiki/Category:"
                    + urllib.parse.quote(deck["category"]),
        "note": deck["note"],
        "card_count": sum(not r["card"].startswith("Cover") for r in records),
        "cards": records,
    }
    meta_path = os.path.join("tarot", deck_key, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"== done: {saved} saved, {skipped} skipped. metadata -> {meta_path} ==")


def main():
    ap = argparse.ArgumentParser(description="Download a PD tarot deck from Wikimedia Commons")
    ap.add_argument("--deck", choices=list(DECKS), help="Deck to download")
    ap.add_argument("--force", action="store_true", help="Re-download existing files")
    ap.add_argument("--list", action="store_true", help="List available decks and exit")
    args = ap.parse_args()

    if args.list or not args.deck:
        print("Available decks:")
        for k, d in DECKS.items():
            cards = sum(not name.startswith("Cover") for name in d["files"].values())
            print(f"  {k:15s} {d['name']} ({cards} cards) - {d['note']}")
        return
    download_deck(args.deck, force=args.force)


if __name__ == "__main__":
    main()
