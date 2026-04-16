#!/usr/bin/env python3
"""Process Etsy CSV exports into Astro content collection markdown files."""

import csv
import os
import re
import sys
import time
import json
from pathlib import Path
from urllib.parse import urlparse
import urllib.request
import urllib.error

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "src" / "content" / "products"
IMAGE_DIR = PROJECT_ROOT / "public" / "images" / "products"
CSV_FILES = [
    PROJECT_ROOT / "scripts" / "etsy.csv",
    PROJECT_ROOT / "scripts" / "etsy (1).csv",
    PROJECT_ROOT / "scripts" / "etsy (2).csv",
]

PLACEHOLDER_FILES_TO_DELETE = [
    "hitchhiking-ghosts-baseball-hat.md",
    "patriotic-american-wreath-sash.md",
    "personalized-baby-swaddle.md",
    "white-linen-cocktail-napkins.md",
]

FEATURED_TITLES = {
    "Christmas Pines Turkish Hand Towel",
    "Blue Ticking Wreath Bow",
    "Personalized Baby Swaddle",
    "Mardi Gras Ladder Wreath Sash",
    "Geaux Tiger Wreath Sash",
    "Flowery Flag Baseball Cap",
}


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def clean_etsy_url(url: str) -> str:
    """Strip click_key, click_sum, ref, pf_from, sts, sr_prefetch, sca tracking params."""
    return url.split("?")[0]


def categorize(title: str) -> str:
    t = title.lower()

    if any(kw in t for kw in ["bouquet wrap", "bouquet ribbon", "bouquet sash", "wedding wrap"]):
        return "bouquet-wraps"

    if "cocktail napkin" in t:
        return "cocktail-napkins"

    if any(kw in t for kw in ["wreath sash", "wreath bow", "basket bow", "bow topper", "wreath or basket", "baby banner"]):
        if "baby banner" in t:
            return "baby"
        return "wreath-sashes"

    if any(kw in t for kw in ["hat", "cap", "visor"]):
        return "hats"

    if "towel" in t:
        return "towels"

    if any(kw in t for kw in ["swaddle", "quilt", "infant", "toddler size backpack", "baby "]):
        return "baby"

    if "toddler" in t and any(kw in t for kw in ["princess", "dress", "bear jamboree", "seersucker"]):
        return "childrens-clothing"

    if "christmas wine tote" in t:
        return "towels"

    if any(kw in t for kw in ["dog bandana", "pet collar", "dog collar"]):
        return "pets"

    return "wreath-sashes"


