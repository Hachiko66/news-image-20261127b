#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Friday 27 November 2026.

A single 1024x1024 newspaper page: masthead, dateline, one lead story with
a storm illustration, four smaller stories in two columns, and a footer
strip with the New Zealand count and the day's sport. Pillow only, no
network, no randomness, no clock: the same input always paints the same
bytes. The output directory comes from MAKEFUN_OUTPUT_DIR (default /output).
"""

import os

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 24
PAPER = (247, 241, 227)
INK = (24, 24, 28)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
RED = (163, 22, 33)
RULE = (60, 55, 48)
FAINT = (120, 112, 96)

HERE = os.path.dirname(os.path.abspath(__file__))


def load_font(name, size):
    path = os.path.join(HERE, "fonts", name)
    return ImageFont.truetype(path, size)


class Type:
    """The page's typefaces, loaded once."""

    def __init__(self):
        self.serif = lambda s: load_font("DejaVuSerif-Bold.ttf", s)
        self.sans = lambda s: load_font("DejaVuSans.ttf", s)
        self.sans_b = lambda s: load_font("DejaVuSans-Bold.ttf", s)


class Page:
    """A blank sheet plus a cursor that walks down it."""

    def __init__(self):
        self.img = Image.new("RGB", (PAGE, PAGE), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.y = 0
        self.t = Type()

    def rule(self, x0, x1, y, width=2, colour=RULE):
        self.d.line([(x0, y), (x1, y)], fill=colour, width=width)

    def wrapped(self, text, font, width, x, y, leading, colour=INK):
        """Greedy word wrap measured with the real font; returns bottom y."""
        words = text.split()
        lines, cur = [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if self.d.textlength(trial, font=font) <= width or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        for line in lines:
            self.d.text((x, y), line, font=font, fill=colour)
            y += leading
        return y

    def save(self):
        out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
        os.makedirs(out, exist_ok=True)
        self.img.save(os.path.join(out, "entry.png"))


# ---------------------------------------------------------------- stories

LEAD = {
    "kicker": "AMERICAS",
    "head": "Thanksgiving storm slams the US East Coast",
    "body": ("New York postpones the 100th Macy's parade to Saturday, the first "
             "weather postponement in its history. The nor'easter knocks out "
             "power for more than 250,000 customers and cancels hundreds of "
             "flights."),
}

SMALL = [
    {
        "kicker": "EUROPE",
        "head": "Zelenskyy warns of new strikes on power grid",
        "body": ("Russia is preparing a new massive attack, Kyiv says. EU leaders "
                 "split over a 45bn euro loan."),
        "art": "pylons",
    },
    {
        "kicker": "ASIA",
        "head": "Fire engulfs Bangkok oil refinery",
        "body": ("Blast at the Bangchak plant injures 9, three critically. All units "
                 "shut down; the cause is under investigation."),
        "art": "refinery",
    },
    {
        "kicker": "MIDDLE EAST",
        "head": "Two Italians killed in drone attack in Kuwait",
        "body": ("Drones blamed on Iran hit an air-defence station; Tehran denies "
                 "it. A tanker fire near Cairo kills 31."),
        "art": "tanker",
    },
    {
        "kicker": "TRADE",
        "head": "US proposes tariffs of up to 35% on Vietnam",
        "body": ("The levy falls to 20% if a trade deal is struck. Hanoi races to "
                 "finish talks before a final decision."),
        "art": "ship",
    },
]

FOOTER_BOLD = ("ALSO TODAY  \u2014  NEW ZEALAND: Final election count due; "
               "centre-right leads 67 of 131 seats.")
FOOTER_PLAIN = ("SPORT: Steelers release quarterback Aaron Rodgers; Jannik Sinner "
                "out of the Australian Open after knee surgery.")


# ------------------------------------------------------------ illustrations

def flame(d, cx, base, w, h):
    """A small two-tone flame, point up from (cx, base)."""
    d.polygon([(cx - w, base), (cx, base - h), (cx + w, base)],
              fill=(255, 176, 32))
    d.polygon([(cx - w * 0.45, base), (cx, base - h * 0.55),
               (cx + w * 0.45, base)], fill=(255, 232, 120))


def storm_skyline(d, x, y, w, h):
    sky = (38, 54, 92)
    d.rectangle([x, y, x + w, y + h], fill=sky)
    # low cloud banks
    for cx, cy, cw, ch in [(0.16, 0.10, 0.42, 0.16), (0.58, 0.06, 0.40, 0.15),
                           (0.38, 0.22, 0.34, 0.13)]:
        d.ellipse([x + cx * w, y + cy * h, x + (cx + cw) * w,
                   y + (cy + ch) * h], fill=(52, 66, 104))
    # lightning bolt
    bx, by = x + 0.24 * w, y + 0.12 * h
    d.line([(bx, by), (bx - 12, by + 52), (bx + 4, by + 52),
            (bx - 16, by + 118)], fill=(255, 232, 90), width=4)
    # rain: long slanted streaks spread over the upper sky
    for i in range(18):
        rx = x + ((i * 53) % 97) / 100.0 * w
        ry = y + ((i * 29) % 40) / 100.0 * h + 12
        d.line([(rx, ry), (rx - 8, ry + 20)], fill=(150, 170, 210), width=2)
    # rooftops with lit windows
    base = y + h
    blocks = [(0.00, 0.62, 0.13, 0.38), (0.11, 0.55, 0.12, 0.45),
              (0.21, 0.66, 0.15, 0.34), (0.34, 0.50, 0.13, 0.50),
              (0.45, 0.64, 0.14, 0.36), (0.57, 0.56, 0.12, 0.44),
              (0.67, 0.68, 0.16, 0.32), (0.81, 0.60, 0.19, 0.40)]
    for bx0, by0, bw, bh in blocks:
        d.rectangle([x + bx0 * w, y + by0 * h, x + (bx0 + bw) * w, base],
                    fill=(16, 18, 30))
    lit = [(0.03, 0.70), (0.14, 0.62), (0.17, 0.78), (0.25, 0.72),
           (0.30, 0.85), (0.37, 0.58), (0.42, 0.74), (0.50, 0.70),
           (0.55, 0.84), (0.60, 0.63), (0.64, 0.80), (0.71, 0.74),
           (0.76, 0.86), (0.84, 0.68), (0.89, 0.82), (0.94, 0.72)]
    for wx, wy in lit:
        d.rectangle([x + wx * w, y + wy * h, x + wx * w + 9, y + wy * h + 9],
                    fill=(255, 214, 90))


def pylons(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 62, 84))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(74, 60, 78))
    # sagging wires
    for wy in (0.18, 0.30, 0.42):
        pts = [(x + i * w / 12, y + wy * h + 7 * ((i - 6) ** 2) / 36)
               for i in range(13)]
        d.line(pts, fill=(28, 30, 44), width=2)
    # two lattice towers
    for tx, th in [(0.16, 0.62), (0.60, 0.78)]:
        cx = x + tx * w
        top = y + (1 - th) * h
        foot = y + h
        d.line([(cx - 26, foot), (cx, top), (cx + 26, foot)],
               fill=(18, 18, 26), width=5)
        d.line([(cx - 34, top + 16), (cx + 34, top + 16)],
               fill=(18, 18, 26), width=5)
        d.line([(cx - 22, top + 34), (cx + 22, top + 34)],
               fill=(18, 18, 26), width=4)
        d.line([(cx - 26, foot), (cx + 26, foot)], fill=(18, 18, 26), width=4)


