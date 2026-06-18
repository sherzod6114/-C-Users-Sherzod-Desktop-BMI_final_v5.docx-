# -*- coding: utf-8 -*-
"""Himoyaga to'liq tayyor, professional prezentatsiya generatori."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image

# ===================== DIZAYN TIZIMI =====================
NAVY   = RGBColor(0x0A, 0x25, 0x40)   # asosiy quyuq
NAVY2  = RGBColor(0x10, 0x33, 0x57)
BLUE   = RGBColor(0x25, 0x63, 0xEB)   # urg'u
TEAL   = RGBColor(0x0E, 0xA5, 0xA4)
GREEN  = RGBColor(0x16, 0xA3, 0x4A)
AMBER  = RGBColor(0xF5, 0x9E, 0x0B)
RED    = RGBColor(0xDC, 0x26, 0x26)
PURPLE = RGBColor(0x7C, 0x3A, 0xED)
SLATE  = RGBColor(0x47, 0x55, 0x69)
LIGHT  = RGBColor(0xF1, 0xF5, 0xFB)
CARD   = RGBColor(0xE8, 0xEE, 0xF7)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
MUTED  = RGBColor(0x9F, 0xB4, 0xD6)
INK    = RGBColor(0x1F, 0x2A, 0x3A)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

TOTAL = 23  # slaydlar soni (footer uchun)


def slide():
    return prs.slides.add_slide(BLANK)


def no_shadow(sp):
    sp.shadow.inherit = False


def rect(s, x, y, w, h, color, line=None, lw=1.0, shape=MSO_SHAPE.RECTANGLE):
    sp = s.shapes.add_shape(shape, x, y, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(lw)
    no_shadow(sp)
    return sp


def txt(s, x, y, w, h, text, size=18, color=NAVY, bold=False, italic=False,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font="Calibri", spacing=1.0):
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.line_spacing = spacing
        r = p.add_run(); r.text = ln
        f = r.font; f.size = Pt(size); f.bold = bold; f.italic = italic
        f.color.rgb = color; f.name = font
    return tb


def bullets(s, x, y, w, h, items, size=17, color=INK, gap=8, mark="▸",
            mark_color=BLUE, spacing=1.04):
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = 0; tf.margin_top = 0
    for i, it in enumerate(items):
        lvl = 0
        if isinstance(it, tuple):
            it, lvl = it
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap); p.space_before = Pt(0); p.line_spacing = spacing
        if lvl == 0:
            rm = p.add_run(); rm.text = mark + "  "
            rm.font.size = Pt(size); rm.font.bold = True
            rm.font.color.rgb = mark_color; rm.font.name = "Calibri"
        else:
            rm = p.add_run(); rm.text = "      –  "
            rm.font.size = Pt(size-1); rm.font.color.rgb = SLATE; rm.font.name = "Calibri"
        r = p.add_run(); r.text = it
        f = r.font; f.size = Pt(size - lvl); f.color.rgb = color; f.name = "Calibri"
    return tb


def header(s, kicker, title):
    rect(s, 0, 0, SW, Inches(1.18), NAVY)
    rect(s, 0, Inches(1.18), SW, Pt(4), BLUE)
    rect(s, Inches(0.5), Inches(0.30), Pt(5), Inches(0.62), TEAL)
    txt(s, Inches(0.72), Inches(0.24), Inches(11.8), Inches(0.32),
        kicker.upper(), size=12.5, color=TEAL, bold=True)
    txt(s, Inches(0.72), Inches(0.55), Inches(11.8), Inches(0.55),
        title, size=24, color=WHITE, bold=True)


def footer(s, n):
    rect(s, 0, SH - Inches(0.42), SW, Inches(0.42), LIGHT)
    txt(s, Inches(0.5), SH - Inches(0.40), Inches(8), Inches(0.34),
        "«Vobkent» 110/35/10 kV PS  ·  Bitiruv malakaviy ishi  ·  Buxoro 2026",
        size=9.5, color=SLATE, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(11.4), SH - Inches(0.40), Inches(1.4), Inches(0.34),
        f"{n} / {TOTAL}", size=9.5, color=SLATE, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def pic_fit(s, path, x, y, w, h):
    iw, ih = Image.open(path).size
    fr = w / h; ir = iw / ih
    if ir > fr:
        nw = w; nh = int(w / ir)
    else:
        nh = h; nw = int(h * ir)
    nx = x + (w - nw) // 2; ny = y + (h - nh) // 2
    return s.shapes.add_picture(path, nx, ny, nw, nh)


def stat_card(s, x, y, w, h, value, label, accent=BLUE, vsize=30, bg=CARD):
    rect(s, x, y, w, h, bg)
    rect(s, x, y, Pt(5), h, accent)
    txt(s, x + Inches(0.18), y + Inches(0.12), w - Inches(0.3), Inches(0.6),
        value, size=vsize, color=NAVY, bold=True)
    txt(s, x + Inches(0.18), y + h - Inches(0.52), w - Inches(0.3), Inches(0.45),
        label, size=11.5, color=SLATE)


def table(s, x, y, w, data, col_w=None, header_bg=NAVY, fontsize=12.5,
          row_h=0.34, head_h=0.42, zebra=True, align_first_left=True,
          highlight_last=False):
    rows = len(data); cols = len(data[0])
    heights = [Inches(head_h)] + [Inches(row_h)] * (rows - 1)
    total_h = sum(heights, Emu(0))
    gtbl = s.shapes.add_table(rows, cols, x, y, w, total_h)
    tbl = gtbl.table
    tbl.first_row = False; tbl.horz_banding = False
    # remove default style banding via xml is complex; we set fills manually
    if col_w:
        total = sum(col_w)
        for j, cw in enumerate(col_w):
            tbl.columns[j].width = Emu(int(int(w) * cw / total))
    for i in range(rows):
        tbl.rows[i].height = heights[i]
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            cell.margin_left = Inches(0.08); cell.margin_right = Inches(0.06)
            cell.margin_top = Inches(0.02); cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            # fill
            if i == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = header_bg
            elif highlight_last and i == rows - 1:
                cell.fill.solid(); cell.fill.fore_color.rgb = CARD
            elif zebra and i % 2 == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = LIGHT
            else:
                cell.fill.solid(); cell.fill.fore_color.rgb = WHITE
            tf = cell.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if (j == 0 and align_first_left) else PP_ALIGN.CENTER
            r = p.add_run(); r.text = str(val)
            f = r.font; f.name = "Calibri"; f.size = Pt(fontsize)
            if i == 0:
                f.color.rgb = WHITE; f.bold = True
            else:
                f.color.rgb = INK
                if (highlight_last and i == rows - 1) or (j == 0 and align_first_left):
                    f.bold = True if (highlight_last and i == rows-1) else False
                    f.color.rgb = NAVY if j == 0 else INK
    return gtbl


def pill(s, x, y, w, h, text, bg, fg=WHITE, size=12):
    sp = rect(s, x, y, w, h, bg, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    try:
        sp.adjustments[0] = 0.5
    except Exception:
        pass
    txt(s, x, y, w, h, text, size=size, color=fg, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ============================================================
# 1. TITUL
# ============================================================
s = slide()
rect(s, 0, 0, SW, SH, NAVY)
rect(s, 0, 0, SW, Inches(0.16), TEAL)
rect(s, 0, SH - Inches(0.16), SW, Inches(0.16), BLUE)
# yon dekorativ chiziqlar
for i, c in enumerate([BLUE, TEAL, GREEN]):
    rect(s, Inches(0.0), Inches(2.7 + i*0.06), Inches(0.55), Pt(3), c)
txt(s, Inches(0.9), Inches(0.55), Inches(11.5), Inches(0.45),
    "O'ZBEKISTON RESPUBLIKASI OLIY TA'LIM, FAN VA INNOVATSIYALAR VAZIRLIGI",
    size=13, color=MUTED, bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(0.9), Inches(1.0), Inches(11.5), Inches(0.35),
    "____________________ universiteti  ·  «Elektr energetikasi» kafedrasi",
    size=12.5, color=MUTED, align=PP_ALIGN.CENTER)
pill(s, Inches(4.92), Inches(1.75), Inches(3.5), Inches(0.5),
     "BITIRUV MALAKAVIY ISHI", GREEN, WHITE, size=14)
txt(s, Inches(0.8), Inches(2.75), Inches(11.7), Inches(1.7),
    "ELEKTR TA'MINOTI TIZIMLARIDA\nENERGIYA SARFINI KAMAYTIRISH TEXNOLOGIYALARI",
    size=30, color=WHITE, bold=True, align=PP_ALIGN.CENTER, spacing=1.05)
txt(s, Inches(1.5), Inches(4.55), Inches(10.3), Inches(0.5),
    "Buxoro viloyati «Vobkent» 110/35/10 kV podstansiyasi misolida tadqiqot",
    size=15, color=RGBColor(0xC9,0xD6,0xEA), italic=True, align=PP_ALIGN.CENTER)
# pastki ma'lumot paneli
rect(s, Inches(1.8), Inches(5.45), Inches(9.7), Inches(1.25), NAVY2)
txt(s, Inches(2.1), Inches(5.62), Inches(9.1), Inches(1.0),
    "Bajardi:               ____________________________\n"
    "Ilmiy rahbar:        ____________________________\n"
    "«Himoyaga ruxsat etildi». Kafedra mudiri:  ______________",
    size=13.5, color=RGBColor(0xD7,0xE1,0xF0), spacing=1.25)
txt(s, Inches(0.8), Inches(6.95), Inches(11.7), Inches(0.4),
    "BUXORO — 2026", size=13, color=TEAL, bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 2. HIMOYA REJASI (mundarija)
# ============================================================
s = slide(); header(s, "Taqdimot rejasi", "Himoya tuzilmasi")
plan = [
    ("01", "Kirish", "Dolzarblik, maqsad, vazifalar, obyekt", BLUE),
    ("02", "I bob — Nazariy asoslar", "Yo'qotish turlari, energiya sifati, en kesim", TEAL),
    ("03", "II bob — Tahlil va hisoblar", "Yuklama, transformator, fider, balans", GREEN),
    ("04", "III bob — Texnologiyalar", "Kompensatsiya, ChOQ, AMI, SCADA, iqtisod", AMBER),
    ("05", "Xavfsizlik va xulosa", "Mehnat muhofazasi, natijalar, tavsiyalar", PURPLE),
]
yy = Inches(1.55)
for num, t, d, c in plan:
    rect(s, Inches(0.7), yy, Inches(11.95), Inches(0.92), LIGHT)
    rect(s, Inches(0.7), yy, Pt(6), Inches(0.92), c)
    txt(s, Inches(0.95), yy, Inches(1.1), Inches(0.92), num, size=30, color=c,
        bold=True, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(2.2), yy + Inches(0.13), Inches(10), Inches(0.4), t, size=18,
        color=NAVY, bold=True)
    txt(s, Inches(2.2), yy + Inches(0.52), Inches(10), Inches(0.35), d, size=13,
        color=SLATE)
    yy += Inches(1.04)
footer(s, 2)

# ============================================================
# 3. DOLZARBLIK
# ============================================================
s = slide(); header(s, "Kirish", "Mavzuning dolzarbligi")
bullets(s, Inches(0.7), Inches(1.45), Inches(7.4), Inches(5.4), [
    "Energiya manbadan iste'molchigacha bo'lgan zanjirning har bir bo'g'inida bir qismi yo'qoladi.",
    "O'zbekiston tarmoqlarida texnik va tijoriy yo'qotishlar ulushi rivojlangan davlatlardan yuqori.",
    "Yo'qotishlarning asosiy qismi 6–10 kV va 0,4 kV taqsimlash tarmoqlarida yuzaga keladi.",
    "Tarmoqda tejalgan har bir kVt·s — manbada qo'shimcha ishlab chiqarish, yoqilg'i va chiqindi tejami.",
    "Yo'qotishni kamaytirish — yangi quvvat qurishga qaraganda ancha arzon yo'l.",
], size=16.5, gap=13)
rect(s, Inches(8.35), Inches(1.45), Inches(4.3), Inches(2.55), NAVY)
txt(s, Inches(8.6), Inches(1.65), Inches(3.85), Inches(0.4), "MUAMMONING MOHIYATI",
    size=12.5, color=TEAL, bold=True)
txt(s, Inches(8.6), Inches(2.15), Inches(3.85), Inches(1.7),
    "Isish yo'qotishlari tokning KVADRATIGA proporsional:\nΔP = 3·I²·R\n→ tokning kichik kamayishi katta tejam beradi.",
    size=15, color=WHITE, spacing=1.1)
rect(s, Inches(8.35), Inches(4.15), Inches(4.3), Inches(2.7), CARD)
txt(s, Inches(8.6), Inches(4.32), Inches(3.85), Inches(0.4), "ZAMONAVIY VOSITALAR",
    size=12.5, color=BLUE, bold=True)
bullets(s, Inches(8.6), Inches(4.78), Inches(3.85), Inches(1.9), [
    "Reaktiv quvvat kompensatsiyasi", "Chastota o'zgartiruvchi qurilma",
    "AMI — aqlli hisobga olish", "SCADA — dispetcher nazorati",
], size=13.5, gap=6, mark="•", mark_color=BLUE)
footer(s, 3)

# ============================================================
# 4. MAQSAD VA VAZIFALAR
# ============================================================
s = slide(); header(s, "Kirish", "Ishning maqsadi va vazifalari")
rect(s, Inches(0.7), Inches(1.5), Inches(5.2), Inches(5.3), NAVY)
rect(s, Inches(0.7), Inches(1.5), Inches(5.2), Inches(0.7), BLUE)
txt(s, Inches(0.95), Inches(1.6), Inches(4.7), Inches(0.5), "MAQSAD", size=18,
    color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(0.95), Inches(2.45), Inches(4.7), Inches(4.2),
    "Elektr ta'minoti tizimlarida energiya sarfini kamaytirish texnologiyalarini "
    "nazariy va amaliy jihatdan tadqiq etish hamda tanlangan obyekt uchun texnik va "
    "iqtisodiy jihatdan asoslangan tavsiyalar ishlab chiqish.",
    size=16.5, color=RGBColor(0xE6,0xED,0xF7), spacing=1.18)
txt(s, Inches(6.25), Inches(1.5), Inches(6.4), Inches(0.45), "VAZIFALAR", size=18,
    color=NAVY, bold=True)
items = [
    "Yo'qotish turlari va yuzaga kelish mexanizmlarini nazariy o'rganish;",
    "Yuklama, kuchlanish pasayishi, transformator va kabel yo'qotishlarini hisoblash;",
    "Garmonik buzilishlar va elektr energiyasi sifatini baholash;",
    "Zamonaviy texnologiyalar ishlash tamoyili va shartlarini tahlil qilish;",
    "Choralar texnik samarasi va investitsiya qaytish muddatini hisoblash;",
    "Elektr xavfsizligi va mehnat muhofazasi tavsiyalarini berish.",
]
yy = Inches(2.05)
for i, it in enumerate(items, 1):
    rect(s, Inches(6.25), yy, Inches(0.4), Inches(0.4), TEAL, shape=MSO_SHAPE.OVAL)
    txt(s, Inches(6.25), yy, Inches(0.4), Inches(0.4), str(i), size=13, color=WHITE,
        bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(6.8), yy - Inches(0.02), Inches(5.85), Inches(0.75), it, size=14,
        color=INK, anchor=MSO_ANCHOR.MIDDLE, spacing=1.02)
    yy += Inches(0.78)
footer(s, 4)

# ============================================================
# 5. OBYEKT VA PREDMET
# ============================================================
s = slide(); header(s, "Kirish", "Tadqiqot obyekti va predmeti")
rect(s, Inches(0.7), Inches(1.45), Inches(11.95), Inches(1.7), LIGHT)
rect(s, Inches(0.7), Inches(1.45), Pt(6), Inches(1.7), BLUE)
txt(s, Inches(1.0), Inches(1.6), Inches(11.4), Inches(0.4), "OBYEKT", size=14,
    color=BLUE, bold=True)
txt(s, Inches(1.0), Inches(2.02), Inches(11.4), Inches(1.05),
    "Buxoro viloyati Vobkent tumanidagi «Vobkent» 110/35/10 kV taqsimlash podstansiyasi va unga "
    "ulangan 10 kV taqsimlash tarmog'i. Modernizatsiya doirasida 16 000 kVA transformator "
    "25 000 kVA quvvatli transformatorga almashtirilgan («Buxoro hududiy elektr tarmoqlari korxonasi» AJ).",
    size=14, color=INK, spacing=1.1)
rect(s, Inches(0.7), Inches(3.3), Inches(11.95), Inches(1.05), NAVY)
rect(s, Inches(0.7), Inches(3.3), Pt(6), Inches(1.05), TEAL)
txt(s, Inches(1.0), Inches(3.42), Inches(11.4), Inches(0.35), "PREDMET", size=14,
    color=TEAL, bold=True)
txt(s, Inches(1.0), Inches(3.78), Inches(11.4), Inches(0.5),
    "Tizimda energiya yo'qotishlarini kamaytirish texnologiyalari va ularning samaradorligini baholash usullari.",
    size=14, color=WHITE)
cards = [("110/35/10", "kV kuchlanish", BLUE), ("25 000", "kVA transformator", TEAL),
         ("8 ta", "10 kV fider", GREEN), ("60", "GVt·s yillik energiya", AMBER)]
cx = Inches(0.7)
for v, l, c in cards:
    stat_card(s, cx, Inches(4.65), Inches(2.86), Inches(1.55), v, l, c, vsize=28, bg=CARD)
    cx += Inches(2.99)
footer(s, 5)

# ============================================================
# 6. BO'LIM AJRATUVCHI — I BOB
# ============================================================
def divider(num, title, subtitle, accent):
    s = slide()
    rect(s, 0, 0, SW, SH, NAVY)
    rect(s, 0, Inches(3.05), SW, Inches(1.5), NAVY2)
    rect(s, Inches(0.0), Inches(3.05), Inches(0.9), Inches(1.5), accent)
    txt(s, Inches(1.2), Inches(2.1), Inches(6), Inches(1.0), num, size=80,
        color=accent, bold=True)
    txt(s, Inches(1.25), Inches(3.2), Inches(11), Inches(0.8), title, size=34,
        color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(1.25), Inches(4.15), Inches(11), Inches(0.4), subtitle, size=16,
        color=MUTED, anchor=MSO_ANCHOR.MIDDLE)
    return s

divider("I", "Energiya yo'qotishlarining nazariy asoslari",
        "Yo'qotish turlari · energiya sifati · iqtisodiy en kesim", TEAL)

# ============================================================
# 7. NAZARIY ASOSLAR
# ============================================================
s = slide(); header(s, "I bob · Nazariya", "Yo'qotishlar tasnifi va asosiy bog'liqliklar")
# 2 ustun klassifikatsiya kartalari
cls = [
    ("Tabiati bo'yicha", ["Yuklamaga bog'liq (o'zgaruvchan)", "Doimiy (salt yurish)"], BLUE),
    ("Kelib chiqishi bo'yicha", ["Texnik (fizik jarayonlar)", "Tijoriy (hisob, o'g'irlik)"], TEAL),
]
xx = Inches(0.7)
for t, its, c in cls:
    rect(s, xx, Inches(1.5), Inches(5.85), Inches(1.85), CARD)
    rect(s, xx, Inches(1.5), Pt(5), Inches(1.85), c)
    txt(s, xx + Inches(0.2), Inches(1.62), Inches(5.4), Inches(0.4), t, size=15,
        color=c, bold=True)
    bullets(s, xx + Inches(0.2), Inches(2.1), Inches(5.4), Inches(1.2), its,
            size=14, gap=6, mark="•", mark_color=c)
    xx += Inches(6.1)
# formula bandi
rect(s, Inches(0.7), Inches(3.6), Inches(5.85), Inches(1.5), NAVY)
txt(s, Inches(0.9), Inches(3.72), Inches(5.4), Inches(0.35), "ASOSIY QONUNIYAT",
    size=12.5, color=TEAL, bold=True)
txt(s, Inches(0.9), Inches(4.12), Inches(5.4), Inches(0.9),
    "ΔP = 3 · I² · R\nTok 2 barobar oshsa — yo'qotish 4 barobar ortadi",
    size=17, color=WHITE, bold=True, spacing=1.1)
rect(s, Inches(6.8), Inches(3.6), Inches(5.85), Inches(1.5), LIGHT)
txt(s, Inches(7.0), Inches(3.72), Inches(5.4), Inches(0.35), "REAKTIV QUVVAT TA'SIRI",
    size=12.5, color=BLUE, bold=True)
txt(s, Inches(7.0), Inches(4.1), Inches(5.4), Inches(0.95),
    "Reaktiv quvvat to'liq tokni oshiradi → barcha elementlarda yo'qotish ko'payadi. "
    "cos φ ni oshirish — kalit zaxira.", size=13.5, color=INK, spacing=1.05)
# nazariy baza pill qatori
txt(s, Inches(0.7), Inches(5.35), Inches(11), Inches(0.35), "Nazariy-uslubiy baza:",
    size=13, color=SLATE, bold=True)
base = ["Yu. S. Jelezko", "V. I. Idelchik", "F. F. Karpov", "B. I. Kudrin", "GOST 32144"]
px = Inches(0.7)
for b in base:
    w = Inches(0.42 + 0.092*len(b))
    pill(s, px, Inches(5.78), w, Inches(0.5), b, NAVY2, WHITE, size=12.5)
    px += w + Inches(0.2)
footer(s, 7)

# ============================================================
# 8. ENERGIYA SIFATI (jadval 0)
# ============================================================
s = slide(); header(s, "I bob · Nazariya", "Elektr energiyasi sifati ko'rsatkichlari (GOST 32144)")
data = [
    ["Ko'rsatkich", "Me'yoriy chegara"],
    ["Kuchlanishning turg'un chetlanishi", "± 10 %  (Uₙₒₘ ga nisbatan)"],
    ["Chastota chetlanishi", "± 0,2 Hz  (vaqtincha ± 0,4 Hz)"],
    ["Garmonik buzilish koeffitsienti (THD)", "≤ 8 %  (0,38–10 kV)"],
    ["Alohida garmonika koeffitsienti", "tartibiga ko'ra cheklanadi"],
    ["Kuchlanish nosimmetrikligi", "≤ 2 %  (vaqtincha ≤ 4 %)"],
]
table(s, Inches(0.7), Inches(1.55), Inches(7.7), data, col_w=[1.6,1.4],
      fontsize=13, row_h=0.62, head_h=0.5)
rect(s, Inches(8.75), Inches(1.55), Inches(3.9), Inches(4.55), CARD)
txt(s, Inches(8.95), Inches(1.75), Inches(3.5), Inches(0.4), "NEGA MUHIM?", size=13,
    color=BLUE, bold=True)
bullets(s, Inches(8.95), Inches(2.25), Inches(3.5), Inches(3.8), [
    "Sifat me'yoridan chetlanish — qo'shimcha yo'qotish va jihoz resursining qisqarishi.",
    "THD oshishi izolatsiya va kondensatorlarni qizdiradi.",
    "Kuchlanish chetlanishi yuklama rejimini buzadi.",
    "Standartga rioya — ishonchli va tejamkor ekspluatatsiya sharti.",
], size=13.5, gap=10)
footer(s, 8)

# ============================================================
# 9. DIVIDER II BOB
# ============================================================
divider("II", "Energiya sarfi va yo'qotishlar tahlili",
        "Yuklama · transformator · fider · balans · qisqa tutashuv", GREEN)

# ============================================================
# 10. YUKLAMA GRAFIGI
# ============================================================
s = slide(); header(s, "II bob · 2.1", "Yuklama grafigi va kuchlanish pasayishi tahlili")
pic_fit(s, "charts/01_load.png", Inches(0.55), Inches(1.45), Inches(8.4), Inches(5.55))
xx = Inches(9.1)
stat_card(s, xx, Inches(1.55), Inches(3.55), Inches(1.18), "12,0 MVt", "Maksimal quvvat Pₘₐₓ", RED, 26)
stat_card(s, xx, Inches(2.85), Inches(3.55), Inches(1.18), "9,05 MVt", "O'rtacha quvvat Pₒ'ʳ", AMBER, 26)
stat_card(s, xx, Inches(4.15), Inches(3.55), Inches(1.18), "0,75", "To'ldirilganlik koeff. k_t", BLUE, 26)
stat_card(s, xx, Inches(5.45), Inches(3.55), Inches(1.18), "60 GVt·s", "Yillik energiya  W", GREEN, 26)
footer(s, 10)

# ============================================================
# 11. TRANSFORMATOR YO'QOTISHLARI (jadval 2 + 5)
# ============================================================
s = slide(); header(s, "II bob · 2.2", "Transformator yo'qotishlari va rejim optimizatsiyasi")
data = [
    ["Ko'rsatkich", "Belgisi", "Qiymat"],
    ["Nominal to'liq quvvat", "Sₙₒₘ", "25 000 kVA"],
    ["Salt yurish yo'qotishi", "ΔPₓₓ", "25 kVt"],
    ["Qisqa tutashuv yo'qotishi", "ΔP_qt", "120 kVt"],
    ["Qisqa tutashuv kuchlanishi", "U_qt", "10,5 %"],
    ["Salt yurish toki", "Iₓₓ", "0,7 %"],
]
table(s, Inches(0.6), Inches(1.55), Inches(6.0), data, col_w=[2.0,0.9,1.1],
      fontsize=12.5, row_h=0.48, head_h=0.44)
pic_fit(s, "charts/09_transformer.png", Inches(6.9), Inches(1.45), Inches(6.0), Inches(4.0))
rect(s, Inches(0.6), Inches(5.55), Inches(12.05), Inches(1.15), CARD)
rect(s, Inches(0.6), Inches(5.55), Pt(6), Inches(1.15), GREEN)
txt(s, Inches(0.85), Inches(5.68), Inches(11.6), Inches(0.4), "ASOSIY NATIJA",
    size=13, color=GREEN, bold=True)
txt(s, Inches(0.85), Inches(6.06), Inches(11.6), Inches(0.6),
    "Bitta transformatorda ishlash (ikkitasi o'rniga) yillik yo'qotishni 503 → 350 MVt·s ga "
    "kamaytiradi — QO'SHIMCHA INVESTITSIYASIZ ≈ 153 MVt·s/yil tejam.",
    size=14, color=INK, spacing=1.05)
footer(s, 11)

# ============================================================
# 12. FIDER YO'QOTISHLARI (jadval 3/17 + chart)
# ============================================================
s = slide(); header(s, "II bob · 2.2", "10 kV fiderlar bo'yicha yo'qotishlar hisobi")
pic_fit(s, "charts/03_feeders.png", Inches(0.55), Inches(1.45), Inches(7.3), Inches(3.4))
data = [
    ["Fider", "L, km", "S, mm²", "ΔU, %", "ΔW, MVt·s"],
    ["F-1 markaz", "2,4", "120", "1,64", "142,8"],
    ["F-2 turmush", "3,1", "95", "2,08", "153,4"],
    ["F-4 qishloq-1", "5,2", "70", "2,98", "154,0"],
    ["F-5 qishloq-2", "6,0", "70", "2,90", "130,6"],
    ["Jami (8 fider)", "—", "—", "—", "865,6"],
]
table(s, Inches(0.55), Inches(4.95), Inches(7.3), data, col_w=[1.7,0.8,0.8,0.8,1.1],
      fontsize=11.5, row_h=0.33, head_h=0.4, highlight_last=True)
rect(s, Inches(8.1), Inches(1.55), Inches(4.55), Inches(5.15), NAVY)
txt(s, Inches(8.35), Inches(1.72), Inches(4.1), Inches(0.4), "TAHLIL XULOSASI",
    size=13, color=TEAL, bold=True)
bullets(s, Inches(8.35), Inches(2.2), Inches(4.05), Inches(4.4), [
    "Fider liniyalaridagi yillik yo'qotish — 865,6 MVt·s.",
    "Eng katta yo'qotish: F-2, F-4, F-5 fiderlarda.",
    "Sabab: katta uzunlik (5–6 km) va kichik en kesim (70 mm²).",
    "F-4 da ΔU = 2,98 % — me'yor chegarasiga yaqin.",
    "Asosiy zaxira aynan 10 kV taqsimlash tarmog'ida joylashgan.",
], size=14, color=RGBColor(0xE6,0xED,0xF7), gap=11, mark="▸", mark_color=TEAL)
footer(s, 12)

# ============================================================
# 13. YO'QOTISHLAR BALANSI (donut)
# ============================================================
s = slide(); header(s, "II bob · 2.3", "Podstansiya energiya balansi va yo'qotishlar tarkibi")
pic_fit(s, "charts/02_balance.png", Inches(0.4), Inches(1.5), Inches(7.8), Inches(5.4))
stat_card(s, Inches(8.4), Inches(1.6), Inches(4.25), Inches(1.5), "1760 MVt·s",
          "Yillik texnik yo'qotish (= 2,9 %)", RED, 26)
bullets(s, Inches(8.55), Inches(3.35), Inches(4.1), Inches(3.4), [
    "Yo'qotishning 68 % dan ortig'i — 10 kV bo'g'inda.",
    "Faqat 10 kV fiderlar — 49,2 % (eng katta ulush).",
    "Balans: W_kir = W_chiq + ΔW_texnik + ΔW_tijoriy.",
    "Demak choralar avvalo 10 kV tarmoqqa yo'naltirilishi kerak.",
], size=14.5, gap=12)
footer(s, 13)

# ============================================================
# 14. cos phi va THD
# ============================================================
s = slide(); header(s, "II bob · 2.3", "Quvvat koeffitsienti va garmonik buzilishlar")
pic_fit(s, "charts/04_thd.png", Inches(0.55), Inches(1.45), Inches(7.5), Inches(5.5))
stat_card(s, Inches(8.3), Inches(1.55), Inches(4.35), Inches(1.25), "cos φ = 0,85",
          "tan φ = 0,62  ·  Qₘₐₓ = 7440 kVar", AMBER, 24)
stat_card(s, Inches(8.3), Inches(2.95), Inches(4.35), Inches(1.25), "THD = 8,8 %",
          "me'yor ≤ 8 % — chegaradan yuqori", RED, 24)
rect(s, Inches(8.3), Inches(4.35), Inches(4.35), Inches(2.35), NAVY)
txt(s, Inches(8.5), Inches(4.5), Inches(3.95), Inches(0.4), "TAVSIYA ETILGAN YECHIM",
    size=12.5, color=TEAL, bold=True)
txt(s, Inches(8.5), Inches(4.95), Inches(3.95), Inches(1.7),
    "Kondensator batareyalarini rezonansdan himoyalovchi sozlangan drossel "
    "(filtr-reaktor, 7 % yoki 14 %) bilan o'rnatish hamda passiv garmonik filtrlardan foydalanish.",
    size=13.5, color=RGBColor(0xE6,0xED,0xF7), spacing=1.08)
footer(s, 14)

# ============================================================
# 15. OYLIK DINAMIKA + QISQA TUTASHUV
# ============================================================
s = slide(); header(s, "II bob · 2.4", "Yo'qotishlarning mavsumiy dinamikasi va qisqa tutashuv")
pic_fit(s, "charts/05_monthly.png", Inches(0.55), Inches(1.45), Inches(8.3), Inches(4.0))
boxes = [("11,9 kA", "Qisqa tutashuv toki I_k", BLUE),
         ("30,3 kA", "Zarba toki i_a", AMBER)]
yy = Inches(1.6)
for v, l, c in boxes:
    stat_card(s, Inches(9.0), yy, Inches(3.65), Inches(1.25), v, l, c, 26)
    yy += Inches(1.45)
rect(s, Inches(9.0), Inches(4.5), Inches(3.65), Inches(1.0), CARD)
txt(s, Inches(9.2), Inches(4.62), Inches(3.3), Inches(0.8),
    "Mavjud taqsimlash qurilmasi termik va dinamik shartlarga to'liq javob beradi.",
    size=12.5, color=INK, spacing=1.05, anchor=MSO_ANCHOR.MIDDLE)
rect(s, Inches(0.55), Inches(5.65), Inches(12.1), Inches(1.05), LIGHT)
rect(s, Inches(0.55), Inches(5.65), Pt(6), Inches(1.05), GREEN)
txt(s, Inches(0.8), Inches(5.77), Inches(11.6), Inches(0.85),
    "Yo'qotish ulushi yil bo'yi barqaror ≈ 2,9 %, lekin yozda (iyul–avgust) va qishda (yanvar) "
    "absolyut qiymat oshadi — cho'qqi davrlarda kompensatsiya samarasi eng yuqori.",
    size=14, color=INK, spacing=1.05, anchor=MSO_ANCHOR.MIDDLE)
footer(s, 15)

# ============================================================
# 16. DIVIDER III BOB
# ============================================================
divider("III", "Kamaytirish texnologiyalari va samaradorlik",
        "Kompensatsiya · ChOQ · AMI · SCADA · iqtisodiy baholash", AMBER)

# ============================================================
# 17. TEXNOLOGIYALAR SHARHI
# ============================================================
s = slide(); header(s, "III bob · 3.1–3.2", "Energiya sarfini kamaytirish texnologiyalari")
tech = [
    ("Reaktiv quvvat kompensatsiyasi", "UKRM 10,5 kV; 3600 kVar (6×600). cos φ: 0,85→0,95; S: 14,12→12,63 MVA. Yo'qotish −20 % ≈ 284 MVt·s/yil.", BLUE),
    ("Chastota o'zgartiruvchi qurilma (ChOQ)", "110 kVt nasos yuritmasi, PID rostlash. Tejam ≈ 180 MVt·s/yil. Qaytish ≈ 0,9 yil — eng tez choralardan.", TEAL),
    ("AMI — aqlli hisobga olish", "Aqlli hisoblagich + konsentrator + MDM. Tijoriy yo'qotishni keskin kamaytiradi: ≈ 1200 MVt·s/yil.", GREEN),
    ("SCADA / PLC / IoT monitoring", "Real vaqtda nazorat, masofadan boshqaruv, tarmoqni balanslash. Tejam ≈ 240 MVt·s/yil.", PURPLE),
]
yy = Inches(1.5)
for t, d, c in tech:
    rect(s, Inches(0.7), yy, Inches(11.95), Inches(1.22), LIGHT)
    rect(s, Inches(0.7), yy, Pt(6), Inches(1.22), c)
    txt(s, Inches(1.0), yy + Inches(0.13), Inches(11.4), Inches(0.4), t, size=16.5,
        color=c, bold=True)
    txt(s, Inches(1.0), yy + Inches(0.57), Inches(11.4), Inches(0.6), d, size=13.5,
        color=INK, spacing=1.05)
    yy += Inches(1.32)
footer(s, 17)

# ============================================================
# 18. CHORALAR SAMARADORLIGI (jadval 10 + chart)
# ============================================================
s = slide(); header(s, "III bob · 3.4", "Choralarning texnik-iqtisodiy ko'rsatkichlari")
pic_fit(s, "charts/06_measures.png", Inches(0.5), Inches(1.5), Inches(7.0), Inches(3.4))
data = [
    ["Chora", "Tejam\nMVt·s/yil", "Tejam\nmln so'm", "Inv.\nmln so'm", "T_q\nyil"],
    ["Reaktiv komp.", "284", "170", "538", "3,1"],
    ["ChOQ", "180", "108", "95", "0,9"],
    ["AMI", "1200", "720", "1730", "2,4"],
    ["SCADA", "240", "144", "640", "4,5"],
    ["Jami (majmua)", "1904", "1142", "3003", "2,6"],
]
table(s, Inches(0.5), Inches(4.95), Inches(7.0), data, col_w=[1.5,1.0,1.0,1.0,0.7],
      fontsize=11, row_h=0.32, head_h=0.44, highlight_last=True)
xx = Inches(7.75)
stat_card(s, xx, Inches(1.55), Inches(4.9), Inches(1.15), "1904 MVt·s/yil",
          "Majmuaning umumiy tejami", GREEN, 24)
stat_card(s, xx, Inches(2.85), Inches(4.9), Inches(1.15), "1142 mln so'm/yil",
          "Yillik pul tejami", BLUE, 24)
stat_card(s, xx, Inches(4.15), Inches(4.9), Inches(1.15), "3003 mln so'm",
          "Umumiy investitsiya", AMBER, 24)
stat_card(s, xx, Inches(5.45), Inches(4.9), Inches(1.15), "≈ 2,6 yil",
          "O'rtacha qaytish muddati", TEAL, 24)
footer(s, 18)

# ============================================================
# 19. NPV / PUL OQIMI (jadval 19 + chart)
# ============================================================
s = slide(); header(s, "III bob · 3.4", "Iqtisodiy asoslash: NPV va sezgirlik tahlili")
pic_fit(s, "charts/07_cashflow.png", Inches(0.5), Inches(1.5), Inches(7.6), Inches(5.3))
rect(s, Inches(8.35), Inches(1.55), Inches(4.3), Inches(1.55), GREEN)
txt(s, Inches(8.55), Inches(1.7), Inches(3.9), Inches(0.4), "ASOSIY NATIJA", size=12.5,
    color=WHITE, bold=True)
txt(s, Inches(8.55), Inches(2.12), Inches(3.9), Inches(0.95),
    "NPV ≈ 1930 mln so'm\n(r = 15 %, 8 yil) → NPV > 0 → loyiha asoslangan",
    size=14.5, color=WHITE, bold=True, spacing=1.05)
# sezgirlik jadvali (tarif)
data = [
    ["Tarif, so'm/kVt·s", "Tejam, mln", "NPV, mln"],
    ["480", "915", "≈ 1100"],
    ["600", "1142", "≈ 1930"],
    ["720", "1370", "≈ 2760"],
]
table(s, Inches(8.35), Inches(3.4), Inches(4.3), data, col_w=[1.4,1.0,1.0],
      fontsize=12, row_h=0.4, head_h=0.42)
bullets(s, Inches(8.35), Inches(5.6), Inches(4.3), Inches(1.2), [
    "Sof oqim ≈ 2,7-yilda musbatga o'tadi.",
    "Tarif oshsa NPV ortadi — loyiha barqaror foydali.",
], size=13, gap=7)
footer(s, 19)

# ============================================================
# 20. NATIJA QIYOSI (jadval 24 + chart)
# ============================================================
s = slide(); header(s, "Natija", "Choralardan oldin va keyin: qiyosiy tahlil")
pic_fit(s, "charts/08_comparison.png", Inches(0.5), Inches(1.5), Inches(7.6), Inches(5.3))
data = [
    ["Ko'rsatkich", "Gacha", "Keyin"],
    ["Quvvat koeffitsienti cos φ", "0,85", "0,95"],
    ["To'liq quvvat, MVA", "14,12", "12,63"],
    ["Texnik yo'qotish, MVt·s", "1760", "≈ 1400"],
    ["Tijoriy yo'qotish, %", "≈ 2,0", "≈ 0,5"],
    ["THD, %", "8,8", "< 5"],
    ["Umumiy yo'qotish, %", "≈ 5,0", "≈ 3,0"],
]
table(s, Inches(8.3), Inches(1.55), Inches(4.35), data, col_w=[2.0,0.9,0.9],
      fontsize=12.5, row_h=0.42, head_h=0.44)
footer(s, 20)

# ============================================================
# 21. XAVFSIZLIK (jadval 13 + 23)
# ============================================================
s = slide(); header(s, "Bob 3.5", "Hayot faoliyati xavfsizligi va mehnat muhofazasi")
txt(s, Inches(0.7), Inches(1.45), Inches(6), Inches(0.35),
    "Relay himoyasi turlari", size=14, color=BLUE, bold=True)
data1 = [
    ["Himoya turi", "Vazifasi"],
    ["Maksimal tok himoyasi", "qisqa tutashuvdan himoya"],
    ["Tok kesimi", "tezkor o'chirish"],
    ["Differensial himoya", "transformator ichki nosozligi"],
    ["Gaz himoyasi", "ichki yoy va moy parchalanishi"],
    ["Yerga tutashuv himoyasi", "bir fazali tutashuvni aniqlash"],
]
table(s, Inches(0.7), Inches(1.85), Inches(6.0), data1, col_w=[1.5,1.7],
      fontsize=12, row_h=0.44, head_h=0.42)
txt(s, Inches(7.0), Inches(1.45), Inches(6), Inches(0.35),
    "Yong'in, ekologik va sanitariya talablari", size=14, color=GREEN, bold=True)
bullets(s, Inches(7.0), Inches(1.95), Inches(5.7), Inches(3.0), [
    "Yerga ulash va zanulleniye (GOST 12.1.030);",
    "Tegish kuchlanishi chegaralari (GOST 12.1.038);",
    "Shaxsiy himoya vositalari: izolatsion shtanga, dielektrik qo'lqop, yoyga chidamli kiyim;",
    "Transformator moyi — yong'in xavfi: moy yig'gich va avtomatik signalizatsiya;",
    "Elektromagnit maydon, shovqin va sanitariya-gigiyena me'yorlariga rioya.",
], size=13.5, gap=9, mark="•", mark_color=GREEN)
rect(s, Inches(0.7), Inches(4.65), Inches(6.0), Inches(2.05), CARD)
txt(s, Inches(0.95), Inches(4.78), Inches(5.5), Inches(0.35), "Yuklanish rejimlari (GOST 14209)",
    size=12.5, color=NAVY, bold=True)
bullets(s, Inches(0.95), Inches(5.22), Inches(5.5), Inches(1.4), [
    "Doimiy normal: k ≤ 1,0;",
    "Sutkalik notekislik: 1,0–1,3;",
    "Avariyadan keyin: 1,3–1,4 (cheklangan vaqt).",
], size=12.5, gap=6, mark="•", mark_color=BLUE)
footer(s, 21)

# ============================================================
# 22. XULOSA VA TAVSIYALAR
# ============================================================
s = slide(); header(s, "Yakun", "Xulosa va amaliy tavsiyalar")
bullets(s, Inches(0.7), Inches(1.4), Inches(12.0), Inches(3.7), [
    "Yo'qotishlar tabiati nazariy asoslandi: ular tok kvadratiga va reaktiv quvvatga bog'liq.",
    "Yillik texnik yo'qotish 1760 MVt·s (2,9 %); 68 % dan ortig'i — 10 kV bo'g'inda, ayniqsa F-2/F-4/F-5 fiderlarda.",
    "cos φ ni 0,85 → 0,95 ga ko'tarish yuklamaga bog'liq yo'qotishlarni ≈ 20 % (≈ 284 MVt·s) kamaytiradi.",
    "Transformator rejimini optimallashtirish xarajatsiz ≈ 153 MVt·s/yil tejam beradi.",
    "Choralar qaytishi 0,9–4,5 yil; majmua uchun NPV ≈ 1930 mln so'm (musbat) → loyiha iqtisodiy asoslangan.",
], size=15.5, gap=10)
rect(s, Inches(0.7), Inches(5.05), Inches(11.95), Inches(1.65), NAVY)
txt(s, Inches(0.95), Inches(5.2), Inches(11.5), Inches(0.35),
    "TAVSIYA ETILGAN JORIY ETISH KETMA-KETLIGI", size=13, color=TEAL, bold=True)
steps = [("1", "Transformator\nrejimi", GREEN), ("2", "ChOQ", TEAL),
         ("3", "Reaktiv\nkompensatsiya", BLUE), ("4", "AMI", AMBER),
         ("5", "SCADA va\nbalanslash", PURPLE)]
sx = Inches(0.95)
for n, t, c in steps:
    rect(s, sx, Inches(5.7), Inches(2.05), Inches(0.85), c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s, sx + Inches(0.12), Inches(5.7), Inches(1.85), Inches(0.85),
        f"{n}.  {t}", size=12.5, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    sx += Inches(2.32)
footer(s, 22)

# ============================================================
# 23. RAHMAT
# ============================================================
s = slide()
rect(s, 0, 0, SW, SH, NAVY)
rect(s, 0, 0, SW, Inches(0.16), TEAL)
rect(s, 0, SH - Inches(0.16), SW, Inches(0.16), BLUE)
rect(s, Inches(4.67), Inches(3.5), Inches(4.0), Pt(4), TEAL)
txt(s, Inches(0.8), Inches(2.55), Inches(11.7), Inches(1.0),
    "E'tiboringiz uchun rahmat!", size=42, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(3.75), Inches(11.7), Inches(0.5),
    "Savollaringizga javob berishga tayyorman", size=17, color=MUTED,
    italic=True, align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(6.7), Inches(11.7), Inches(0.4),
    "«Vobkent» 110/35/10 kV podstansiyasi  ·  Buxoro — 2026",
    size=12.5, color=RGBColor(0x6F,0x82,0xA6), align=PP_ALIGN.CENTER)

out = "Prezentatsiya_Vobkent_BMI.pptx"
prs.save(out)
print("Saqlandi:", out, "| slaydlar:", len(prs.slides._sldIdLst))