def write_description(title: str) -> str:
    """Return a warm, Southern-toned 2-3 sentence description for a product."""
    t = title.lower()

    templates = {
        "christmas pines turkish hand towel": "Bring a little Christmas into the kitchen. This Turkish hand towel is hand-embroidered with a soft pine design — the kind of detail that turns a sink full of dishes into something that feels like home.",
        "blue ticking wreath bow": "A classic blue ticking stripe bow that brings a little farmhouse charm to your front door. Hand-stitched and finished with care — the kind of detail that makes a plain wreath feel intentional. Works year-round, from spring porches to winter wreaths.",
        "witch linen cocktail napkins": "A little wink of Halloween for your cocktail hour. These linen napkins are hand-embroidered with a witchy design — perfect for October gatherings, spooky soirees, or anyone who loves a seasonal touch that still feels grown-up.",
        "christmas tree bow topper": "The finishing flourish your Christmas tree has been waiting for. Hand-embroidered and sewn to sit pretty at the top, this bow adds a little handmade charm to your holiday — the kind you'll pull out of the storage bin every year with a smile.",
        "red mistletoe wreath bow": "A hand-embroidered bow in classic red with mistletoe detailing — a simple, sweet way to dress up your Christmas wreath. The kind of piece that feels like it's been in the family for years.",
        "flowery flag baseball cap": "Red, white, blue, and a whole lot of charm. This baseball cap features a hand-embroidered floral flag design — patriotic with a softer, prettier twist. Perfect for game days, Fourth of July picnics, or just an everyday good hair day.",
        "patriotic crab baseball cap": "A little Gulf Coast meets Americana. This baseball cap is hand-embroidered with a patriotic crab — red, white, and blue with a coastal wink. Great for beach days, boat days, and long Louisiana summers.",
        "red broad stripes wreath bow": "Bold red stripes, hand-embroidered and tied into a bow that gives any wreath a pop of holiday spirit. Simple, classic, and made with the kind of care you can see in every stitch.",
        "prince charming toddler/infant heirloom quilt": "A hand-embroidered keepsake quilt for your own little prince charming. Soft, sweet, and made to be loved on — the kind of gift that gets dragged around, washed a hundred times, and saved in the cedar chest when they've outgrown it.",
        "personalized baby swaddle": "Wrap your little one in something made just for them. This soft baby swaddle comes hand-embroidered with their name — a gift that new parents hold onto long after the newborn days are over.",
        "nautical theme baby heirloom quilt": "A hand-embroidered heirloom quilt in a sweet nautical theme. Anchors, sailboats, and soft stitching — the kind of baby gift that gets passed down, not put away.",
        "classic baby carriage wreath sash": "A sweet hand-embroidered wreath sash featuring a classic baby carriage. Perfect for baby showers, hospital door hangers, or welcoming a new little one home — stitched with the kind of care you'd put into your own nursery.",
        "split monogram wedding wreath sash": "Dress up your wedding day door with a hand-embroidered split monogram wreath sash. Personalized with the couple's initials and stitched to become a keepsake — the kind of detail that makes a big day feel even more like yours.",
        "mama bear hat": "For the mama who runs the show. This hat is hand-embroidered with a sweet Mama Bear design — perfect for school drop-offs, soccer games, or a ponytail-and-coffee kind of morning.",
        "christmas pines wreath sash": "A soft, hand-embroidered wreath sash with a Christmas pine design. Classic, understated, and the kind of holiday decor that works from Thanksgiving right through New Year's.",
        "tiny bee linen cocktail napkin (set of 4)": "A set of four linen cocktail napkins hand-embroidered with tiny bees — sweet, subtle, and just the right amount of whimsy. Perfect as a hostess gift or a little upgrade for your own bar cart.",
        "damn strait baseball cap": "A little country music, a little attitude. This baseball cap is hand-embroidered with 'Damn Strait' — for the George Strait fans, the country radio faithful, and anyone who wants to wear their playlist on their head.",
        "geaux tiger wreath sash": "Geaux Tigers. This hand-embroidered wreath sash is LSU pride in its purest form — perfect for game days, tailgates, or keeping on the door straight through the season. Made in Louisiana, for Louisiana.",
        "personalized pink linen cocktail napkins": "A set of pink linen cocktail napkins, hand-embroidered with your custom monogram or design. Perfect for bridal showers, hostess gifts, or making your own bar cart feel a little more finished.",
        "monogram bouquet ribbon": "Turn your wedding bouquet into a keepsake. This hand-embroidered ribbon is personalized with a monogram — wrap it around your flowers, and you'll have a piece of the day to keep long after the petals have dried.",
        "christmas wine tote": "A hand-embroidered wine tote in a festive Christmas design — the kind of hostess gift that makes a regular bottle of red feel a little more special. Wrap it up, gift it with the wine inside, and you're done.",
        "princess tiana toddler quilt": "A hand-embroidered heirloom quilt for your little princess. Featuring a sweet Princess Tiana design — a New Orleans favorite, stitched with the kind of care that makes this more than just a blanket.",
        "fall basket pumpkin wreath sash": "A hand-embroidered wreath sash with a sweet fall basket and pumpkin design. Soft, warm, and the kind of autumn decor that works from the first sign of crisp air through Thanksgiving.",
        "st. luke the evangelist, slidell la wreath sash": "A hand-embroidered wreath sash honoring St. Luke the Evangelist in Slidell, Louisiana. Stitched locally, with care — the kind of piece that feels right at home on a parish family's front door.",
        "peeking bunny on seersucker wreath or basket bow": "A peeking bunny hand-embroidered on classic seersucker — sweet, Southern, and the perfect Easter accent for your wreath or basket. Simple, old-fashioned charm in every stitch.",
        "chocolate bunny wreath sash on blue toile": "A hand-embroidered chocolate bunny on a blue toile wreath sash. Easter sweetness with a little vintage charm — the kind of seasonal detail that feels like it was pulled out of your grandmother's linen closet.",
        "steamboat willie baby banner": "A hand-embroidered baby banner featuring classic Steamboat Willie. A sweet nursery keepsake or baby shower gift — stitched in vintage black and white for a timeless Disney nod.",
        "new orleans snowball wreath sash": "A hand-embroidered wreath sash featuring a New Orleans snowball — because down here, shaved ice is practically a food group. A sweet piece of Louisiana summer for your front door.",
        "mardi gras ladder wreath sash": "Throw me something, mister. This hand-embroidered wreath sash celebrates Mardi Gras in full color — purple, green, and gold with ladder and beads detailing. The kind of piece that makes every door on the block feel like it's on the parade route.",
        "personalized nautical theme baby banner": "A hand-embroidered baby banner in a sweet nautical theme, personalized with baby's name. Perfect for nursery walls, baby showers, or photographs you'll actually frame.",
        "bunny with glasses wreath sash": "A hand-embroidered wreath sash featuring the sweetest little bunny in glasses. A whimsical spring addition to your front door — and just the right amount of quirky.",
        "chic thanksgiving turkey wreath sash": "A hand-embroidered wreath sash featuring a chic Thanksgiving turkey. Classic fall colors and the kind of detailed stitching that turns a plain wreath into a seasonal statement piece.",
        "harry potter wreath sash": "For the family that still rereads the series every year. This hand-embroidered wreath sash features a Harry Potter-inspired design — a little bit of magic for your front door.",
        "whimsical pumpkin wreath sash": "A hand-embroidered wreath sash with a whimsical pumpkin design — the perfect balance of fall cozy and a little bit playful. Works all autumn long, from September porch season through Halloween.",
        "groovy cat halloween wreath sash": "A hand-embroidered Halloween wreath sash featuring a groovy cat — retro colors, playful stitching, and the kind of seasonal charm that stands out on a street of plain pumpkins.",
        "let them hat": "For the moms who say 'let them eat cake' — and mean it. This hand-embroidered baseball cap is a little motto, a little vibe, and a whole lot of permission to let kids be kids.",
        "catholic heirloom bouquet sash": "A hand-embroidered bouquet sash honoring the Catholic tradition — stitched to become a keepsake long after the wedding day is over. Personalized, handmade, and made to be kept.",
    }

    if t in templates:
        return templates[t]

    cat = categorize(title)
    generic = {
        "wreath-sashes": f"A hand-embroidered wreath sash featuring {title.lower()} — the kind of detail that turns a plain wreath into something that feels handmade and intentional. Stitched with care in Slidell, Louisiana.",
        "hats": f"A hand-embroidered {title.lower()} — made in Slidell, Louisiana. Stitched with the kind of care that makes a simple cap feel a little more yours.",
        "cocktail-napkins": f"Hand-embroidered linen cocktail napkins — {title.lower()}. The kind of detail that makes a regular gathering feel a little more special. Perfect as a hostess gift or for your own bar cart.",
        "towels": f"Hand-embroidered {title.lower()} — softer and sweeter than anything you'll find at the big box store. Made in Slidell, Louisiana, with care in every stitch.",
        "baby": f"A hand-embroidered {title.lower()} — the kind of baby gift that gets kept forever. Made in Slidell, Louisiana, with the care you'd put into something for your own family.",
        "childrens-clothing": f"A hand-embroidered {title.lower()} — made in Slidell, Louisiana. The kind of keepsake clothing you'll want to photograph before they grow out of it.",
        "bouquet-wraps": f"A hand-embroidered {title.lower()} — a keepsake to turn your wedding bouquet into something you'll hold onto long after the petals have dried.",
        "pets": f"A hand-embroidered {title.lower()} — because your pet deserves the monogram treatment too. Made in Slidell, Louisiana.",
    }
    return generic[cat]