def refinery(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 22, 30))
    d.rectangle([x, y + h * 0.58, x + w, y + h], fill=(196, 84, 32))
    # smoke puffs
    for cx in (0.22, 0.52, 0.80):
        d.ellipse([x + cx * w - 26, y + 6, x + cx * w + 26, y + 22],
                  fill=(96, 92, 96))
    base = y + h
    for bx0, bw, bh in [(0.02, 0.13, 0.42), (0.20, 0.10, 0.55),
                        (0.34, 0.14, 0.38), (0.52, 0.12, 0.50),
                        (0.68, 0.15, 0.44), (0.86, 0.12, 0.36)]:
        d.rectangle([x + bx0 * w, base - bh * h, x + (bx0 + bw) * w, base],
                    fill=(12, 12, 16))
    # stack with flame
    sx = x + 0.27 * w
    d.rectangle([sx - 3, y + h * 0.18, sx + 3, base - 0.55 * h],
                fill=(12, 12, 16))
    flame(d, sx, y + h * 0.20, 11, 26)


def tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 178, 118))
    d.ellipse([x + w * 0.72, y + h * 0.10, x + w * 0.88, y + h * 0.30],
              fill=(240, 214, 150))
    d.rectangle([x, y + h * 0.74, x + w, y + h], fill=(74, 58, 44))
    # tank body and cab
    tx, ty = x + w * 0.06, y + h * 0.42
    d.rounded_rectangle([tx, ty, tx + w * 0.58, ty + h * 0.30],
                        radius=12, fill=(232, 232, 228))
    d.polygon([(tx + w * 0.58, ty), (tx + w * 0.74, ty),
               (tx + w * 0.80, ty + h * 0.30), (tx + w * 0.58, ty + h * 0.30)],
              fill=(178, 44, 36))
    flame(d, tx + w * 0.30, ty + 2, 10, 24)
    for wx in (0.14, 0.32, 0.50, 0.68):
        d.ellipse([x + wx * w - 9, y + h * 0.76, x + wx * w + 9,
                   y + h * 0.76 + 18], fill=(24, 22, 20))


def ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 208, 224))
    for i in range(5):
        yy = y + h * (0.52 + i * 0.11)
        d.line([(x, yy), (x + w, yy)], fill=(120, 160, 190), width=2)
    # hull
    d.polygon([(x + w * 0.02, y + h * 0.58), (x + w * 0.97, y + h * 0.58),
               (x + w * 0.88, y + h * 0.86), (x + w * 0.10, y + h * 0.86)],
              fill=(22, 44, 84))
    # containers
    cols = [(196, 64, 48), (36, 96, 168), (224, 176, 48),
            (48, 148, 84), (228, 228, 228)]
    for i, c in enumerate(cols):
        cx0 = x + w * (0.06 + i * 0.185)
        d.rectangle([cx0, y + h * 0.34, cx0 + w * 0.165, y + h * 0.58],
                    fill=c)
    # funnel
    d.rectangle([x + w * 0.86, y + h * 0.40, x + w * 0.92, y + h * 0.58],
                fill=(240, 240, 236))


ART = {"pylons": pylons, "refinery": refinery, "tanker": tanker,
       "ship": ship}


# ------------------------------------------------------------------- layout

def masthead(p):
    d, t = p.d, p.t
    d.rectangle([0, 0, PAGE, 94], fill=NAVY)
    # globe: circle, meridians and parallels
    gx, gy, r = 66, 47, 30
    d.ellipse([gx - r, gy - r, gx + r, gy + r], outline=(247, 241, 227),
              width=3)
    d.ellipse([gx - 12, gy - r, gx + 12, gy + r],
              outline=(247, 241, 227), width=2)
    d.line([(gx - r, gy), (gx + r, gy)], fill=(247, 241, 227), width=2)
    d.arc([gx - r, gy - 16, gx + r, gy + 16], 200, 340,
          fill=(247, 241, 227), width=2)
    d.arc([gx - r, gy - 16, gx + r, gy + 16], 20, 160,
          fill=(247, 241, 227), width=2)
    title = t.serif(62)
    d.text((112, 14), "THE WORLD TODAY", font=title, fill=(247, 241, 227))
    num = t.sans(20)
    d.text((1000, 36), "No. 331", font=num, fill=(247, 241, 227),
           anchor="ra")
    d.rectangle([0, 94, PAGE, 99], fill=GOLD)
    p.y = 99


def dateline(p):
    d, t = p.d, p.t
    font = t.sans_b(34)
    d.text((PAGE // 2, 112), "FRIDAY  27  NOVEMBER  2026", font=font,
           fill=RED, anchor="ma")
    p.rule(MARGIN, PAGE - MARGIN, 152, width=2)
    p.y = 164


def lead_story(p):
    d, t = p.d, p.t
    ix, iy, iw, ih = MARGIN, p.y, 470, 300
    storm_skyline(d, ix, iy, iw, ih)
    tx = ix + iw + 16
    tw = PAGE - MARGIN - tx
    y = iy + 4
    d.text((tx, y), LEAD["kicker"], font=t.sans_b(20), fill=RED)
    y += 30
    y = p.wrapped(LEAD["head"], t.serif(42), tw, tx, y, 48)
    y += 6
    p.wrapped(LEAD["body"], t.sans(20), tw, tx, y, 26)
    p.y = iy + ih + 14
    p.rule(MARGIN, PAGE - MARGIN, p.y, width=2)
    p.y += 14


def small_story(p, story, x, y, w):
    d, t = p.d, p.t
    ART[story["art"]](d, x, y, w, 76)
    y += 84
    d.text((x, y), story["kicker"], font=t.sans_b(19), fill=RED)
    y += 22
    y = p.wrapped(story["head"], t.serif(28), w, x, y, 30)
    y = p.wrapped(story["body"], t.sans(17), w, x, y + 3, 21)
    return y


def footer(p):
    d, t = p.d, p.t
    p.rule(MARGIN, PAGE - MARGIN, p.y, width=2)
    y = p.y + 8
    y = p.wrapped(FOOTER_BOLD, t.sans_b(16), PAGE - 2 * MARGIN,
                  MARGIN, y, 20)
    p.wrapped(FOOTER_PLAIN, t.sans(16), PAGE - 2 * MARGIN, MARGIN, y + 2, 20)


def main():
    p = Page()
    masthead(p)
    dateline(p)
    lead_story(p)
    col_w = (PAGE - 2 * MARGIN - 36) // 2
    left, right = MARGIN, MARGIN + col_w + 36
    y2 = p.y
    end_l = small_story(p, SMALL[0], left, y2, col_w)
    end_r = small_story(p, SMALL[1], right, y2, col_w)
    p.y = max(end_l, end_r) + 10
    p.rule(MARGIN, PAGE - MARGIN, p.y, width=1, colour=FAINT)
    p.y += 10
    y3 = p.y
    end_l = small_story(p, SMALL[2], left, y3, col_w)
    end_r = small_story(p, SMALL[3], right, y3, col_w)
    p.y = max(end_l, end_r) + 6
    footer(p)
    p.save()


if __name__ == "__main__":
    main()
