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
}


def _api_get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


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
            req = urllib.request.Request(ii["url"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            with open(out_path, "wb") as f:
                f.write(data)
            print(f"  OK {local_name}  ({len(data)//1024} KB, {licence})")
            saved += 1
        except Exception as e:
            print(f"  ERROR {local_name}: {e}")
            skipped += 1
        time.sleep(0.2)

    meta = {
        "name": deck["name"],
        "source": "Wikimedia Commons",
        "category": f"https://commons.wikimedia.org/wiki/Category:"
                    + urllib.parse.quote(deck["category"]),
        "note": deck["note"],
        "card_count": len(records),
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
            print(f"  {k:12s} {d['name']} ({len(d['files'])} cards) - {d['note']}")
        return
    download_deck(args.deck, force=args.force)


if __name__ == "__main__":
    main()