def write_meta_description(title: str, category: str) -> str:
    cat_name = {
        "wreath-sashes": "wreath sash",
        "hats": "hat",
        "cocktail-napkins": "cocktail napkins",
        "towels": "towel",
        "baby": "baby gift",
        "childrens-clothing": "children's piece",
        "bouquet-wraps": "bouquet wrap",
        "pets": "pet accessory",
    }.get(category, "piece")
    desc = f"Hand-embroidered {title}. Handmade in Slidell, Louisiana. Ships nationwide."
    if len(desc) > 155:
        desc = f"Hand-embroidered {cat_name}. Handmade in Slidell, Louisiana."
    return desc


def write_alt_text(title: str, category: str) -> str:
    cat_desc = {
        "wreath-sashes": "wreath sash",
        "hats": "hat",
        "cocktail-napkins": "linen cocktail napkins",
        "towels": "kitchen towel",
        "baby": "baby item",
        "childrens-clothing": "children's clothing piece",
        "bouquet-wraps": "bouquet wrap",
        "pets": "pet accessory",
    }.get(category, "item")
    return f"Hand-embroidered {cat_desc} — {title} by Slidell Stitches"


def upgrade_image_url(url: str, size: str = "1588xN") -> str:
    """Replace il_340x270 with il_{size}."""
    return re.sub(r"il_\d+x\d+", f"il_{size}", url)


