# -*- coding: utf-8 -*-
"""Himoyaga to'liq tayyor 15 slaydli prezentatsiya — energetik dizayn (navy + mis)."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

# ===================== DIZAYN TIZIMI: energetik palitra =====================
NAVY    = RGBColor(0x0B, 0x25, 0x45)   # quyuq ko'k (asosiy fon)
NAVY2   = RGBColor(0x13, 0x33, 0x5A)   # ochroq navy panel
STEEL   = RGBColor(0x1F, 0x4E, 0x79)   # po'lat ko'k
COPPER  = RGBColor(0xC0, 0x79, 0x2B)   # mis urg'u
COPPERL = RGBColor(0xD9, 0x9B, 0x57)   # och mis
TEAL    = RGBColor(0x2A, 0x9D, 0x8F)
GREEN   = RGBColor(0x2E, 0x7D, 0x32)
AMBER   = RGBColor(0xE0, 0xA1, 0x00)
RED     = RGBColor(0xB3, 0x26, 0x1E)
SLATE   = RGBColor(0x41, 0x50, 0x6B)
LIGHT   = RGBColor(0xF1, 0xF5, 0xFB)
CARD    = RGBColor(0xE7, 0xED, 0xF6)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
MUTED   = RGBColor(0x9D, 0xB2, 0xD4)
INK     = RGBColor(0x1A, 0x24, 0x33)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]
TOTAL = 15


def slide():
    return prs.slides.add_slide(BLANK)


def rect(s, x, y, w, h, color, line=None, lw=1.0, shape=MSO_SHAPE.RECTANGLE):
    sp = s.shapes.add_shape(shape, x, y, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(lw)
    sp.shadow.inherit = False
    return sp


def txt(s, x, y, w, h, text, size=18, color=NAVY, bold=False, italic=False,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font="Calibri", spacing=1.0):
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    for i, ln in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.line_spacing = spacing
        r = p.add_run(); r.text = ln
        f = r.font; f.size = Pt(size); f.bold = bold; f.italic = italic
        f.color.rgb = color; f.name = font
    return tb


def bullets(s, x, y, w, h, items, size=17, color=INK, gap=8, mark="▸",
            mark_color=COPPER, spacing=1.05):
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
            rm.font.size = Pt(size - 1); rm.font.color.rgb = SLATE
            rm.font.name = "Calibri"
        r = p.add_run(); r.text = it
        f = r.font; f.size = Pt(size - lvl); f.color.rgb = color; f.name = "Calibri"
    return tb


def header(s, kicker, title):
    rect(s, 0, 0, SW, Inches(1.12), NAVY)
    rect(s, 0, Inches(1.12), SW, Pt(3.5), COPPER)
    rect(s, Inches(0.5), Inches(0.28), Pt(5), Inches(0.6), COPPER)
    txt(s, Inches(0.72), Inches(0.22), Inches(11.8), Inches(0.3),
        kicker.upper(), size=12, color=COPPERL, bold=True)
    txt(s, Inches(0.72), Inches(0.52), Inches(11.8), Inches(0.55),
        title, size=23, color=WHITE, bold=True)


def footer(s, n):
    rect(s, 0, SH - Inches(0.4), SW, Inches(0.4), LIGHT)
    txt(s, Inches(0.5), SH - Inches(0.38), Inches(9), Inches(0.32),
        "«Vobkent» 110/35/10 kV PS  ·  M.Sh. Muxiddinov  ·  BuxDTU, 2026",
        size=9.5, color=SLATE, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(11.4), SH - Inches(0.38), Inches(1.4), Inches(0.32),
        f"{n} / {TOTAL}", size=9.5, color=SLATE, align=PP_ALIGN.RIGHT,
        anchor=MSO_ANCHOR.MIDDLE)


def pic_fit(s, path, x, y, w, h):
    iw, ih = Image.open(path).size
    fr = w / h; ir = iw / ih
    if ir > fr:
        nw = w; nh = int(w / ir)
    else:
        nh = h; nw = int(h * ir)
    nx = x + (w - nw) // 2; ny = y + (h - nh) // 2
    return s.shapes.add_picture(path, nx, ny, nw, nh)


def stat_card(s, x, y, w, h, value, label, accent=COPPER, vsize=26, bg=CARD,
              valcolor=NAVY):
    rect(s, x, y, w, h, bg)
    rect(s, x, y, Pt(5), h, accent)
    txt(s, x + Inches(0.2), y + Inches(0.12), w - Inches(0.32), Inches(0.55),
        value, size=vsize, color=valcolor, bold=True)
    txt(s, x + Inches(0.2), y + h - Inches(0.5), w - Inches(0.32), Inches(0.42),
        label, size=11, color=SLATE)


def table(s, x, y, w, data, col_w=None, header_bg=NAVY, fontsize=12,
          row_h=0.34, head_h=0.42, highlight_last=False):
    rows = len(data); cols = len(data[0])
    heights = [Inches(head_h)] + [Inches(row_h)] * (rows - 1)
    total_h = sum(heights, Emu(0))
    gtbl = s.shapes.add_table(rows, cols, x, y, w, total_h)
    tbl = gtbl.table
    tbl.first_row = False; tbl.horz_banding = False
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
            if i == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = header_bg
            elif highlight_last and i == rows - 1:
                cell.fill.solid(); cell.fill.fore_color.rgb = CARD
            elif i % 2 == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = LIGHT
            else:
                cell.fill.solid(); cell.fill.fore_color.rgb = WHITE
            tf = cell.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
            r = p.add_run(); r.text = str(val)
            f = r.font; f.name = "Calibri"; f.size = Pt(fontsize)
            if i == 0:
                f.color.rgb = WHITE; f.bold = True
            else:
                f.color.rgb = NAVY if j == 0 else INK
                if highlight_last and i == rows - 1:
                    f.bold = True
    return gtbl


def pill(s, x, y, w, h, text, bg, fg=WHITE, size=12):
    sp = rect(s, x, y, w, h, bg, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    try:
        sp.adjustments[0] = 0.5
    except Exception:
        pass
    txt(s, x, y, w, h, text, size=size, color=fg, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def numbered(s, x, y, w, items, size=14, gap=0.74, accent=TEAL):
    yy = y
    for i, it in enumerate(items, 1):
        rect(s, x, yy, Inches(0.4), Inches(0.4), accent, shape=MSO_SHAPE.OVAL)
        txt(s, x, yy, Inches(0.4), Inches(0.4), str(i), size=13, color=WHITE,
            bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        txt(s, x + Inches(0.55), yy - Inches(0.02), w - Inches(0.55),
            Inches(gap), it, size=size, color=INK, anchor=MSO_ANCHOR.MIDDLE,
            spacing=1.03)
        yy += Inches(gap)


# ============================================================
# 1. TITUL
# ============================================================
s = slide()
rect(s, 0, 0, SW, SH, NAVY)
rect(s, 0, 0, SW, Inches(0.14), COPPER)
rect(s, 0, SH - Inches(0.14), SW, Inches(0.14), COPPER)
# yon mis aksent chiziqlari (energetik motiv)
for i in range(3):
    rect(s, Inches(0.0), Inches(2.62 + i*0.07), Inches(0.5), Pt(3), COPPERL)
txt(s, Inches(0.9), Inches(0.5), Inches(11.5), Inches(0.4),
    "O'ZBEKISTON RESPUBLIKASI OLIY TA'LIM, FAN VA INNOVATSIYALAR VAZIRLIGI",
    size=13, color=MUTED, bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(0.9), Inches(0.94), Inches(11.5), Inches(0.34),
    "BUXORO DAVLAT TEXNIKA UNIVERSITETI  ·  «Elektr energetikasi» kafedrasi",
    size=13, color=MUTED, align=PP_ALIGN.CENTER)
txt(s, Inches(0.9), Inches(1.32), Inches(11.5), Inches(0.3),
    "Mutaxassislik: 60710900 — Energiya tejamkorligi va energoaudit",
    size=12, color=MUTED, align=PP_ALIGN.CENTER)
pill(s, Inches(4.92), Inches(1.78), Inches(3.5), Inches(0.48),
     "BITIRUV MALAKAVIY ISHI", COPPER, WHITE, size=14)
txt(s, Inches(0.7), Inches(2.72), Inches(11.95), Inches(1.55),
    "ELEKTR TA'MINOTI TIZIMLARIDA ENERGIYA SARFINI\nKAMAYTIRISH TEXNOLOGIYALARINI TADQIQOT QILISH",
    size=27, color=WHITE, bold=True, align=PP_ALIGN.CENTER, spacing=1.06)
txt(s, Inches(1.4), Inches(4.5), Inches(10.5), Inches(0.5),
    "Buxoro viloyati «Vobkent» 110/35/10 kV podstansiyasi misolida",
    size=15, color=COPPERL, italic=True, align=PP_ALIGN.CENTER)
rect(s, Inches(2.1), Inches(5.4), Inches(9.1), Inches(1.18), NAVY2)
txt(s, Inches(2.45), Inches(5.55), Inches(8.5), Inches(0.95),
    "Bajardi:  Muxiddinov Sherzod Shaxob o'g'li\n"
    "Ilmiy rahbar:  dots. S.Sh. Rustamov\n"
    "«Himoyaga ruxsat etildi». Kafedra mudiri:  ______________",
    size=13.5, color=RGBColor(0xDC,0xE5,0xF2), spacing=1.22)
txt(s, Inches(0.9), Inches(6.85), Inches(11.5), Inches(0.4),
    "BUXORO — 2026", size=13, color=COPPERL, bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 2. DOLZARBLIK VA MUAMMO
# ============================================================
s = slide(); header(s, "Kirish", "Mavzuning dolzarbligi va muammoning qo'yilishi")
pic_fit(s, "charts/02_balance.png", Inches(0.35), Inches(1.4), Inches(7.1), Inches(5.6))
bullets(s, Inches(7.7), Inches(1.5), Inches(5.2), Inches(3.6), [
    "Energiya manbadan iste'molchigacha har bir bo'g'inda qisman yo'qoladi; "
    "yo'qotishlarni kamaytirish — tarmoq ekspluatatsiyasining markaziy masalasi.",
    "Yo'qotishning asosiy qismi 6–10 kV taqsimlash tarmog'ida yuzaga keladi.",
    "Isish yo'qotishi tokning KVADRATIGA bog'liq (ΔP = 3·I²·R) — kichik tok "
    "kamayishi katta tejam beradi.",
], size=14.5, gap=11)
rect(s, Inches(7.7), Inches(5.05), Inches(5.2), Inches(1.95), NAVY)
rect(s, Inches(7.7), Inches(5.05), Pt(5), Inches(1.95), COPPER)
txt(s, Inches(7.95), Inches(5.2), Inches(4.8), Inches(0.35), "MUAMMO",
    size=12.5, color=COPPERL, bold=True)
txt(s, Inches(7.95), Inches(5.58), Inches(4.8), Inches(1.3),
    "Obyektda yillik texnik yo'qotish 1760 MVt·s (2,9 %) ni tashkil etadi va "
    "uning 68 % dan ortig'i 10 kV bo'g'inga to'g'ri keladi — bu zaxirani "
    "miqdoran baholash va kamaytirish zarur.",
    size=13.5, color=RGBColor(0xDC,0xE5,0xF2), spacing=1.08)
footer(s, 2)

# ============================================================
# 3. MAQSAD VA VAZIFALAR
# ============================================================
s = slide(); header(s, "Kirish", "Tadqiqotning maqsadi va vazifalari")
rect(s, Inches(0.7), Inches(1.5), Inches(5.0), Inches(5.3), NAVY)
rect(s, Inches(0.7), Inches(1.5), Inches(5.0), Inches(0.68), COPPER)
txt(s, Inches(0.95), Inches(1.6), Inches(4.5), Inches(0.5), "MAQSAD", size=17,
    color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(0.95), Inches(2.42), Inches(4.5), Inches(4.2),
    "Elektr ta'minoti tizimlarida energiya sarfini kamaytirish texnologiyalarini "
    "nazariy va amaliy jihatdan tadqiq etish hamda «Vobkent» podstansiyasi uchun "
    "texnik va iqtisodiy jihatdan asoslangan tavsiyalar ishlab chiqish.",
    size=16, color=RGBColor(0xE6,0xED,0xF7), spacing=1.18)
txt(s, Inches(6.1), Inches(1.5), Inches(6.5), Inches(0.4), "VAZIFALAR", size=17,
    color=NAVY, bold=True)
numbered(s, Inches(6.1), Inches(2.05), Inches(6.55), [
    "Yo'qotish turlari va yuzaga kelish mexanizmlarini nazariy o'rganish;",
    "Yuklama, kuchlanish pasayishi, transformator va fider yo'qotishlarini hisoblash;",
    "Garmonik buzilishlar va elektr energiyasi sifatini baholash;",
    "Kamaytirish texnologiyalari ishlash tamoyilini tahlil qilish;",
    "Choralar texnik samarasi va iqtisodiy qaytimini hisoblash;",
    "Elektr xavfsizligi bo'yicha amaliy tavsiyalar berish.",
], size=13.5, gap=0.79)
footer(s, 3)

# ============================================================
# 4. ILMIY YANGILIK VA HIMOYAGA OLIB CHIQILADIGAN HOLATLAR
# ============================================================
s = slide(); header(s, "Akademik asos", "Ilmiy yangilik va himoyaga olib chiqiladigan holatlar")
rect(s, Inches(0.7), Inches(1.5), Inches(5.85), Inches(5.3), CARD)
rect(s, Inches(0.7), Inches(1.5), Pt(6), Inches(5.3), COPPER)
txt(s, Inches(0.95), Inches(1.65), Inches(5.4), Inches(0.4), "ILMIY YANGILIK",
    size=15, color=COPPER, bold=True)
bullets(s, Inches(0.95), Inches(2.2), Inches(5.4), Inches(4.4), [
    "Bir necha kamaytirish texnologiyasi (kompensatsiya, ChOQ, AMI, SCADA) "
    "yagona obyekt uchun yagona metodika asosida qiyosiy baholangan.",
    "Choralar texnik samara va investitsiya qaytimi bo'yicha ustuvorlik "
    "tartibida joylashtirilgan.",
    "Ishlab chiqilgan metodika viloyatdagi o'xshash podstansiyalarga "
    "tatbiq etish uchun yaroqli.",
], size=14, gap=12)
rect(s, Inches(6.75), Inches(1.5), Inches(5.85), Inches(5.3), NAVY)
rect(s, Inches(6.75), Inches(1.5), Pt(6), Inches(5.3), TEAL)
txt(s, Inches(7.0), Inches(1.65), Inches(5.4), Inches(0.4),
    "HIMOYAGA OLIB CHIQILADIGAN HOLATLAR", size=15, color=TEAL, bold=True)
bullets(s, Inches(7.0), Inches(2.2), Inches(5.4), Inches(4.4), [
    "Yo'qotishlar balansi va 10 kV bo'g'indagi asosiy zaxiralarning miqdoriy bahosi.",
    "cos φ ni 0,95 ga ko'tarish orqali yuklama yo'qotishini ≈ 20 % kamaytirish.",
    "Transformator rejimini optimallashtirishning xarajatsiz samarasi (≈ 153 MVt·s/yil).",
    "Choralar majmuasining iqtisodiy asoslanganligi (NPV > 0).",
], size=14, color=RGBColor(0xE6,0xED,0xF7), gap=11, mark_color=TEAL)
footer(s, 4)

# ============================================================
# 5. OBYEKT — BIR CHIZIQLI SXEMA
# ============================================================
s = slide(); header(s, "Tadqiqot obyekti", "«Vobkent» 110/35/10 kV podstansiyasi")
pic_fit(s, "charts/00_sld.png", Inches(0.3), Inches(1.35), Inches(8.7), Inches(5.75))
cards = [("110/35/10", "kV kuchlanish", STEEL),
         ("25 000", "kVA transformator", COPPER),
         ("8 ta", "10 kV fider", TEAL),
         ("60", "GVt·s yillik energiya", AMBER)]
yy = Inches(1.5)
for v, l, c in cards:
    stat_card(s, Inches(9.2), yy, Inches(3.45), Inches(1.18), v, l, c, vsize=24)
    yy += Inches(1.4)
footer(s, 5)

# ============================================================
# 6. TADQIQOT USULLARI VA ASOSIY FORMULALAR
# ============================================================
s = slide(); header(s, "Metodologiya", "Tadqiqot usullari va asosiy hisob formulalari")
bullets(s, Inches(0.7), Inches(1.5), Inches(5.5), Inches(5.3), [
    "Tahliliy usul — yo'qotishlarni elementlar bo'yicha hisoblash;",
    "Statistik usul — yuklama grafigi va mavsumiy taqsimot tahlili;",
    "Qiyosiy usul — texnologiyalarni yagona mezon asosida solishtirish;",
    "Texnik-iqtisodiy baholash — NPV va qaytish muddati hisobi;",
    "Me'yoriy hujjatlar: GOST 32144, GOST 14209, PUE talablari.",
], size=15, gap=13)
rect(s, Inches(6.45), Inches(1.5), Inches(6.2), Inches(5.3), NAVY)
txt(s, Inches(6.7), Inches(1.65), Inches(5.7), Inches(0.4),
    "ASOSIY HISOB FORMULALARI", size=13.5, color=COPPERL, bold=True)
formulas = [
    ("Quvvat yo'qotishi", "ΔP = 3 · I² · R"),
    ("Kuchlanish pasayishi", "ΔU = (P·R + Q·X) / U"),
    ("Yo'qotishlar vaqti", "τ = (0,124 + Tₘₐₓ/10⁴)² · 8760"),
    ("Kompensatsiya quvvati", "Q_k = P · (tan φ₁ − tan φ₂)"),
    ("Garmonik buzilish", "THD = √(ΣUₙ²) / U₁ · 100 %"),
    ("Sof joriy qiymat", "NPV = Σ E_y/(1+r)ᵗ − K"),
]
yy = Inches(2.18)
for name, fla in formulas:
    txt(s, Inches(6.7), yy, Inches(2.6), Inches(0.5), name, size=12.5,
        color=MUTED, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(9.3), yy, Inches(3.1), Inches(0.5), fla, size=14.5,
        color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    yy += Inches(0.74)
footer(s, 6)

# ============================================================
# 7. YUKLAMA REJIMI
# ============================================================
s = slide(); header(s, "II bob · Tahlil", "Yuklama rejimi va sutkalik grafik")
pic_fit(s, "charts/01_load.png", Inches(0.5), Inches(1.45), Inches(8.4), Inches(5.55))
stat_card(s, Inches(9.15), Inches(1.55), Inches(3.5), Inches(1.18), "12,0 MVt",
          "Maksimal quvvat Pₘₐₓ", RED, 24)
stat_card(s, Inches(9.15), Inches(2.85), Inches(3.5), Inches(1.18), "9,05 MVt",
          "O'rtacha quvvat Pₒ'ʳ", AMBER, 24)
stat_card(s, Inches(9.15), Inches(4.15), Inches(3.5), Inches(1.18), "0,75",
          "To'ldirilganlik koeff. k_t", STEEL, 24)
stat_card(s, Inches(9.15), Inches(5.45), Inches(3.5), Inches(1.18), "60 GVt·s",
          "Yillik energiya W", TEAL, 24)
footer(s, 7)

# ============================================================
# 8. TRANSFORMATOR YO'QOTISHLARI VA OPTIMIZATSIYA
# ============================================================
s = slide(); header(s, "II bob · Tahlil", "Transformator yo'qotishlari va rejim optimizatsiyasi")
pic_fit(s, "charts/09_transformer.png", Inches(0.5), Inches(1.45), Inches(7.0), Inches(4.1))
data = [
    ["Ko'rsatkich", "Belgi", "Qiymat"],
    ["Nominal quvvat", "Sₙₒₘ", "25 000 kVA"],
    ["Salt yurish yo'qotishi", "ΔPₓₓ", "25 kVt"],
    ["Qisqa tutashuv yo'qotishi", "ΔP_qt", "120 kVt"],
    ["Qisqa tutashuv kuchlanishi", "U_qt", "10,5 %"],
]
table(s, Inches(0.6), Inches(5.5), Inches(6.9), data, col_w=[2.1,0.8,1.1],
      fontsize=11.5, row_h=0.29, head_h=0.36)
rect(s, Inches(7.75), Inches(1.55), Inches(4.9), Inches(5.15), NAVY)
rect(s, Inches(7.75), Inches(1.55), Pt(5), Inches(5.15), GREEN)
txt(s, Inches(8.0), Inches(1.72), Inches(4.5), Inches(0.4), "ASOSIY NATIJA",
    size=13.5, color=GREEN, bold=True)
txt(s, Inches(8.0), Inches(2.2), Inches(4.45), Inches(1.5),
    "Bitta transformatorda ishlash (ikkitasi o'rniga) yillik yo'qotishni "
    "503 → 350 MVt·s ga kamaytiradi.", size=14.5,
    color=RGBColor(0xE6,0xED,0xF7), spacing=1.1)
rect(s, Inches(8.0), Inches(3.95), Inches(4.4), Inches(1.2), COPPER)
txt(s, Inches(8.2), Inches(4.08), Inches(4.0), Inches(1.0),
    "≈ 153 MVt·s/yil tejam\nQO'SHIMCHA INVESTITSIYASIZ", size=16,
    color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(8.0), Inches(5.35), Inches(4.45), Inches(1.2),
    "Transformator yillik yo'qotishi: 349,6 MVt·s\n(salt yurish 219 + yuklama 131).",
    size=12.5, color=MUTED, spacing=1.08)
footer(s, 8)

# ============================================================
# 9. 10 kV FIDERLAR TAHLILI
# ============================================================
s = slide(); header(s, "II bob · Tahlil", "10 kV fiderlar bo'yicha yo'qotishlar hisobi")
pic_fit(s, "charts/03_feeders.png", Inches(0.5), Inches(1.45), Inches(7.2), Inches(3.45))
data = [
    ["Fider", "L, km", "S, mm²", "ΔU, %", "ΔW, MVt·s"],
    ["F-2 turmush", "3,1", "95", "2,08", "153,4"],
    ["F-4 qishloq-1", "5,2", "70", "2,98", "154,0"],
    ["F-5 qishloq-2", "6,0", "70", "2,90", "130,6"],
    ["Jami (8 fider)", "—", "—", "—", "865,6"],
]
table(s, Inches(0.5), Inches(5.0), Inches(7.2), data, col_w=[1.7,0.8,0.8,0.8,1.1],
      fontsize=11.5, row_h=0.32, head_h=0.4, highlight_last=True)
rect(s, Inches(7.95), Inches(1.55), Inches(4.7), Inches(5.15), NAVY)
txt(s, Inches(8.2), Inches(1.72), Inches(4.2), Inches(0.4), "TAHLIL XULOSASI",
    size=13.5, color=COPPERL, bold=True)
bullets(s, Inches(8.2), Inches(2.2), Inches(4.25), Inches(4.4), [
    "Fider liniyalaridagi yillik yo'qotish — 865,6 MVt·s (umumiy yo'qotishning ≈ 49 %).",
    "Eng katta yo'qotish F-2, F-4, F-5 — uzun qishloq fiderlarida.",
    "Sabab: katta uzunlik (5–6 km) va kichik en kesim (70 mm²).",
    "F-4 da ΔU = 2,98 % — me'yor (≤ 5 %) chegarasiga yaqinlashmoqda.",
], size=13.5, color=RGBColor(0xE6,0xED,0xF7), gap=11, mark_color=COPPERL)
footer(s, 9)

# ============================================================
# 10. cos phi VA GARMONIKALAR
# ============================================================
s = slide(); header(s, "II bob · Sifat", "Quvvat koeffitsienti va garmonik buzilishlar")
pic_fit(s, "charts/04_thd.png", Inches(0.5), Inches(1.45), Inches(7.5), Inches(5.5))
stat_card(s, Inches(8.25), Inches(1.55), Inches(4.4), Inches(1.2), "cos φ = 0,85",
          "tan φ = 0,62 · Qₘₐₓ = 7440 kVar", AMBER, 22)
stat_card(s, Inches(8.25), Inches(2.95), Inches(4.4), Inches(1.2), "THD = 8,8 %",
          "me'yor ≤ 8 % — chegaradan yuqori", RED, 22)
rect(s, Inches(8.25), Inches(4.35), Inches(4.4), Inches(2.35), NAVY)
rect(s, Inches(8.25), Inches(4.35), Pt(5), Inches(2.35), TEAL)
txt(s, Inches(8.5), Inches(4.5), Inches(3.95), Inches(0.4),
    "TAVSIYA ETILGAN YECHIM", size=12.5, color=TEAL, bold=True)
txt(s, Inches(8.5), Inches(4.95), Inches(3.95), Inches(1.7),
    "Kondensator batareyalarini rezonansdan himoyalovchi sozlangan drossel "
    "(filtr-reaktor, 7 % yoki 14 %) bilan o'rnatish; passiv garmonik filtrlardan "
    "foydalanish.", size=13.5, color=RGBColor(0xE6,0xED,0xF7), spacing=1.08)
footer(s, 10)

# ============================================================
# 11. TEXNOLOGIYALAR SHARHI
# ============================================================
s = slide(); header(s, "III bob · Yechim", "Energiya sarfini kamaytirish texnologiyalari")
tech = [
    ("Reaktiv quvvat kompensatsiyasi", "UKRM 10,5 kV; 3600 kVar (6×600). cos φ: 0,85→0,95; "
     "S: 14,12→12,63 MVA. Tejam ≈ 284 MVt·s/yil.", COPPER),
    ("Chastota o'zgartiruvchi qurilma (ChOQ)", "110 kVt nasos yuritmasi, PID rostlash. "
     "Tejam ≈ 180 MVt·s/yil; qaytish ≈ 0,9 yil — eng tez.", TEAL),
    ("AMI — aqlli hisobga olish", "Aqlli hisoblagich + konsentrator + MDM. Tijoriy "
     "yo'qotishni keskin kamaytiradi: ≈ 1200 MVt·s/yil.", STEEL),
    ("SCADA / PLC / IoT monitoring", "Real vaqtda nazorat, masofadan boshqaruv, "
     "tarmoqni balanslash. Tejam ≈ 240 MVt·s/yil.", GREEN),
]
yy = Inches(1.5)
for t, d, c in tech:
    rect(s, Inches(0.7), yy, Inches(11.95), Inches(1.22), LIGHT)
    rect(s, Inches(0.7), yy, Pt(6), Inches(1.22), c)
    txt(s, Inches(1.0), yy + Inches(0.13), Inches(11.4), Inches(0.4), t, size=16.5,
        color=c, bold=True)
    txt(s, Inches(1.0), yy + Inches(0.57), Inches(11.4), Inches(0.6), d, size=13.5,
        color=INK, spacing=1.04)
    yy += Inches(1.32)
footer(s, 11)

# ============================================================
# 12. IQTISODIY SAMARADORLIK (NPV)
# ============================================================
s = slide(); header(s, "III bob · Iqtisod", "Iqtisodiy samaradorlik: choralar va NPV")
pic_fit(s, "charts/07_cashflow.png", Inches(0.5), Inches(1.45), Inches(7.5), Inches(3.9))
data = [
    ["Chora", "Tejam\nMVt·s/yil", "Inv.\nmln so'm", "T_q\nyil"],
    ["Reaktiv komp.", "284", "538", "3,1"],
    ["ChOQ", "180", "95", "0,9"],
    ["AMI", "1200", "1730", "2,4"],
    ["SCADA", "240", "640", "4,5"],
    ["Jami (majmua)", "1904", "3003", "2,6"],
]
table(s, Inches(0.5), Inches(5.4), Inches(7.5), data, col_w=[1.7,1.0,1.0,0.7],
      fontsize=10.5, row_h=0.24, head_h=0.38, highlight_last=True)
stat_card(s, Inches(8.25), Inches(1.55), Inches(4.4), Inches(1.25), "≈ 1930 mln so'm",
          "Majmua NPV (r=15%, 8 yil) → NPV>0", GREEN, 22)
stat_card(s, Inches(8.25), Inches(2.95), Inches(4.4), Inches(1.25), "≈ 2,7 yil",
          "Sof oqim musbatga o'tish muddati", COPPER, 22)
stat_card(s, Inches(8.25), Inches(4.35), Inches(4.4), Inches(1.25), "1142 mln so'm/yil",
          "Majmua yillik pul tejami", STEEL, 22)
rect(s, Inches(8.25), Inches(5.75), Inches(4.4), Inches(0.95), CARD)
txt(s, Inches(8.45), Inches(5.85), Inches(4.0), Inches(0.78),
    "Tarif oshsa NPV ortadi — loyiha barqaror foydali (sezgirlik tahlili).",
    size=12, color=INK, spacing=1.05, anchor=MSO_ANCHOR.MIDDLE)
footer(s, 12)

# ============================================================
# 13. NATIJA: OLDIN / KEYIN
# ============================================================
s = slide(); header(s, "Natija", "Choralardan oldin va keyin: qiyosiy tahlil")
pic_fit(s, "charts/08_comparison.png", Inches(0.5), Inches(1.45), Inches(7.6), Inches(5.5))
data = [
    ["Ko'rsatkich", "Gacha", "Keyin"],
    ["Quvvat koeffitsienti cos φ", "0,85", "0,95"],
    ["To'liq quvvat, MVA", "14,12", "12,63"],
    ["Texnik yo'qotish, MVt·s", "1760", "≈ 1400"],
    ["Tijoriy yo'qotish, %", "≈ 2,0", "≈ 0,5"],
    ["Garmonik buzilish THD, %", "8,8", "< 5"],
    ["Umumiy yo'qotish, %", "≈ 5,0", "≈ 3,0"],
]
table(s, Inches(8.3), Inches(1.55), Inches(4.35), data, col_w=[2.1,0.85,0.85],
      fontsize=12, row_h=0.42, head_h=0.44)
footer(s, 13)

# ============================================================
# 14. XULOSA VA AMALIY TAVSIYALAR
# ============================================================
s = slide(); header(s, "Yakun", "Xulosa va amaliy tavsiyalar")
bullets(s, Inches(0.7), Inches(1.4), Inches(12.0), Inches(3.65), [
    "Yo'qotishlar tabiati nazariy asoslandi: ular tok kvadratiga va reaktiv quvvatga bog'liq.",
    "Yillik texnik yo'qotish 1760 MVt·s (2,9 %); 68 % dan ortig'i 10 kV bo'g'inda (F-2/F-4/F-5).",
    "cos φ ni 0,95 ga ko'tarish yuklama yo'qotishini ≈ 20 % (≈ 284 MVt·s) kamaytiradi.",
    "Transformator rejimini optimallashtirish — xarajatsiz ≈ 153 MVt·s/yil tejam.",
    "Choralar qaytishi 0,9–4,5 yil; majmua NPV ≈ 1930 mln so'm → loyiha iqtisodiy asoslangan.",
], size=15, gap=9)
rect(s, Inches(0.7), Inches(5.05), Inches(11.95), Inches(1.65), NAVY)
txt(s, Inches(0.95), Inches(5.18), Inches(11.5), Inches(0.35),
    "TAVSIYA ETILGAN JORIY ETISH KETMA-KETLIGI (YO'L XARITASI)", size=13,
    color=COPPERL, bold=True)
steps = [("1", "Transformator\nrejimi", GREEN), ("2", "ChOQ", TEAL),
         ("3", "Reaktiv\nkompensatsiya", COPPER), ("4", "AMI", AMBER),
         ("5", "SCADA va\nbalanslash", STEEL)]
sx = Inches(0.95)
for n, t, c in steps:
    rect(s, sx, Inches(5.68), Inches(2.05), Inches(0.85), c,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s, sx + Inches(0.1), Inches(5.68), Inches(1.85), Inches(0.85),
        f"{n}.  {t}", size=12, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    sx += Inches(2.32)
footer(s, 14)

# ============================================================
# 15. RAHMAT
# ============================================================
s = slide()
rect(s, 0, 0, SW, SH, NAVY)
rect(s, 0, 0, SW, Inches(0.14), COPPER)
rect(s, 0, SH - Inches(0.14), SW, Inches(0.14), COPPER)
rect(s, Inches(4.67), Inches(3.45), Inches(4.0), Pt(3.5), COPPER)
txt(s, Inches(0.8), Inches(2.5), Inches(11.7), Inches(1.0),
    "E'tiboringiz uchun rahmat!", size=42, color=WHITE, bold=True,
    align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(3.7), Inches(11.7), Inches(0.5),
    "Savollaringizga javob berishga tayyorman", size=17, color=COPPERL,
    italic=True, align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(6.5), Inches(11.7), Inches(0.7),
    "Muxiddinov Sherzod Shaxob o'g'li\n"
    "Ilmiy rahbar: dots. S.Sh. Rustamov  ·  Buxoro davlat texnika universiteti, 2026",
    size=12.5, color=MUTED, align=PP_ALIGN.CENTER, spacing=1.15)

out = "Prezentatsiya_Vobkent_BMI.pptx"
prs.save(out)
print("Saqlandi:", out, "| slaydlar:", len(prs.slides._sldIdLst))
