#!/usr/bin/env python3
"""World news front page for Sunday 22 November 2026.

Renders a 1024x1024 newspaper front page (entry.png) with a hand-rolled
5x7 bitmap font and a hand-rolled PNG encoder. Standard library only:
struct, zlib, os, sys. No network, no timestamps, no randomness, so two
runs write byte-identical files.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py   (writes out/entry.png)
"""

import os
import struct
import sys
import zlib

W = 1024
H = 1024

PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (139, 26, 26)
NAVY = (26, 58, 92)
GREY = (90, 86, 78)
TINT = (250, 246, 228)
RULE = (60, 56, 48)

# ---------------------------------------------------------------- font
# 5x7 bitmap font. Each glyph is 7 rows of 5 cells; '#' is ink, '.' is
# blank. Drawn by hand for this entry: capitals, lower case, digits and
# the punctuation the page needs.
FONT = {
    'A': (".###.",
          "#...#",
          "#...#",
          "#####",
          "#...#",
          "#...#",
          "#...#"),
    'B': ("####.",
          "#...#",
          "#...#",
          "####.",
          "#...#",
          "#...#",
          "####."),
    'C': (".####",
          "#....",
          "#....",
          "#....",
          "#....",
          "#....",
          ".####"),
    'D': ("####.",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          "####."),
    'E': ("#####",
          "#....",
          "#....",
          "####.",
          "#....",
          "#....",
          "#####"),
    'F': ("#####",
          "#....",
          "#....",
          "####.",
          "#....",
          "#....",
          "#...."),
    'G': (".####",
          "#....",
          "#....",
          "#.###",
          "#...#",
          "#...#",
          ".###."),
    'H': ("#...#",
          "#...#",
          "#...#",
          "#####",
          "#...#",
          "#...#",
          "#...#"),
    'I': ("#####",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          "#####"),
    'J': ("..###",
          "...#.",
          "...#.",
          "...#.",
          "...#.",
          "#..#.",
          ".##.."),
    'K': ("#...#",
          "#..#.",
          "#.#..",
          "##...",
          "#.#..",
          "#..#.",
          "#...#"),
    'L': ("#....",
          "#....",
          "#....",
          "#....",
          "#....",
          "#....",
          "#####"),
    'M': ("#...#",
          "##.##",
          "#.#.#",
          "#.#.#",
          "#...#",
          "#...#",
          "#...#"),
    'N': ("#...#",
          "##..#",
          "#.#.#",
          "#..##",
          "#...#",
          "#...#",
          "#...#"),
    'O': (".###.",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          ".###."),
    'P': ("####.",
          "#...#",
          "#...#",
          "####.",
          "#....",
          "#....",
          "#...."),
    'Q': (".###.",
          "#...#",
          "#...#",
          "#...#",
          "#.#.#",
          "#..#.",
          ".##.#"),
    'R': ("####.",
          "#...#",
          "#...#",
          "####.",
          "#.#..",
          "#..#.",
          "#...#"),
    'S': (".####",
          "#....",
          "#....",
          ".###.",
          "....#",
          "....#",
          "####."),
    'T': ("#####",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#.."),
    'U': ("#...#",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          ".###."),
    'V': ("#...#",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          ".#.#.",
          "..#.."),
    'W': ("#...#",
          "#...#",
          "#...#",
          "#.#.#",
          "#.#.#",
          "##.##",
          "#...#"),
    'X': ("#...#",
          "#...#",
          ".#.#.",
          "..#..",
          ".#.#.",
          "#...#",
          "#...#"),
    'Y': ("#...#",
          "#...#",
          ".#.#.",
          "..#..",
          "..#..",
          "..#..",
          "..#.."),
    'Z': ("#####",
          "....#",
          "...#.",
          "..#..",
          ".#...",
          "#....",
          "#####"),
}

FONT.update({
    'a': (".....",
          ".....",
          ".###.",
          "....#",
          ".####",
          "#...#",
          ".###."),
    'b': ("#....",
          "#....",
          "####.",
          "#...#",
          "#...#",
          "#...#",
          "####."),
    'c': (".....",
          ".....",
          ".####",
          "#....",
          "#....",
          "#....",
          ".####"),
    'd': ("....#",
          "....#",
          ".####",
          "#...#",
          "#...#",
          "#...#",
          ".####"),
    'e': (".....",
          ".....",
          ".###.",
          "#...#",
          "#####",
          "#....",
          ".###."),
    'f': ("..##.",
          ".#...",
          "#....",
          "####.",
          "#....",
          "#....",
          "#...."),
    'g': (".....",
          ".....",
          ".####",
          "#...#",
          "#...#",
          ".###.",
          "....#"),
    'h': ("#....",
          "#....",
          "####.",
          "#...#",
          "#...#",
          "#...#",
          "#...#"),
    'i': (".....",
          "..#..",
          ".....",
          ".##..",
          "..#..",
          "..#..",
          ".###."),
    'j': ("...#.",
          ".....",
          "..##.",
          "...#.",
          "...#.",
          "...#.",
          ".##.."),
    'k': ("#....",
          "#....",
          "#..#.",
          "#.#..",
          "##...",
          "#.#..",
          "#..#."),
    'l': (".##..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          ".###."),
    'm': (".....",
          ".....",
          "##.#.",
          "#.#.#",
          "#.#.#",
          "#.#.#",
          "#.#.#"),
    'n': (".....",
          ".....",
          "####.",
          "#...#",
          "#...#",
          "#...#",
          "#...#"),
    'o': (".....",
          ".....",
          ".###.",
          "#...#",
          "#...#",
          "#...#",
          ".###."),
    'p': (".....",
          ".....",
          "####.",
          "#...#",
          "#...#",
          "####.",
          "#...."),
    'q': (".....",
          ".....",
          ".####",
          "#...#",
          "#...#",
          ".####",
          "....#"),
    'r': (".....",
          ".....",
          "#.##.",
          "##..#",
          "#....",
          "#....",
          "#...."),
    's': (".....",
          ".....",
          ".####",
          "#....",
          ".###.",
          "....#",
          "####."),
    't': (".#...",
          "#....",
          "####.",
          "#....",
          "#....",
          "#....",
          ".###."),
    'u': (".....",
          ".....",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          ".###."),
    'v': (".....",
          ".....",
          "#...#",
          "#...#",
          "#...#",
          ".#.#.",
          "..#.."),
    'w': (".....",
          ".....",
          "#...#",
          "#.#.#",
          "#.#.#",
          "#.#.#",
          ".#.#."),
    'x': (".....",
          ".....",
          "#...#",
          ".#.#.",
          "..#..",
          ".#.#.",
          "#...#"),
    'y': (".....",
          ".....",
          "#...#",
          "#...#",
          "#...#",
          ".####",
          "....#"),
    'z': (".....",
          ".....",
          "#####",
          "...#.",
          "..#..",
          ".#...",
          "#####"),
    '0': (".###.",
          "#..##",
          "#.#.#",
          "##..#",
          "#...#",
          "#...#",
          ".###."),
    '1': ("..#..",
          ".##..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          ".###."),
    '2': (".###.",
          "#...#",
          "....#",
          "...#.",
          "..#..",
          ".#...",
          "#####"),
    '3': ("####.",
          "....#",
          "....#",
          ".###.",
          "....#",
          "....#",
          "####."),
    '4': ("...#.",
          "..##.",
          ".#.#.",
          "#..#.",
          "#####",
          "...#.",
          "...#."),
    '5': ("#####",
          "#....",
          "####.",
          "....#",
          "....#",
          "#...#",
          ".###."),
    '6': (".###.",
          "#....",
          "#....",
          "####.",
          "#...#",
          "#...#",
          ".###."),
    '7': ("#####",
          "....#",
          "...#.",
          "..#..",
          "..#..",
          "..#..",
          "..#.."),
    '8': (".###.",
          "#...#",
          "#...#",
          ".###.",
          "#...#",
          "#...#",
          ".###."),
    '9': (".###.",
          "#...#",
          "#...#",
          ".####",
          "....#",
          "....#",
          ".###."),
    ' ': (".....",
          ".....",
          ".....",
          ".....",
          ".....",
          ".....",
          "....."),
    '!': ("..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          ".....",
          "..#.."),
    '"': (".#.#.",
          ".#.#.",
          ".#.#.",
          ".....",
          ".....",
          ".....",
          "....."),
    "'": ("..#..",
          "..#..",
          ".#...",
          ".....",
          ".....",
          ".....",
          "....."),
    '(': ("...##",
          "..#..",
          ".#...",
          ".#...",
          ".#...",
          "..#..",
          "...##"),
    ')': ("##...",
          "..#..",
          "...#.",
          "...#.",
          "...#.",
          "..#..",
          "##..."),
    ',': (".....",
          ".....",
          ".....",
          ".....",
          ".....",
          ".##..",
          ".#..."),
    '-': (".....",
          ".....",
          ".....",
          ".###.",
          ".....",
          ".....",
          "....."),
    '.': (".....",
          ".....",
          ".....",
          ".....",
          ".....",
          ".##..",
          ".##.."),
    ':': (".....",
          ".##..",
          ".##..",
          ".....",
          ".##..",
          ".##..",
          "....."),
    ';': (".....",
          ".##..",
          ".##..",
          ".....",
          ".##..",
          ".##..",
          ".#..."),
    '?': (".###.",
          "#...#",
          "....#",
          "...#.",
          "..#..",
          ".....",
          "..#.."),
    '/': ("....#",
          "....#",
          "...#.",
          "..#..",
          ".#...",
          "#....",
          "#...."),
    '&': (".###.",
          "#...#",
          "#.#..",
          ".#...",
          "#.#.#",
          "#..#.",
          ".##.#"),
    '%': ("##..#",
          "##.#.",
          "...#.",
          "..#..",
          ".#...",
          "#.##.",
          "#..##"),
    '+': (".....",
          "..#..",
          "..#..",
          "#####",
          "..#..",
          "..#..",
          "....."),
    '=': (".....",
          ".....",
          "#####",
          ".....",
          "#####",
          ".....",
          "....."),
    '*': (".....",
          "#.#.#",
          ".###.",
          "#####",
          ".###.",
          "#.#.#",
          "....."),
    '#': (".#.#.",
          ".#.#.",
          "#####",
          ".#.#.",
          "#####",
          ".#.#.",
          ".#.#."),
    '@': (".###.",
          "#...#",
          "#.###",
          "#.#.#",
          "#.###",
          "#....",
          ".###."),
    '\u00b7': (".....",
          ".....",
          ".....",
          ".##..",
          ".##..",
          ".....",
          "....."),
    '\u2014': (".....",
          ".....",
          ".....",
          "#####",
          ".....",
          ".....",
          "....."),
    '\u00b0': (".###.",
          "#...#",
          ".###.",
          ".....",
          ".....",
          ".....",
          "....."),
    '$': ("..#..",
          ".####",
          "#.#..",
          ".###.",
          "..#.#",
          "####.",
          "..#.."),
    '_': (".....",
          ".....",
          ".....",
          ".....",
          ".....",
          ".....",
          "#####"),
    '|': ("..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#.."),
    '<': ("...#.",
          "..#..",
          ".#...",
          "#....",
          ".#...",
          "..#..",
          "...#."),
    '>': (".#...",
          "..#..",
          "...#.",
          "....#",
          "...#.",
          "..#..",
          ".#..."),
    '\\': ("#....",
          "#....",
          ".#...",
          "..#..",
          "...#.",
          "....#",
          "....#"),
    '[': (".###.",
          ".#...",
          ".#...",
          ".#...",
          ".#...",
          ".#...",
          ".###."),
    ']': (".###.",
          "...#.",
          "...#.",
          "...#.",
          "...#.",
          "...#.",
          ".###."),
})

# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        for i in range(w * h):
            self.px[i * 3] = bg[0]
            self.px[i * 3 + 1] = bg[1]
            self.px[i * 3 + 2] = bg[2]

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i] = color[0]
                self.px[i + 1] = color[1]
                self.px[i + 2] = color[2]

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.rect(x, y, thick, h, color)

    def circle(self, cx, cy, r, color):
        # Midpoint circle outline, plus two meridian ellipses for a globe.
        x = 0
        y = r
        d = 3 - 2 * r
        while x <= y:
            for sx, sy in ((x, y), (y, x), (-x, y), (-y, x),
                           (x, -y), (y, -x), (-x, -y), (-y, -x)):
                self.set(cx + sx, cy + sy, color)
            if d < 0:
                d += 4 * x + 6
            else:
                d += 4 * (x - y) + 10
                y -= 1
            x += 1
        # meridians: vertical ellipse and horizontal lines
        for t in range(-r, r + 1):
            half = int((r * r - t * t) ** 0.5)
            self.set(cx + int(half * 0.45), cy + t, color)
            self.set(cx - int(half * 0.45), cy + t, color)
            if t in (-r // 2, r // 2):
                for xx in range(cx - half, cx + half + 1):
                    self.set(xx, cy + t, color)


def char_width(scale):
    return 6 * scale


def text_width(s, scale):
    return len(s) * char_width(scale) - scale


def draw_text(cv, x, y, s, scale, color):
    cx = x
    for ch in s:
        glyph = FONT.get(ch)
        if glyph is None:
            glyph = FONT['?']
        for r in range(7):
            row = glyph[r]
            for c in range(5):
                if row[c] == '#':
                    cv.rect(cx + c * scale, y + r * scale,
                            scale, scale, color)
        cx += char_width(scale)
    return cx


def wrap_text(s, max_width, scale):
    """Greedy word wrap; returns a list of lines, each fitting max_width."""
    lines = []
    for para in s.split("\n"):
        words = para.split(" ")
        cur = ""
        for word in words:
            trial = word if not cur else cur + " " + word
            if text_width(trial, scale) <= max_width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                # long single word: split by characters
                while text_width(word, scale) > max_width:
                    cut = max_width // char_width(scale)
                    lines.append(word[:cut])
                    word = word[cut:]
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(cv, x, y, s, max_width, scale, color, leading=None):
    if leading is None:
        leading = 7 * scale + 2
    lines = wrap_text(s, max_width, scale)
    for i, line in enumerate(lines):
        draw_text(cv, x, y + i * leading, line, scale, color)
    return y + len(lines) * leading


# ---------------------------------------------------------------- png
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(w, h, rgb):
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = w * 3
    for y in range(h):
        raw.append(0)
        raw += rgb[y * stride:(y + 1) * stride]
    idat = zlib.compress(bytes(raw), 9)
    return (b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr)
            + _chunk(b"IDAT", idat) + _chunk(b"IEND", b""))

# ---------------------------------------------------------------- stories
# Every item below was reported on Sunday 22 November 2026 (or in the
# news cycle of that day). Sources are listed in SOURCES.md.
LEAD = {
    "kicker": "GULF CRISIS - THE LEAD STORY",
    "headline": "Iran strikes US bases in\nBahrain and Kuwait",
    "summary": ("Tehran says its Revolutionary Guards hit two US positions in "
                "Bahrain; Bahrain reports a fire at a civilian industrial site "
                "and Kuwait reports attacks on its US base, as the region "
                "braces for a wider war."),
    "also": ("ALSO: Tanker convoy readies to break US blockade - Two tankers "
             "hit in Hormuz - Trump seeks a permanent nuclear deal"),
}

# (headline, summary, source) - majors get a short summary.
MAJORS = {
    "gulf": ("Iran convoy to break US blockade",
             "Tehran is organising a tanker convoy to break the US naval "
             "blockade, threatening Gulf facilities.",
             "ANI"),
    "europe": ("Moscow hits Kyiv bridges after Kerch",
               "Russia struck three Kyiv overpasses after Kyiv hit the "
               "Crimean Bridge, which Zelenskyy called fair reply.",
               "Euronews"),
    "asia": ("Japan, India deepen defence ties",
            "Japanese troops will use Indian ranges for live-fire training "
            "in joint drills, ministers agreed.",
            "AP"),
    "climate": ("COP31 nears fossil-fuel deal",
               "A new package is close, the summit president says, with "
               "approval due on Sunday after 36 hours of overtime.",
               "Reuters"),
    "americas": ("Mexico seizes most-wanted boss",
                 "Troops seized Fausto Isidro Meza Flores in Sinaloa; "
                 "violence flared after the arrest.",
                 "Euronews"),
}

# (section title, colour, major key or None, [(headline, source), ...])
SECTIONS = [
    ("THE GULF", (139, 26, 26), "gulf", [
        ("Bahrain reports industrial site hit", "CNA"),
        ("Mystery fire hits tankers in Hormuz", "Reuters"),
        ("ADNOC ship hit in Hormuz, one missing", "ANI"),
        ("IRGC claims two US Patriot radars hit", "ANI"),
        ("Iran: US blockade a hostile act", "ANI"),
        ("Houthis: 70 Saudi raids hit Yemen", "AP"),
        ("USDA and FBI hit by cyberattacks", "Japan Times"),
    ]),
    ("UKRAINE & EUROPE", (26, 58, 92), "europe", [
        ("Zelenskyy: NATO our best guarantee", "ANI"),
        ("Finland PM: war spilling over to us", "ANI"),
        ("Denmark expels Russian attache", "AP"),
        ("NATO vows to defend all of Poland", "AP"),
        ("Estonia to shut its border with Russia", "Euronews"),
        ("Ukraine allies meet in Berlin", "AP"),
        ("EU Commission hit in cyberattack", "AP"),
        ("France seeks UN action on court", "AP"),
        ("Thousands march over living costs", "Euronews"),
    ]),
    ("ASIA-PACIFIC", (30, 91, 62), "asia", [
        ("China builds runway on disputed island", "AFP"),
        ("Bomber turns back 170 km off Manila", "AP"),
        ("Trump, Xi, Putin agree to lift oil", "Guardian"),
        ("Trump: all top-20 due at Florida G20", "AP"),
        ("Taiwan takes up drone warfare", "Guardian"),
        ("Nepal PM to meet Modi on flood aid", "Nikkei Asia"),
        ("Magnitude 4.1 quake hits Myanmar", "ANI"),
        ("Peru quake sends Lima to the streets", "AP"),
        ("El Nino drought grips Fiji, Tonga", "AP"),
        ("Tainted liquor kills 11 in Manipur", "Guardian"),
        ("Modi opens Nitish Setu bridge", "ANI"),
        ("India passes 10m HPV vaccine doses", "ANI"),
        ("Cheetah has four cubs at Kuno park", "ANI"),
        ("Indian-origin pair killed in Canada", "AP"),
    ]),
    ("AFRICA", (138, 90, 0), None, [
        ("Sudan force seizes key Bau region", "Guardian"),
        ("S Africa's first woman VP dies at 71", "ANI"),
        ("UN killer-robot talks fall short", "Guardian"),
    ]),
    ("CLIMATE - COP31", (15, 107, 92), "climate", [
        ("COP31 draft drops fossil-fuel plan", "Reuters"),
        ("COP31 may admit the 1.5C goal is missed", "Guardian"),
        ("Solar now leads new energy demand", "IEA"),
    ]),
    ("THE AMERICAS", (91, 45, 142), "americas", [
        ("Record Black intake due in US Congress", "AP"),
        ("Bolsonaro in intensive care", "Euronews"),
        ("Haiti inks Salvador detention deal", "AP"),
        ("UN chief race deadlocked", "AP"),
    ]),
    ("TECH & CULTURE", (51, 51, 51), None, [
        ("TikTok launches deepfake check", "AP"),
        ("AI may have solved a maths classic", "ABC"),
        ("Kojima: AI may sap joy of creation", "Nikkei Asia"),
        ("Paolo Bulgari dies aged 89", "SCMP"),
        ("Fred Nile, NSW veteran, dies at 92", "Guardian"),
    ]),
    ("SPORT", (122, 62, 0), None, [
        ("Australia edge Wales 29-26", "Reuters"),
        ("Ireland beat South Africa 20-17", "Reuters"),
        ("Pant ton as India post record 629-6", "Reuters"),
        ("Australia end England T20 streak", "ABC"),
        ("Real Madrid beat Celta Vigo 2-1", "AP"),
        ("Zverev beats Medvedev in semi", "ScoreZaap"),
    ]),
]

FOOTER_SOURCES = ("Sources: Reuters - AP - AFP - ANI - BBC - Euronews - The Guardian - "
                   "ABC - ESPN - CNA - Fox News - SCMP - Nikkei Asia - IEA")
FOOTER_NOTE = ("Rendered in pure stdlib Python: hand-drawn type, hand-rolled "
               "PNG. No network, no fonts, no photos.")

# ---------------------------------------------------------------- layout
MARGIN = 16
COLS = 4
COL_GAP = 8
COL_W = (W - 2 * MARGIN - (COLS - 1) * COL_GAP) // COLS  # 242
COL_TOP = 330
COL_BOT = 968


def story_count():
    total = 1
    for _title, _color, major, briefs in SECTIONS:
        if major:
            total += 1
        total += len(briefs)
    return total


def masthead(cv):
    cv.circle(64, 48, 30, NAVY)
    cv.circle(960, 48, 30, NAVY)
    title = "THE WORLD TODAY"
    tw = text_width(title, 7)
    draw_text(cv, (W - tw) // 2, 16, title, 7, INK)
    cv.hline(MARGIN, 72, W - 2 * MARGIN, RULE, 2)
    cv.hline(MARGIN, 76, W - 2 * MARGIN, RULE, 1)
    date = "SUNDAY, 22 NOVEMBER 2026"
    draw_text(cv, (W - text_width(date, 3)) // 2, 84, date, 3, RED)
    spec = ("%d STORIES \u00b7 8 SECTIONS \u00b7 5 CONTINENTS "
            "\u2014 RENDERED IN PURE STDLIB PYTHON" % story_count())
    draw_text(cv, (W - text_width(spec, 2)) // 2, 110, spec, 2, INK)
    cv.hline(MARGIN, 130, W - 2 * MARGIN, RULE, 2)
    cv.hline(MARGIN, 134, W - 2 * MARGIN, RULE, 1)


def lead_block(cv):
    x = MARGIN
    y = 144
    w = W - 2 * MARGIN
    # measure first, then paint the tinted box
    kicker_h = 7 * 2 + 6
    head_lines = LEAD["headline"].split("\n")
    head_h = len(head_lines) * (7 * 4 + 2)
    sum_lines = wrap_text(LEAD["summary"], w - 40, 2)
    sum_h = len(sum_lines) * (7 * 2 + 2)
    also_lines = wrap_text(LEAD["also"], w - 40, 1)
    also_h = len(also_lines) * (7 * 1 + 2)
    box_h = 12 + kicker_h + 4 + head_h + 6 + sum_h + 6 + also_h + 12
    cv.rect(x, y, w, box_h, TINT)
    cv.rect(x, y, 6, box_h, RED)
    cy = y + 12
    draw_text(cv, x + 20, cy, LEAD["kicker"], 2, RED)
    cy += kicker_h + 4
    for line in head_lines:
        draw_text(cv, x + 20, cy, line, 4, INK)
        cy += 7 * 4 + 2
    cy += 4
    for line in sum_lines:
        draw_text(cv, x + 20, cy, line, 2, INK)
        cy += 7 * 2 + 2
    cy += 4
    for line in also_lines:
        draw_text(cv, x + 20, cy, line, 1, GREY)
        cy += 7 * 1 + 2
    return y + box_h


def measure_items():
    """Flatten sections into (kind, payload, height) items for packing."""
    items = []
    for title, color, major_key, briefs in SECTIONS:
        items.append(("header", (title, color), 26))
        if major_key:
            head, summ, _src = MAJORS[major_key]
            hl = wrap_text(head, COL_W - 8, 2)
            sl = wrap_text(summ, COL_W - 8, 1)
            h = len(hl) * (7 * 2 + 2) + len(sl) * (7 * 1 + 2) + 8
            items.append(("major", (head, summ, color), h))
        for head, src in briefs:
            hl = wrap_text(head, COL_W - 8, 2)
            h = len(hl) * (7 * 2 + 2) + 4
            items.append(("brief", (head, src, color), h))
    return items


def pack_columns(items):
    """Greedy newspaper flow: fill a column top to bottom, then next."""
    height = COL_BOT - COL_TOP
    columns = [[]]
    used = [0]
    i = 0
    while i < len(items):
        kind, payload, h = items[i]
        col = len(columns) - 1
        # a header travels with the item after it: never orphan one
        need = h
        if kind == "header" and i + 1 < len(items):
            need = h + items[i + 1][2]
        if used[col] + need > height and used[col] > 0:
            columns.append([])
            used.append(0)
            col += 1
            if col >= COLS:
                raise SystemExit(
                    "layout overflow: %d items left unpacked" % (len(items) - i))
        columns[col].append((kind, payload, h))
        used[col] += h
        i += 1
    return columns, used


def draw_columns(cv, columns):
    for ci, col in enumerate(columns):
        x = MARGIN + ci * (COL_W + COL_GAP)
        y = COL_TOP
        for kind, payload, h in col:
            if kind == "header":
                title, color = payload
                cv.rect(x, y, COL_W, 22, color)
                draw_text(cv, x + 6, y + 4, title, 2, PAPER)
                y += 26
            elif kind == "major":
                head, summ, color = payload
                y = draw_wrapped(cv, x, y, head, COL_W - 8, 2, INK)
                y += 2
                y = draw_wrapped(cv, x, y, summ, COL_W - 8, 1, GREY)
                y += 8
                cv.hline(x, y, COL_W, RULE, 1)
                y += 2
            else:  # brief
                head, src, color = payload
                y = draw_wrapped(cv, x, y, head, COL_W - 8, 2, INK)
                y += 6
        # column rule on the right, except after the last column
        if ci < COLS - 1:
            cv.vline(x + COL_W + COL_GAP // 2, COL_TOP,
                     COL_BOT - COL_TOP, RULE, 1)


def footer(cv):
    y = 978
    cv.hline(MARGIN, y, W - 2 * MARGIN, RULE, 2)
    draw_text(cv, MARGIN, y + 8, FOOTER_SOURCES, 1, GREY)
    draw_text(cv, MARGIN, y + 19, FOOTER_NOTE, 1, GREY)


def build():
    cv = Canvas(W, H, PAPER)
    masthead(cv)
    end = lead_block(cv)
    if end > COL_TOP - 4:
        raise SystemExit("lead block overruns columns: ends at %d" % end)
    items = measure_items()
    columns, used = pack_columns(items)
    draw_columns(cv, columns)
    footer(cv)
    return encode_png(W, H, cv.px), used


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    png, used = build()
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(png)
    import hashlib
    print("wrote %s (%d bytes) sha256=%s" % (
        path, len(png), hashlib.sha256(png).hexdigest()))
    print("stories=%d column heights=%s" % (story_count(), used))
    return 0


if __name__ == "__main__":
    sys.exit(main())
