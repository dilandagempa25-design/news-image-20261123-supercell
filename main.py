#!/usr/bin/env python3
"""Draw a one-page newspaper summing up Monday 23 November 2026.

Run:  python3 main.py   -> writes entry.png (1024x1024) beside this file.
Only Pillow is required.  All artwork is drawn with PIL primitives and all
text is rendered with system fonts, so the page stays crisp and legible.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
PAPER = (247, 240, 221)
PAPER_DARK = (238, 228, 201)
INK = (24, 24, 24)
GREY = (92, 86, 74)
RED = (178, 34, 40)
BLUE = (35, 78, 128)
GREEN = (42, 112, 74)
GOLD = (176, 126, 24)
PANEL = (255, 252, 244)
LINE = (50, 46, 40)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, fnt):
    box = draw.textbbox((0, 0), s, font=fnt)
    return box[2] - box[0]


def centered(draw, cx, y, s, fnt, fill=INK):
    draw.text((cx - text_w(draw, s, fnt) / 2, y), s, font=fnt, fill=fill)


def wrap(draw, s, fnt, width):
    """Greedy word wrap measured in pixels."""
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, s, fnt, width, leading, fill=INK):
    for line in wrap(draw, s, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- icons
def icon_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=5)
    d.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r], outline=BLUE, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=BLUE, width=3)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 180, fill=BLUE, width=3)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 180, 360, fill=BLUE, width=3)
    # red crack of failure across the globe
    pts = [(cx - r + 8, cy - r + 16), (cx - 8, cy - 6), (cx + 12, cy + 8),
           (cx - 2, cy + 26), (cx + r - 14, cy + r - 12)]
    d.line(pts, fill=RED, width=6, joint="curve")


def icon_ship(d, x, y, s):
    d.polygon([(x, y + 34 * s), (x + 92 * s, y + 34 * s), (x + 76 * s, y + 52 * s),
               (x + 14 * s, y + 52 * s)], fill=INK)
    d.rectangle([x + 34 * s, y + 12 * s, x + 62 * s, y + 34 * s], fill=GREY)
    d.rectangle([x + 44 * s, y, x + 54 * s, y + 12 * s], fill=RED)
    for i in range(3):
        wx = x + 4 * s + i * 30 * s
        d.arc([wx, y + 54 * s, wx + 24 * s, y + 68 * s], 0, 180, fill=BLUE, width=3)


def icon_house(d, x, y, s):
    d.polygon([(x, y + 22 * s), (x + 32 * s, y), (x + 64 * s, y + 22 * s)], fill=RED)
    d.rectangle([x + 8 * s, y + 22 * s, x + 56 * s, y + 54 * s], outline=INK, width=3)
    d.line([x + 14 * s, y + 54 * s, x + 30 * s, y + 38 * s, x + 44 * s, y + 54 * s],
           fill=INK, width=3)
    d.ellipse([x + 24 * s, y + 30 * s, x + 38 * s, y + 44 * s], fill=GOLD)


def icon_chip(d, x, y, s):
    d.rectangle([x + 16 * s, y + 16 * s, x + 64 * s, y + 64 * s], outline=INK, width=4)
    d.rectangle([x + 30 * s, y + 30 * s, x + 50 * s, y + 50 * s], fill=BLUE)
    for i in range(4):
        p = (24 + i * 11) * s
        d.line([x + p, y, x + p, y + 16 * s], fill=INK, width=3)
        d.line([x + p, y + 64 * s, x + p, y + 80 * s], fill=INK, width=3)
        d.line([x, y + p, x + 16 * s, y + p], fill=INK, width=3)
        d.line([x + 64 * s, y + p, x + 80 * s, y + p], fill=INK, width=3)


def icon_plane(d, x, y, s):
    # simple top-view airliner: nose right, swept wings, tail fin
    d.polygon([(x + 88 * s, y + 34 * s), (x + 40 * s, y + 26 * s), (x + 8 * s, y + 26 * s),
               (x, y + 34 * s), (x + 8 * s, y + 42 * s), (x + 40 * s, y + 42 * s)], fill=BLUE)
    d.polygon([(x + 44 * s, y + 28 * s), (x + 24 * s, y + 2 * s), (x + 36 * s, y + 2 * s),
               (x + 56 * s, y + 28 * s)], fill=BLUE)
    d.polygon([(x + 44 * s, y + 40 * s), (x + 24 * s, y + 66 * s), (x + 36 * s, y + 66 * s),
               (x + 56 * s, y + 40 * s)], fill=BLUE)
    d.polygon([(x + 4 * s, y + 28 * s), (x - 6 * s, y + 16 * s), (x + 2 * s, y + 34 * s),
               (x - 6 * s, y + 52 * s), (x + 4 * s, y + 40 * s)], fill=INK)
    d.line([x + 2 * s, y + 76 * s, x + 88 * s, y + 76 * s], fill=RED, width=4)


def icon_controller(d, x, y, s):
    d.rounded_rectangle([x, y + 14 * s, x + 88 * s, y + 56 * s], radius=int(18 * s),
                        outline=INK, width=4)
    d.line([x + 18 * s, y + 28 * s, x + 18 * s, y + 44 * s], fill=INK, width=4)
    d.line([x + 10 * s, y + 36 * s, x + 26 * s, y + 36 * s], fill=INK, width=4)
    for dx, dy, c in [(64, 30, RED), (74, 40, GREEN)]:
        d.ellipse([x + dx * s, y + dy * s, x + (dx + 8) * s, y + (dy + 8) * s], fill=c)


def icon_cross(d, x, y, s):
    d.rectangle([x + 28 * s, y, x + 52 * s, y + 80 * s], fill=RED)
    d.rectangle([x, y + 28 * s, x + 80 * s, y + 52 * s], fill=RED)
    d.ellipse([x + 4 * s, y + 4 * s, x + 76 * s, y + 76 * s], outline=INK, width=3)


def icon_trophy(d, x, y, s):
    d.polygon([(x + 22 * s, y), (x + 58 * s, y), (x + 54 * s, y + 34 * s),
               (x + 26 * s, y + 34 * s)], fill=GOLD)
    d.arc([x + 2 * s, y + 2 * s, x + 26 * s, y + 26 * s], 90, 270, fill=GOLD, width=4)
    d.arc([x + 54 * s, y + 2 * s, x + 78 * s, y + 26 * s], 270, 90, fill=GOLD, width=4)
    d.rectangle([x + 36 * s, y + 34 * s, x + 44 * s, y + 48 * s], fill=GOLD)
    d.rectangle([x + 24 * s, y + 48 * s, x + 56 * s, y + 56 * s], fill=INK)


ICONS = {"ship": icon_ship, "house": icon_house, "chip": icon_chip,
         "plane": icon_plane, "game": icon_controller, "cross": icon_cross,
         "trophy": icon_trophy}


def panel(d, x, y, w, h, tag, headline, summary, icon, tag_color,
          head_size=24, sum_size=19, sum_leading=23):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=LINE, width=2)
    d.rectangle([x, y, x + w, y + 30], fill=tag_color)
    d.text((x + 10, y + 5), tag, font=font(SANS_B, 19), fill=(255, 255, 255))
    ty = block(d, x + 12, y + 38, headline, font(SANS_B, head_size), w - 24,
               head_size + 4)
    # A ruled strip along the bottom belongs to the icon alone, so the
    # summary can use the full width and simply stops above the strip.
    strip_top = y + h - 58
    d.line([x + 10, strip_top, x + w - 10, strip_top], fill=GREY, width=1)
    max_lines = max(1, (strip_top - 6 - (ty + 4)) // sum_leading)
    lines = wrap(d, summary, font(SANS, sum_size), w - 24)[:max_lines]
    sy = ty + 4
    for line in lines:
        d.text((x + 12, sy), line, font=font(SANS, sum_size), fill=(45, 42, 36))
        sy += sum_leading
    ICONS[icon](d, x + w // 2 - 26, strip_top + 5, 0.6)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # page frame
    d.rectangle([14, 14, W - 14, H - 14], outline=INK, width=4)
    d.rectangle([24, 24, W - 24, H - 24], outline=GREY, width=1)

    # ---------------- masthead ----------------
    centered(d, W // 2, 34, "GLOBAL NEWS  •  ONE PAGE  •  ONE DAY", font(SANS_B, 20), GREY)
    centered(d, W // 2, 58, "THE WORLD IN ONE DAY", font(SERIF_B, 57))
    d.rectangle([36, 128, W - 36, 134], fill=RED)
    d.rectangle([36, 140, W - 36, 196], fill=INK)
    centered(d, W // 2, 148, "MONDAY 23 NOVEMBER 2026", font(SERIF_B, 40), (255, 250, 235))
    d.rectangle([36, 202, W - 36, 206], fill=RED)

    # ---------------- lead story ----------------
    lx, ly, lw, lh = 36, 218, W - 72, 248
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=PANEL, outline=LINE, width=3)
    d.rectangle([lx, ly, lx + lw, ly + 34], fill=RED)
    d.text((lx + 12, ly + 6), "LEAD STORY — CLIMATE", font=font(SANS_B, 21), fill=(255, 255, 255))
    ty = block(d, lx + 18, ly + 48, "COP31 TALKS COLLAPSE IN ANTALYA",
               font(SERIF_B, 41), 620, 48)
    block(d, lx + 18, ty + 8,
          "After a 49-hour overrun, an EU-led bloc of 130+ nations rejected a "
          "draft that dropped the fossil-fuel phase-out. UN chief Guterres "
          "lamented the outcome.",
          font(SANS, 24), 620, 30, fill=(45, 42, 36))
    icon_globe(d, lx + lw - 150, ly + 146, 100)
    centered(d, lx + lw - 150, ly + lh - 30, "NO DEAL", font(SANS_B, 22), RED)

    # ---------------- story grid ----------------
    stories_top = [
        ("WAR AT SEA", "UKRAINE DRONES SINK RUSSIAN SHIP",
         "Sea drones sank the warship 'Merkury' in Benghazi port, Libya. "
         "The UN calls for a probe into the port attacks.",
         "ship", BLUE),
        ("UKRAINE", "STRIKES KILL 12 NEAR KYIV",
         "Russian strikes killed at least 12 in the Kyiv region. "
         "A boy of 7 was pulled alive from the rubble.",
         "house", RED),
        ("TECH & CHIPS", "NVIDIA: HUANG BACK, +30%",
         "Jensen Huang returns as CEO; shares jumped about 30%. "
         "US blacklists Megaspeed over AI-chip diversion to China.",
         "chip", INK),
    ]
    stories_bottom = [
        ("TRAVEL", "DELTA GROUNDS ATLANTA",
         "Load-calculation failure forced an FAA ground stop: "
         "1,300 flights delayed, Thanksgiving eve.",
         "plane", BLUE),
        ("GAMES", "GTA VI: $3.79B DAY ONE",
         "'Grand Theft Auto VI' smashed the all-time entertainment "
         "record with its day-one haul.",
         "game", GREEN),
        ("AFRICA", "EBOLA TEAMS TRAPPED IN CONGO",
         "Heavy fighting in Ituri traps Ebola responders near "
         "a hospital, says the WHO.",
         "cross", RED),
        ("SPORT", "UK HOSTS 2035 WORLD CUP",
         "FIFA: UK hosts the 2035 Women's World Cup. Alcaraz beat "
         "Zverev for his first ATP Finals title.",
         "trophy", GOLD),
    ]
    gx, gy, gap = 36, 476, 12
    pw = (W - 72 - 2 * gap) // 3
    for i, s in enumerate(stories_top):
        panel(d, gx + i * (pw + gap), gy, pw, 254, *s)
    pw2 = (W - 72 - 3 * gap) // 4
    for i, s in enumerate(stories_bottom):
        panel(d, gx + i * (pw2 + gap), gy + 264, pw2, 240, *s,
              head_size=20, sum_size=17, sum_leading=21)

    centered(d, W // 2, 984, "All stories verified from the day's reporting — no speculation.",
             font(SERIF, 15), GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
