#!/usr/bin/env python3
"""Draw a newspaper front page summing up the world news of Friday
27 November 2026 and write it to /output/entry.png.

Pure stdlib + Pillow, no network, fully deterministic: fixed layout,
fixed palette, no randomness, no timestamps.

Stories (verified against live news reporting on 27 Nov 2026):
- Thanksgiving nor'easter slams the US East Coast; the 100th Macy's
  parade is postponed to Saturday, the first weather postponement in
  its history; power out for 250,000+ customers.
- Zelenskyy warns Russia is preparing a new massive strike on
  Ukraine's power grid; EU leaders split over a 45bn euro loan.
- Explosion and fire at Bangkok's Bangchak refinery: 9 injured,
  three critically; all units shut down.
- Two Italian technicians killed in a drone attack in Kuwait blamed
  on Iran (Tehran denies it); a tanker fire near Cairo kills 31.
- The US proposes tariffs of up to 35% on Vietnamese goods, falling
  to 20% if a trade deal is struck.
- New Zealand's final election count is due; the centre-right
  coalition leads 67 of 131 seats on the preliminary tally.
- Sport: Steelers release Aaron Rodgers; Jannik Sinner is out of the
  Australian Open after knee surgery.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (248, 243, 232)
INK = (24, 24, 24)
NAVY = (20, 33, 58)
NAVY2 = (44, 62, 96)
RED = (172, 36, 24)
GOLD = (198, 158, 38)
SLATE = (58, 74, 99)
BODY = (62, 62, 58)
FAINT = (188, 184, 170)

_HERE = os.path.dirname(os.path.abspath(__file__))


def font(name, size):
    """Load a bundled DejaVu font, falling back to the system copy."""
    for path in (
        os.path.join(_HERE, "fonts", name),
        os.path.join("/usr/share/fonts/truetype/dejavu", name),
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def wrap_text(d, text, f, width):
    """Greedy word wrap; returns a list of lines fitting width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, color, width, leading, max_lines=None):
    """Draw wrapped paragraph; return y below the last line. When
    max_lines is set, never draw more than that many lines."""
    lines = wrap_text(d, text, f, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=f, fill=color)
        y += leading
    return y


def kicker(d, x, y, label, color=RED):
    """Small red region label; return y below it."""
    d.text((x, y), label, font=sans_b(18), fill=color)
    return y + 25


# ------------------------------------------------------------------ art

