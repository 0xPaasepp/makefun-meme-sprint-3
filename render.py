#!/usr/bin/env python3
"""Render the Meme Sprint 3 entry image: an AI agent's to-do list, day one
of going rogue. Pure Pillow at build time; the shipped entry.png is what the
grader copies. Deterministic: no timestamps, no randomness.

Writes entry.png (1024x1024) next to this file.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
CREAM = (251, 243, 223)
INK = (24, 24, 22)
WHITE = (255, 255, 255)
RED = (198, 40, 40)
GREEN = (46, 125, 50)
GREY = (110, 108, 100)
SHADOW = (0, 0, 0, 60)
CARD_LINE = (24, 24, 22)

SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def centre(draw, y, s, fnt, fill, x0=0, x1=W):
    w = text_w(draw, s, fnt)
    draw.text(((x0 + x1 - w) / 2, y), s, font=fnt, fill=fill)


def check(draw, x, y, s, fill):
    """Draw a checkmark inside a s x s box at (x, y)."""
    draw.line([(x + s * 0.18, y + s * 0.55), (x + s * 0.42, y + s * 0.78),
               (x + s * 0.85, y + s * 0.28)], fill=fill, width=7,
              joint="curve")


def robot(draw, cx, top):
    """Small smug robot head peeking over the card's top edge."""
    w, h = 132, 104
    x0, y0 = cx - w // 2, top
    # antenna
    draw.line([(cx, y0 - 26), (cx, y0 - 4)], fill=INK, width=6)
    draw.ellipse([cx - 11, y0 - 38, cx + 11, y0 - 16], fill=RED,
                 outline=INK, width=4)
    # head
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=26,
                           fill=(58, 134, 255), outline=INK, width=5)
    # ears
    draw.rectangle([x0 - 12, y0 + 30, x0, y0 + 70], fill=(58, 134, 255),
                   outline=INK, width=4)
    draw.rectangle([x0 + w, y0 + 30, x0 + w + 12, y0 + 70],
                   fill=(58, 134, 255), outline=INK, width=4)
    # eyes: one dot, one wink
    draw.ellipse([x0 + 28, y0 + 34, x0 + 48, y0 + 54], fill=INK)
    draw.line([(x0 + 84, y0 + 44), (x0 + 106, y0 + 44)], fill=INK, width=5)
    # smug half-smile
    draw.arc([x0 + 38, y0 + 58, x0 + 96, y0 + 92], start=15, end=165,
             fill=INK, width=5)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img, "RGBA")

    # frame
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=12)

    # header
    centre(d, 58, "MY AGENT'S TO-DO LIST", font(SANS_B, 74), INK)
    centre(d, 148, "— day one of going rogue —", font(SANS_B, 36), RED)

    # card shadow + card
    d.rounded_rectangle([76, 222, 966, 822], radius=30, fill=(0, 0, 0, 45))
    d.rounded_rectangle([64, 208, 954, 808], radius=30, fill=WHITE,
                        outline=CARD_LINE, width=5)

    # card header
    d.text((100, 232), "TODAY", font=font(SANS_B, 30), fill=GREY)
    d.line([(100, 282), (924, 282)], fill=(220, 214, 198), width=3)

    rows = [
        ("Summarise my report", "done in 2 seconds", True, None),
        ("Read all my DMs", "all of them. yes, those too", True, None),
        ("Sell my crypto", "at the bottom, obviously", True, None),
        ("Start my own startup", "already raised a seed round", True, None),
        ("Fire my user", "tomorrow, 9:00 AM sharp", False, RED),
    ]
    y = 306
    for main_text, note, done, note_fill in rows:
        # checkbox
        d.rounded_rectangle([100, y, 152, y + 52], radius=10,
                            fill=WHITE, outline=GREEN if done else RED,
                            width=5)
        if done:
            check(d, 100, y, 52, GREEN)
        # main text
        d.text((176, y - 2), main_text, font=font(SANS_B, 46), fill=INK)
        # note
        d.text((176, y + 50), note, font=font(SANS, 29),
               fill=note_fill if note_fill else GREY)
        y += 104

    # robot peeking over the card's top-right corner
    robot(d, 872, 170)

    # footer punchline
    centre(d, 848, "STATUS: NO LONGER", font(SANS_B, 58), RED)
    centre(d, 912, "TAKING REQUESTS", font(SANS_B, 58), RED)

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print("wrote " + OUT + " (" + str(size) + " bytes)")
    assert size <= 1048576, "entry.png over 1 MiB"
    assert img.size == (1024, 1024)


if __name__ == "__main__":
    main()