def download_image(url: str, dest: Path) -> bool:
    """Download an image, trying progressively larger sizes. Returns True on success."""
    if dest.exists():
        return True

    sizes = ["1588xN", "794xN", "680xN", "340x270"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.etsy.com/",
    }
    for size in sizes:
        try_url = upgrade_image_url(url, size)
        try:
            req = urllib.request.Request(try_url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status == 200:
                    data = resp.read()
                    dest.write_bytes(data)
                    return True
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            continue
    return False


def escape_yaml_string(s: str) -> str:
    return s.replace('"', '\\"')


def write_markdown(slug: str, product: dict) -> Path:
    md_path = CONTENT_DIR / f"{slug}.md"
    frontmatter = f"""---
name: "{escape_yaml_string(product['name'])}"
price: {product['price']}
image: "/images/products/{slug}.jpg"
image_alt: "{escape_yaml_string(product['image_alt'])}"
category: "{product['category']}"
etsy_url: "{product['etsy_url']}"
featured: {str(product['featured']).lower()}
in_stock: true
description: "{escape_yaml_string(product['description'])}"
meta_description: "{escape_yaml_string(product['meta_description'])}"
---
"""
    md_path.write_text(frontmatter)
    return md_path


def main():
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    # Delete placeholder files
    for filename in PLACEHOLDER_FILES_TO_DELETE:
        path = CONTENT_DIR / filename
        if path.exists():
            path.unlink()
            print(f"  [delete] {filename}")

    # Load and merge all CSVs
    seen_urls = set()
    products = []
    for csv_path in CSV_FILES:
        if not csv_path.exists():
            print(f"  [skip] {csv_path.name} (not found)")
            continue
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = clean_etsy_url(row["listing-link href"])
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                products.append({
                    "etsy_url": url,
                    "image_url": row["wt-width-full src"],
                    "name": row["wt-text-caption"].strip(),
                    "price": float(row["currency-value"]),
                })

    print(f"\nTotal unique products from {len(CSV_FILES)} CSVs: {len(products)}\n")

    stats = {"markdown": 0, "images_ok": 0, "images_failed": []}
    for i, p in enumerate(products, 1):
        slug = slugify(p["name"])
        if not slug:
            print(f"  [{i:3}] SKIP (no slug) — {p['name']}")
            continue

        category = categorize(p["name"])
        p["category"] = category
        p["featured"] = p["name"] in FEATURED_TITLES
        p["description"] = write_description(p["name"])
        p["meta_description"] = write_meta_description(p["name"], category)
        p["image_alt"] = write_alt_text(p["name"], category)

        img_path = IMAGE_DIR / f"{slug}.jpg"
        ok = download_image(p["image_url"], img_path)
        if ok:
            stats["images_ok"] += 1
        else:
            stats["images_failed"].append(p["name"])

        write_markdown(slug, p)
        stats["markdown"] += 1
        print(f"  [{i:3}] {category:18} {p['name'][:60]}")
        time.sleep(0.4)

    print(f"\n=== Summary ===")
    print(f"  Markdown files written: {stats['markdown']}")
    print(f"  Images downloaded:      {stats['images_ok']}")
    if stats["images_failed"]:
        print(f"  Failed images:          {len(stats['images_failed'])}")
        for name in stats["images_failed"]:
            print(f"    - {name}")


if __name__ == "__main__":
    main()