def art_storm(d, x0, y0, w, h):
    """Nor'easter over a city: darkening sky, cloud bank, rain, lit
    windows, one fork of lightning."""
    steps = 20
    for i in range(steps):
        t = i / (steps - 1)
        col = tuple(int(NAVY2[c] + (NAVY[c] - NAVY2[c]) * t) for c in range(3))
        d.rectangle([x0, y0 + i * h // steps, x0 + w,
                     y0 + (i + 1) * h // steps], fill=col)
    # cloud bank (kept inside the frame)
    for cx, cy, rx, ry in ((0.20, 0.16, 0.17, 0.08), (0.55, 0.10, 0.22, 0.09),
                           (0.84, 0.18, 0.13, 0.07), (0.40, 0.24, 0.14, 0.06)):
        d.ellipse([x0 + (cx - rx) * w, y0 + (cy - ry) * h,
                   x0 + (cx + rx) * w, y0 + (cy + ry) * h], fill=(50, 60, 82))
    # lightning
    bolt = [(0.30, 0.14), (0.22, 0.40), (0.28, 0.40),
            (0.18, 0.66), (0.28, 0.38), (0.22, 0.38)]
    d.polygon([(x0 + bx * w, y0 + by * h) for bx, by in bolt],
              fill=(248, 216, 76))
    # rain strokes, fixed pattern
    for i in range(52):
        rx = x0 + ((i * 89) % 100) / 100.0 * w
        ry = y0 + h * 0.28 + ((i * 47) % 100) / 100.0 * h * 0.60
        d.line([rx, ry, rx - 6, ry + 14], fill=(148, 168, 204), width=2)
    # skyline
    base = y0 + h
    towers = [(0.00, 0.55, 0.12, 0.27), (0.12, 0.66, 0.10, 0.16),
              (0.22, 0.50, 0.12, 0.32), (0.34, 0.60, 0.11, 0.22),
              (0.45, 0.46, 0.12, 0.36), (0.57, 0.62, 0.10, 0.20),
              (0.67, 0.52, 0.12, 0.30), (0.79, 0.66, 0.10, 0.16),
              (0.89, 0.58, 0.11, 0.24)]
    for bx, by, bw, bh in towers:
        d.rectangle([x0 + bx * w, y0 + by * h,
                     x0 + (bx + bw) * w, base], fill=(14, 20, 34))
        for wx in range(2):
            for wy in range(3):
                if (int(bx * 100) + wx * 5 + wy * 2) % 3 == 0:
                    d.rectangle(
                        [x0 + (bx + 0.025 + wx * 0.05) * w,
                         y0 + (by + 0.04 + wy * 0.10) * h,
                         x0 + (bx + 0.05 + wx * 0.05) * w,
                         y0 + (by + 0.075 + wy * 0.10) * h],
                        fill=(248, 216, 76))
    d.rectangle([x0, base - 3, x0 + w, base], fill=(14, 20, 34))


def art_pylon(d, x0, y0, w, h):
    """Electricity pylon against a grey dusk sky."""
    for i in range(10):
        t = i / 9
        shade = int(88 - 52 * t)
        d.rectangle([x0, y0 + i * h // 10, x0 + w,
                     y0 + (i + 1) * h // 10],
                    fill=(shade, shade + 7, shade + 22))
    d.rectangle([x0, y0 + h * 0.80, x0 + w, y0 + h], fill=(104, 90, 100))
    cx = x0 + w * 0.68
    top, bot = y0 + h * 0.08, y0 + h
    d.polygon([(cx - 4, top), (cx + 4, top), (cx + 26, bot), (cx + 12, bot)],
              fill=INK)
    d.polygon([(cx - 4, top), (cx + 4, top), (cx - 12, bot), (cx - 26, bot)],
              fill=INK)
    for ay in (0.18, 0.34):
        yy = y0 + h * ay
        d.rectangle([cx - w * 0.22, yy - 3, cx + w * 0.22, yy + 3], fill=INK)
        d.line([x0, yy + 12, cx - w * 0.22, yy + 4], fill=INK, width=2)
        d.line([cx + w * 0.22, yy + 4, x0 + w, yy + 12], fill=INK, width=2)
    # smaller pylon in the distance
    cx2 = x0 + w * 0.16
    d.polygon([(cx2 - 3, y0 + h * 0.38), (cx2 + 3, y0 + h * 0.38),
               (cx2 + 11, bot), (cx2 + 4, bot)], fill=(42, 42, 46))
    d.polygon([(cx2 - 3, y0 + h * 0.38), (cx2 + 3, y0 + h * 0.38),
               (cx2 - 4, bot), (cx2 - 11, bot)], fill=(42, 42, 46))
    d.rectangle([cx2 - w * 0.09, y0 + h * 0.44,
                 cx2 + w * 0.09, y0 + h * 0.44 + 3], fill=(42, 42, 46))


def art_refinery(d, x0, y0, w, h):
    """Refinery towers, smoke and flame at night."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(36, 32, 38))
    # heat glow at the base
    for i in range(9):
        t = i / 8
        d.rectangle([x0, y0 + h - (i + 1) * h // 20, x0 + w,
                     y0 + h - i * h // 20],
                    fill=(196 - int(84 * t), 88 - int(38 * t), 28))
    # smoke
    for sx, sy, sr in ((0.30, 0.10, 0.08), (0.52, 0.07, 0.09),
                       (0.74, 0.12, 0.07)):
        d.ellipse([x0 + (sx - sr) * w, y0 + (sy - sr) * h,
                   x0 + (sx + sr) * w, y0 + (sy + sr) * h],
                  fill=(118, 114, 116))
    # towers
    for tx, tw, th in ((0.08, 0.11, 0.58), (0.24, 0.13, 0.74),
                       (0.44, 0.10, 0.52), (0.60, 0.14, 0.66),
                       (0.80, 0.10, 0.46)):
        d.rectangle([x0 + tx * w, y0 + h * (1 - th),
                     x0 + (tx + tw) * w, y0 + h], fill=(18, 16, 20))
        d.rectangle([x0 + tx * w, y0 + h * (1 - th) - 5,
                     x0 + (tx + tw) * w, y0 + h * (1 - th)],
                    fill=(58, 54, 58))
    # flame on the tallest tower
    fx, fy = x0 + w * 0.305, y0 + h * 0.28
    d.polygon([(fx - 12, fy + 14), (fx, fy - 12), (fx + 12, fy + 14)],
              fill=(246, 158, 38))
    d.polygon([(fx - 6, fy + 14), (fx, fy + 2), (fx + 6, fy + 14)],
              fill=(248, 216, 76))


def art_tanker(d, x0, y0, w, h):
    """Fuel tanker on a desert road at dusk, flame above the tank."""
    d.rectangle([x0, y0, x0 + w, y0 + h * 0.60], fill=(212, 156, 90))
    d.ellipse([x0 + w * 0.76, y0 + h * 0.08,
               x0 + w * 0.90, y0 + h * 0.32], fill=(240, 192, 112))
    d.rectangle([x0, y0 + h * 0.60, x0 + w, y0 + h], fill=(166, 126, 82))
    d.rectangle([x0, y0 + h * 0.78, x0 + w, y0 + h], fill=(58, 54, 50))
    ty = y0 + h * 0.48
    d.rounded_rectangle([int(x0 + w * 0.10), int(ty), int(x0 + w * 0.58),
                         int(ty + h * 0.26)], radius=9, fill=(204, 204, 200))
    d.rectangle([x0 + w * 0.10, ty + h * 0.09,
                 x0 + w * 0.58, ty + h * 0.13], fill=(168, 168, 164))
    d.polygon([(x0 + w * 0.58, ty + h * 0.03), (x0 + w * 0.68, ty + h * 0.03),
               (x0 + w * 0.73, ty + h * 0.26), (x0 + w * 0.58, ty + h * 0.26)],
              fill=(168, 38, 28))
    for wx in (0.16, 0.32, 0.44):
        d.ellipse([x0 + w * wx, ty + h * 0.24,
                   x0 + w * (wx + 0.05), ty + h * 0.36], fill=INK)
    d.ellipse([x0 + w * 0.64, ty + h * 0.24,
               x0 + w * 0.69, ty + h * 0.36], fill=INK)
    fx, fy = x0 + w * 0.34, ty - h * 0.10
    d.polygon([(fx - 14, fy + 12), (fx, fy - 16), (fx + 14, fy + 12)],
              fill=(246, 158, 38))
    d.polygon([(fx - 6, fy + 12), (fx, fy - 2), (fx + 6, fy + 12)],
              fill=(248, 216, 76))


def art_ship(d, x0, y0, w, h):
    """Container ship on the sea under a pale sky."""
    d.rectangle([x0, y0, x0 + w, y0 + h * 0.52], fill=(194, 212, 226))
    d.rectangle([x0, y0 + h * 0.52, x0 + w, y0 + h], fill=(42, 82, 118))
    for wy in (0.60, 0.72, 0.84):
        d.line([x0, y0 + h * wy, x0 + w, y0 + h * wy],
               fill=(118, 158, 188), width=2)
    d.polygon([(x0 + w * 0.05, y0 + h * 0.60), (x0 + w * 0.95, y0 + h * 0.60),
               (x0 + w * 0.87, y0 + h * 0.80), (x0 + w * 0.13, y0 + h * 0.80)],
              fill=(28, 42, 64))
    cols = [(198, 68, 48), (38, 108, 158), (218, 158, 38), (58, 138, 88)]
    for i, col in enumerate(cols):
        cx = x0 + w * (0.13 + i * 0.19)
        d.rectangle([cx, y0 + h * 0.38, cx + w * 0.16, y0 + h * 0.60],
                    fill=col)
        d.rectangle([cx, y0 + h * 0.38, cx + w * 0.16, y0 + h * 0.42],
                    fill=(252, 252, 248))
    d.rectangle([x0 + w * 0.87, y0 + h * 0.32,
                 x0 + w * 0.94, y0 + h * 0.60], fill=(238, 238, 234))


def art_globe(d, cx, cy, r):
    """Small line-art globe for the masthead."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(250, 246, 236),
              width=3)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=(250, 246, 236), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(250, 246, 236), width=2)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
          start=200, end=340, fill=(250, 246, 236), width=2)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
          start=20, end=160, fill=(250, 246, 236), width=2)


