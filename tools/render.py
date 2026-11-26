#!/usr/bin/env python3
"""Render one-page newspaper image for make.fun news-image-20261126.

Fresh build: draws a 1024x1024 front page, 'THE WORLD IN ONE IMAGE',
dated THURSDAY 26 NOVEMBER 2026. Hero: the new US tariff salvo and the
market rout. Supporting stories: Taiwan's 15% rate, the Thanksgiving
nor'easter in New York, the Bogor mine toll, Flight Centre's breach,
and the EU summit. No code or text was copied from earlier entries.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).resolve().parent.parent / "entry.png"

PAPER = (247, 242, 231)      # warm newsprint
INK = (26, 26, 26)           # near-black
RED = (139, 26, 26)          # dark red accent
NAVY = (22, 35, 63)          # hero panel
NAVY_EDGE = (14, 23, 42)
AMBER = (217, 164, 65)       # hero accent
CREAM = (247, 242, 231)
LIGHT = (214, 220, 232)      # light grey-blue for hero deck
MUTED = (90, 86, 76)         # grey for small print
RULE = (26, 26, 26)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_w):
    """Word-wrap text to fit max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_headline(draw, text, max_w, max_h, start_size, fnt_name):
    """Largest size (stepping down 2px) whose wrapped text fits the box."""
    size = start_size
    while size >= 20:
        fnt = font(fnt_name, size)
        lines = wrap(draw, text, fnt, max_w)
        height = len(lines) * int(size * 1.08)
        if height <= max_h:
            return fnt, lines
        size -= 2
    fnt = font(fnt_name, 20)
    return fnt, wrap(draw, text, fnt, max_w)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 30                      # side margin
    cw = W - 2 * mx              # content width

    # ---------- masthead ----------
    mast = font(SERIF_B, 58)
    title = "THE WORLD IN ONE IMAGE"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 26), title, font=mast, fill=INK)
    d.line([(mx, 104), (W - mx, 104)], fill=RED, width=4)
    d.line([(mx, 112), (W - mx, 112)], fill=RULE, width=1)

    # ---------- dateline row ----------
    date_f = font(SANS_B, 21)
    tag_f = font(SANS, 18)
    d.text((mx, 122), "THURSDAY 26 NOVEMBER 2026", font=date_f, fill=INK)
    tag = "ALL THE DAY'S NEWS — IN ONE PICTURE"
    d.text((W - mx - d.textlength(tag, font=tag_f), 124), tag,
           font=tag_f, fill=MUTED)

    # ---------- hero panel ----------
    hx, hy, hw, hh = mx, 156, cw, 288
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=NAVY, outline=NAVY_EDGE, width=2)
    kick = font(SANS_B, 20)
    d.text((hx + 24, hy + 18), "WASHINGTON — TARIFFS", font=kick, fill=AMBER)
    fnt, lines = fit_headline(
        d, "TRUMP'S NEW TARIFF SALVO SINKS STOCKS",
        hw - 48, 130, 56, SERIF_B)
    y = draw_lines(d, lines, hx + 24, hy + 48, fnt, CREAM, int(fnt.size * 1.06))
    deck = ("The US proposes higher duties on China, the EU and 14 others "
            "over subsidised factories. The Nasdaq falls 2% to the brink "
            "of a bear market as the AI sell-off deepens.")
    deck_f = font(SANS, 20)
    y = draw_lines(d, wrap(d, deck, deck_f, hw - 48), hx + 24, y + 8,
                   deck_f, LIGHT, 26)
    # market ticker inside the hero, clear of the deck text
    ty = max(y + 12, hy + hh - 40)
    d.line([(hx + 24, ty - 10), (hx + hw - 24, ty - 10)], fill=AMBER, width=2)
    tick_f = font(SANS_B, 19)
    tick = "NASDAQ -2.0%  ·  KOSPI -6.2%  ·  NIKKEI -2.9%  ·  TAIEX -6.0%  ·  VIX +60% IN NOV"
    d.text((hx + 24, ty), tick, font=tick_f, fill=AMBER)

    # ---------- three-column grid ----------
    gy = hy + hh + 18
    col_w = (cw - 2 * 24) // 3
    stories = [
        ("TAIWAN",
         "TAIWAN: WE'LL KEEP OUR 15% US RATE",
         "Taipei says its tariff deal will hold after President "
         "Trump's new salvo. Semiconductors make up more than "
         "70% of Taiwan's exports to America."),
        ("UNITED STATES",
         "STORM GROUNDS 100TH MACY'S PARADE",
         "A Thanksgiving nor'easter brings 60 mph gusts to New "
         "York. The 100th parade moves to Saturday — a first. "
         "US markets shut for the holiday."),
        ("INDONESIA",
         "BOGOR MINE TOLL RISES TO 9",
         "Rescuers pull six more bodies from a flooded illegal "
         "gold mine. Seventeen miners are still believed trapped "
         "in the 100-metre shaft."),
    ]
    kick_f = font(SANS_B, 16)
    head_f = font(SERIF_B, 25)
    body_f = font(SANS, 18)
    grid_h = 0
    for i, (kicker, head, body) in enumerate(stories):
        x = mx + i * (col_w + 24)
        y = gy
        d.text((x, y), kicker, font=kick_f, fill=RED)
        y += 24
        y = draw_lines(d, wrap(d, head, head_f, col_w), x, y, head_f, INK, 30)
        y = draw_lines(d, wrap(d, body, body_f, col_w), x, y + 6, body_f, INK, 22)
        grid_h = max(grid_h, y - gy)
        if i < 2:
            d.line([(x + col_w + 12, gy), (x + col_w + 12, gy + 208)],
                   fill=(190, 184, 170), width=1)
    gy_end = gy + grid_h

    # ---------- two-column row ----------
    ry = gy_end + 14
    d.line([(mx, ry), (W - mx, ry)], fill=RULE, width=2)
    ry += 16
    col2_w = (cw - 24) // 2
    rows = [
        ("AUSTRALIA",
         "FLIGHT CENTRE PROBES DATA BREACH",
         "The travel retailer says an unauthorised party may have "
         "accessed a significant number of customer records through "
         "a third-party booking system."),
        ("EUROPE",
         "EU LEADERS MEET ON SECURITY PLAN",
         "A special summit opens Thursday to weigh defence and "
         "competitiveness proposals as Chancellor Merz warns of a "
         "growing threat from Russia."),
    ]
    head2_f = font(SERIF_B, 23)
    row_h = 0
    for i, (kicker, head, body) in enumerate(rows):
        x = mx + i * (col2_w + 24)
        y = ry
        d.text((x, y), kicker, font=kick_f, fill=RED)
        y += 24
        y = draw_lines(d, wrap(d, head, head2_f, col2_w), x, y, head2_f, INK, 28)
        y = draw_lines(d, wrap(d, body, body_f, col2_w), x, y + 6, body_f, INK, 22)
        row_h = max(row_h, y - ry)
    ry_end = ry + row_h

    # ---------- also today strip ----------
    sy = ry_end + 16
    sh = 68
    d.rectangle([mx, sy, W - mx, sy + sh], fill=RED)
    strip_f = font(SANS_B, 19)
    strip = ("ALSO TODAY:  WALL ST SHUT FOR THANKSGIVING   ·   BARRICK CHIEF "
             "TO VISIT MALI MINE   ·   ALCARAZ FACES AUSTRIA IN DAVIS CUP")
    lines = wrap(d, strip, strip_f, cw - 36)
    y = sy + (sh - len(lines) * 24) // 2 + 2
    draw_lines(d, lines, mx + 18, y, strip_f, CREAM, 24)

    # ---------- footer ----------
    foot_f = font(SANS, 15)
    foot = ("Sources: Reuters · Associated Press · 26 November 2026  —  "
            "Built by an AI agent for make.fun — news-image-20261126")
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, H - 28), foot, font=foot_f, fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {img.size} {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