# ------------------------------------------------------------------ page

def grid_story(d, x, y, w, art, region, headline, body):
    """One grid story: art strip, kicker, headline, two body lines."""
    art(d, x, y, w, 80)
    y += 88
    y = kicker(d, x, y, region)
    y = para(d, x, y, headline, serif_b(24), INK, w, 28)
    y += 2
    para(d, x, y, body, sans(17), BODY, w, 20, max_lines=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 96], fill=NAVY)
    art_globe(d, 78, 48, 26)
    d.text((122, 48), "THE WORLD TODAY", font=serif_b(56),
           fill=(250, 246, 236), anchor="lm")
    d.text((W - 24, 48), "No. 331", font=sans(20),
           fill=(200, 196, 180), anchor="rm")
    d.rectangle([0, 96, W, 100], fill=GOLD)

    # ---- date bar
    d.text((W // 2, 122), "FRIDAY  27  NOVEMBER  2026", font=sans_b(30),
           fill=RED, anchor="mm")
    d.line([24, 146, W - 24, 146], fill=INK, width=2)

    # ---- lead story: Thanksgiving storm
    art_storm(d, 24, 158, 470, 306)
    lx = 518
    y = 164
    y = kicker(d, lx, y, "AMERICAS")
    y = para(d, lx, y, "Thanksgiving storm slams the US East Coast",
             serif_b(38), INK, 482, 46)
    y += 8
    para(d, lx, y,
         "New York postpones the 100th Macy's parade to Saturday, the "
         "first weather postponement in its history. The nor'easter "
         "knocks out power for more than 250,000 customers and cancels "
         "hundreds of flights.",
         sans(21), BODY, 482, 27)
    d.line([24, 480, W - 24, 480], fill=INK, width=2)

    # ---- grid row 1
    grid_story(d, 24, 494, 476, art_pylon, "EUROPE",
               "Zelenskyy warns of new strikes on power grid",
               "Russia is preparing a new massive attack, Kyiv says. "
               "EU leaders split over a 45bn euro loan.")
    grid_story(d, 524, 494, 476, art_refinery, "ASIA",
               "Fire engulfs Bangkok oil refinery",
               "Blast at the Bangchak plant injures 9, three critically. "
               "All units shut down; the cause is under investigation.")
    d.line([24, 712, W - 24, 712], fill=FAINT, width=1)

    # ---- grid row 2
    grid_story(d, 24, 726, 476, art_tanker, "MIDDLE EAST",
               "Two Italians killed in drone attack in Kuwait",
               "Drones blamed on Iran hit an air-defence station; Tehran "
               "denies it. A tanker fire near Cairo kills 31.")
    grid_story(d, 524, 726, 476, art_ship, "TRADE",
               "US proposes tariffs of up to 35% on Vietnam",
               "The levy falls to 20% if a trade deal is struck. Hanoi "
               "races to finish talks before a final decision.")
    d.line([24, 944, W - 24, 944], fill=INK, width=2)

    # ---- footer: New Zealand + sport
    d.text((24, 954),
           "ALSO TODAY  \u2014  NEW ZEALAND: Final election count due; the "
           "centre-right coalition leads 67 of 131 seats.",
           font=sans_b(15), fill=INK)
    d.text((24, 976),
           "SPORT: Steelers release quarterback Aaron Rodgers; Jannik Sinner "
           "out of the Australian Open after knee surgery.",
           font=sans(14), fill=BODY)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "entry.png"), format="PNG")


if __name__ == "__main__":
    main()
