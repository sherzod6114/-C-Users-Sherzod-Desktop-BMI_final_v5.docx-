# -*- coding: utf-8 -*-
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# Ranglar
DARK = RGBColor(0x0d, 0x1b, 0x3a)
ACCENT = RGBColor(0x1f, 0x6f, 0xeb)
ACCENT2 = RGBColor(0x2e, 0xa0, 0x43)
LIGHT = RGBColor(0xf2, 0xf5, 0xfa)
WHITE = RGBColor(0xff, 0xff, 0xff)
GRAY = RGBColor(0x44, 0x4c, 0x56)
WARN = RGBColor(0xe3, 0x61, 0x1c)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def add_slide():
    return prs.slides.add_slide(BLANK)


def rect(slide, x, y, w, h, color, line=None):
    from pptx.enum.shapes import MSO_SHAPE
    sp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(1)
    sp.shadow.inherit = False
    return sp


def txt(slide, x, y, w, h, text, size=18, color=DARK, bold=False,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font="Calibri", italic=False):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    f = r.font; f.size = Pt(size); f.bold = bold; f.italic = italic
    f.color.rgb = color; f.name = font
    return tb


def bullets(slide, x, y, w, h, items, size=18, color=DARK, gap=6, bullet="•  "):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap); p.space_before = Pt(0)
        lvl = 0
        if isinstance(it, tuple):
            it, lvl = it
        r = p.add_run()
        r.text = ("    " * lvl) + (bullet if lvl == 0 else "–  ") + it
        f = r.font; f.size = Pt(size - lvl*2); f.color.rgb = color; f.name = "Calibri"
    return tb


def header(slide, title, kicker=None):
    rect(slide, 0, 0, SW, Inches(1.15), DARK)
    rect(slide, 0, Inches(1.15), SW, Inches(0.06), ACCENT)
    txt(slide, Inches(0.5), Inches(0.18), Inches(12.3), Inches(0.8),
        title, size=26, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    if kicker:
        txt(slide, Inches(0.55), Inches(0.02), Inches(12), Inches(0.3),
            kicker, size=12, color=ACCENT, bold=True)


def pagenum(slide, n):
    txt(slide, Inches(12.3), Inches(7.0), Inches(0.9), Inches(0.4),
        str(n), size=12, color=GRAY, align=PP_ALIGN.RIGHT)


def pic_fit(slide, path, x, y, w, h):
    """Rasmni berilgan ramkaga nisbatni saqlab joylashtirish (markazlangan)."""
    from PIL import Image
    iw, ih = Image.open(path).size
    fr = w / h; ir = iw / ih
    if ir > fr:
        nw = w; nh = int(w / ir)
    else:
        nh = h; nw = int(h * ir)
    nx = x + (w - nw)//2; ny = y + (h - nh)//2
    slide.shapes.add_picture(path, nx, ny, nw, nh)


# ---------- 1. TITUL ----------
s = add_slide()
rect(s, 0, 0, SW, SH, DARK)
rect(s, 0, Inches(2.55), SW, Inches(0.07), ACCENT)
rect(s, 0, Inches(4.62), SW, Inches(0.07), ACCENT)
txt(s, Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.5),
    "O'ZBEKISTON RESPUBLIKASI OLIY TA'LIM, FAN VA INNOVATSIYALAR VAZIRLIGI",
    size=14, color=RGBColor(0x9f,0xb4,0xd6), bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.4),
    "«Elektr energetikasi» kafedrasi", size=14,
    color=RGBColor(0x9f,0xb4,0xd6), align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(1.65), Inches(11.7), Inches(0.5),
    "BITIRUV MALAKAVIY ISHI", size=20, color=ACCENT2, bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(2.75), Inches(11.7), Inches(1.7),
    "ELEKTR TA'MINOTI TIZIMLARIDA ENERGIYA SARFINI KAMAYTIRISH TEXNOLOGIYALARINI TADQIQOT QILISH",
    size=28, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(0.8), Inches(4.7), Inches(11.7), Inches(0.5),
    "Buxoro viloyati «Vobkent» 110/35/10 kV podstansiyasi misolida",
    size=16, color=RGBColor(0xc9,0xd6,0xea), italic=True, align=PP_ALIGN.CENTER)
txt(s, Inches(2.0), Inches(5.55), Inches(9.3), Inches(1.3),
    "Bajardi:  ____________________\n"
    "Ilmiy rahbar:  ____________________\n"
    "Kafedra mudiri:  ____________________",
    size=15, color=RGBColor(0xc9,0xd6,0xea), align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(6.95), Inches(11.7), Inches(0.4),
    "Buxoro — 2026", size=14, color=RGBColor(0x9f,0xb4,0xd6), bold=True, align=PP_ALIGN.CENTER)

# ---------- 2. DOLZARBLIK ----------
s = add_slide(); header(s, "Mavzuning dolzarbligi", "KIRISH")
rect(s, Inches(0.5), Inches(1.5), Inches(7.4), Inches(5.5), LIGHT)
bullets(s, Inches(0.8), Inches(1.75), Inches(6.9), Inches(5.1), [
    "Elektr energiyasi manbadan iste'molchigacha bo'lgan zanjirning har bir bo'g'inida bir qismi yo'qoladi.",
    "O'zbekiston tarmoqlarida texnik va tijoriy yo'qotishlar ulushi rivojlangan davlatlardan yuqori.",
    "Yo'qotishlarning asosiy qismi 6–10 kV va 0,4 kV taqsimlash tarmoqlarida yuzaga keladi.",
    "Tarmoqda tejalgan har bir kVt·s — manbada qo'shimcha ishlab chiqarilishi shart bo'lmagan energiya, yoqilg'i va chiqindi tejami.",
    "Yo'qotishlarni kamaytirish — yangi quvvat qurishdan ko'ra ancha arzon yo'l.",
], size=17, gap=11)
rect(s, Inches(8.2), Inches(1.7), Inches(4.6), Inches(2.55), DARK)
txt(s, Inches(8.4), Inches(1.95), Inches(4.2), Inches(0.5),
    "Muammoning markazi", size=15, color=ACCENT2, bold=True)
txt(s, Inches(8.4), Inches(2.5), Inches(4.2), Inches(1.7),
    "Isish yo'qotishlari tokning KVADRATIGA proporsional — kichik tok kamayishi katta tejam beradi.",
    size=16, color=WHITE)
rect(s, Inches(8.2), Inches(4.45), Inches(4.6), Inches(2.55), ACCENT)
txt(s, Inches(8.4), Inches(4.7), Inches(4.2), Inches(2.1),
    "Zamonaviy vositalar:\n• Reaktiv quvvat kompensatsiyasi\n• Chastota o'zgartiruvchi qurilma\n• AMI — aqlli hisob\n• SCADA — dispetcher nazorati",
    size=15, color=WHITE, bold=True)
pagenum(s, 2)

# ---------- 3. MAQSAD VA VAZIFALAR ----------
s = add_slide(); header(s, "Ishning maqsadi va vazifalari", "KIRISH")
rect(s, Inches(0.5), Inches(1.5), Inches(5.6), Inches(5.5), ACCENT)
txt(s, Inches(0.8), Inches(1.75), Inches(5.0), Inches(0.6),
    "MAQSAD", size=18, color=WHITE, bold=True)
txt(s, Inches(0.8), Inches(2.4), Inches(5.0), Inches(4.2),
    "Elektr ta'minoti tizimlarida energiya sarfini kamaytirish texnologiyalarini nazariy va amaliy "
    "jihatdan tadqiq etish hamda tanlangan obyekt uchun texnik va iqtisodiy jihatdan asoslangan "
    "tavsiyalar ishlab chiqish.", size=18, color=WHITE)
txt(s, Inches(6.4), Inches(1.55), Inches(6.4), Inches(0.5),
    "VAZIFALAR", size=18, color=DARK, bold=True)
bullets(s, Inches(6.4), Inches(2.1), Inches(6.6), Inches(5.0), [
    "Yo'qotishlar turlari va yuzaga kelish mexanizmlarini o'rganish;",
    "Podstansiya va 10 kV tarmoqda yuklama, kuchlanish pasayishi, transformator va kabel yo'qotishlarini hisoblash;",
    "Garmonik buzilishlar va energiya sifatini baholash;",
    "Zamonaviy texnologiyalar ishlash tamoyilini tahlil qilish;",
    "Choralar texnik samarasi va qaytish muddatini hisoblash;",
    "Elektr xavfsizligi va mehnat muhofazasi tavsiyalarini berish.",
], size=15, gap=9)
pagenum(s, 3)

# ---------- 4. OBYEKT VA PREDMET ----------
s = add_slide(); header(s, "Tadqiqot obyekti va predmeti", "KIRISH")
rect(s, Inches(0.5), Inches(1.5), Inches(12.3), Inches(2.2), LIGHT)
txt(s, Inches(0.8), Inches(1.7), Inches(11.7), Inches(0.5),
    "OBYEKT", size=16, color=ACCENT, bold=True)
txt(s, Inches(0.8), Inches(2.2), Inches(11.7), Inches(1.4),
    "Buxoro viloyati Vobkent tumanidagi «Vobkent» 110/35/10 kV taqsimlash podstansiyasi va unga "
    "ulangan 10 kV taqsimlash tarmog'i. Modernizatsiya doirasida 16 000 kVA transformator "
    "25 000 kVA quvvatli transformatorga almashtirilgan. («Buxoro hududiy elektr tarmoqlari korxonasi» AJ).",
    size=16, color=DARK)
rect(s, Inches(0.5), Inches(3.9), Inches(12.3), Inches(1.3), DARK)
txt(s, Inches(0.8), Inches(4.05), Inches(11.7), Inches(0.5),
    "PREDMET", size=16, color=ACCENT2, bold=True)
txt(s, Inches(0.8), Inches(4.5), Inches(11.7), Inches(0.6),
    "Tizimda energiya yo'qotishlarini kamaytirish texnologiyalari va ularning samaradorligini baholash usullari.",
    size=16, color=WHITE)
# kichik ko'rsatkichlar kartalari
cards = [("110/35/10", "kV kuchlanish"), ("25 000", "kVA transformator"),
         ("8", "ta 10 kV fider"), ("60", "GVt·s yillik energiya")]
cx = Inches(0.5)
for val, lab in cards:
    rect(s, cx, Inches(5.45), Inches(2.95), Inches(1.4), ACCENT)
    txt(s, cx, Inches(5.6), Inches(2.95), Inches(0.7), val, size=30, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    txt(s, cx, Inches(6.35), Inches(2.95), Inches(0.45), lab, size=13, color=WHITE, align=PP_ALIGN.CENTER)
    cx += Inches(3.07)
pagenum(s, 4)

# ---------- 5. I BOB NAZARIY ----------
s = add_slide(); header(s, "I bob. Yo'qotishlarning nazariy asoslari", "NAZARIYA")
bullets(s, Inches(0.6), Inches(1.5), Inches(6.3), Inches(5.5), [
    "Yo'qotishlar tabiati bo'yicha: YUKLAMAGA BOG'LIQ (o'zgaruvchan) va DOIMIY (salt yurish);",
    "Kelib chiqishi bo'yicha: TEXNIK va TIJORIY;",
    "Yuklama yo'qotishi:  ΔP = 3·I²·R  — tok kvadratiga bog'liq;",
    "Reaktiv quvvat to'liq tokni oshiradi → barcha elementlarda yo'qotish ortadi;",
    "Energiya sifati: kuchlanish chetlanishi, THD (garmonik buzilish);",
    "Iqtisodiy tok zichligi — o'tkazgich en kesimini optimal tanlash mezoni.",
], size=16, gap=11)
rect(s, Inches(7.1), Inches(1.6), Inches(5.7), Inches(2.3), LIGHT)
txt(s, Inches(7.3), Inches(1.75), Inches(5.3), Inches(0.4), "Asosiy formula", size=14, color=ACCENT, bold=True)
txt(s, Inches(7.3), Inches(2.25), Inches(5.3), Inches(1.5),
    "ΔP = 3 · I² · R\n\nTok 2 barobar oshsa — yo'qotish 4 barobar ortadi",
    size=20, color=DARK, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
rect(s, Inches(7.1), Inches(4.1), Inches(5.7), Inches(2.9), DARK)
txt(s, Inches(7.3), Inches(4.3), Inches(5.3), Inches(0.4), "Nazariy baza", size=14, color=ACCENT2, bold=True)
txt(s, Inches(7.3), Inches(4.8), Inches(5.3), Inches(2.0),
    "Yu. S. Jelezko — yo'qotish va reaktiv quvvat hisobi\n"
    "V. I. Idelchik — tarmoq rejimlari nazariyasi\n"
    "F. F. Karpov — reaktiv quvvat kompensatsiyasi\n"
    "GOST 32144 — energiya sifati normalari",
    size=15, color=WHITE)
pagenum(s, 5)

# ---------- 6. II BOB - YUKLAMA GRAFIGI ----------
s = add_slide(); header(s, "Yuklama tahlili va sutkalik grafik", "TAHLIL · 2.1")
pic_fit(s, "charts/01_load.png", Inches(0.4), Inches(1.45), Inches(8.0), Inches(5.6))
rect(s, Inches(8.6), Inches(1.6), Inches(4.3), Inches(5.3), LIGHT)
txt(s, Inches(8.8), Inches(1.8), Inches(3.9), Inches(0.4), "Asosiy ko'rsatkichlar", size=15, color=ACCENT, bold=True)
metrics = [("Pₘₐₓ", "12,0 MVt"), ("Pₒ'ʳ", "9,05 MVt"),
           ("k_t (to'ldirilganlik)", "0,75"), ("Yillik energiya W", "60 GVt·s")]
yy = Inches(2.35)
for lab, val in metrics:
    txt(s, Inches(8.8), yy, Inches(3.9), Inches(0.35), lab, size=14, color=GRAY)
    txt(s, Inches(8.8), yy+Inches(0.32), Inches(3.9), Inches(0.5), val, size=22, color=DARK, bold=True)
    yy += Inches(1.05)
pagenum(s, 6)

# ---------- 7. TRANSFORMATOR VA FIDER ----------
s = add_slide(); header(s, "Transformator va fider yo'qotishlari", "TAHLIL · 2.2")
pic_fit(s, "charts/03_feeders.png", Inches(0.4), Inches(1.4), Inches(7.6), Inches(5.7))
bullets(s, Inches(8.2), Inches(1.7), Inches(4.8), Inches(3.0), [
    "Transformator salt yurish: 219 MVt·s",
    "Transformator yuklama: 131 MVt·s",
    "Jami transformator: 349,6 MVt·s",
    "10 kV fiderlar (jami): 866 MVt·s",
], size=16, gap=10)
rect(s, Inches(8.2), Inches(4.7), Inches(4.8), Inches(2.2), WARN)
txt(s, Inches(8.4), Inches(4.9), Inches(4.4), Inches(1.9),
    "Eng katta yo'qotish:\nF-2, F-4, F-5 — uzun qishloq fiderlari.\n"
    "Sabab: katta uzunlik (5–6 km) va kichik en kesim (70 mm²).",
    size=15, color=WHITE, bold=True)
pagenum(s, 7)

# ---------- 8. YO'QOTISHLAR TARKIBI (PIE) ----------
s = add_slide(); header(s, "Yillik yo'qotishlar tarkibi", "TAHLIL · 2.3")
pic_fit(s, "charts/02_losses_pie.png", Inches(0.4), Inches(1.45), Inches(7.2), Inches(5.6))
rect(s, Inches(7.9), Inches(1.7), Inches(5.0), Inches(2.4), DARK)
txt(s, Inches(8.1), Inches(2.0), Inches(4.6), Inches(2.0),
    "Yillik texnik yo'qotish:\n1760 MVt·s\n= uzatilgan energiyaning 2,9 %",
    size=20, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
bullets(s, Inches(7.9), Inches(4.35), Inches(5.0), Inches(2.6), [
    "68 % dan ortig'i — 10 kV bo'g'inda;",
    "10 kV fiderlar — 49,2 % (eng katta ulush);",
    "Demak asosiy zaxira aynan taqsimlash tarmog'ida.",
], size=16, gap=10)
pagenum(s, 8)

# ---------- 9. cos phi va THD ----------
s = add_slide(); header(s, "Quvvat koeffitsienti va garmonikalar", "TAHLIL · 2.3")
pic_fit(s, "charts/04_thd.png", Inches(0.4), Inches(1.4), Inches(7.4), Inches(5.7))
rect(s, Inches(8.0), Inches(1.7), Inches(4.9), Inches(2.4), LIGHT)
txt(s, Inches(8.2), Inches(1.9), Inches(4.5), Inches(0.4), "Quvvat koeffitsienti", size=14, color=ACCENT, bold=True)
txt(s, Inches(8.2), Inches(2.35), Inches(4.5), Inches(1.6),
    "cos φ = 0,85   →   tan φ = 0,62\nQₘₐₓ = 7440 kVar\nSₘₐₓ = 14,12 MVA",
    size=18, color=DARK, bold=True)
rect(s, Inches(8.0), Inches(4.3), Inches(4.9), Inches(2.6), WARN)
txt(s, Inches(8.2), Inches(4.5), Inches(4.5), Inches(2.2),
    "THD = 8,8 %\n(8 % chegaradan yuqori)\n\nYechim: kondensator batareyalarini "
    "rezonansdan himoyalovchi sozlangan drossel (filtr-reaktor) bilan o'rnatish.",
    size=15, color=WHITE, bold=True)
pagenum(s, 9)

# ---------- 10. QISQA TUTASHUV VA ZAXIRA ----------
s = add_slide(); header(s, "Qisqa tutashuv toklari va zaxiralar", "TAHLIL · 2.4–2.5")
boxes = [("11,9 kA", "Qisqa tutashuv toki, Iₖ"),
         ("30,3 kA", "Zarba toki, iₐ"),
         ("OK", "Taqsimlash qurilmasi\nshartlarga javob beradi")]
cx = Inches(0.5)
for val, lab in boxes:
    rect(s, cx, Inches(1.6), Inches(4.0), Inches(1.9), ACCENT)
    txt(s, cx, Inches(1.8), Inches(4.0), Inches(0.8), val, size=34, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    txt(s, cx, Inches(2.75), Inches(4.0), Inches(0.7), lab, size=14, color=WHITE, align=PP_ALIGN.CENTER)
    cx += Inches(4.27)
txt(s, Inches(0.5), Inches(3.8), Inches(12), Inches(0.5),
    "Yo'qotishlarni kamaytirish zaxiralari:", size=18, color=DARK, bold=True)
bullets(s, Inches(0.7), Inches(4.35), Inches(12.0), Inches(2.6), [
    "cos φ ni 0,85 → 0,95 ga ko'tarish — yuklamaga bog'liq yo'qotishlarni ≈ 20 % kamaytiradi;",
    "Transformator ish rejimini optimallashtirish — QO'SHIMCHA INVESTITSIYASIZ yiliga ≈ 153 MVt·s tejam;",
    "Uzun fiderlarni balanslash va en kesimni oshirish;",
    "Garmonikalarni filtr orqali cheklash (THD < 5 %).",
], size=17, gap=11)
pagenum(s, 10)

# ---------- 11. III BOB - TEXNOLOGIYALAR ----------
s = add_slide(); header(s, "III bob. Kamaytirish texnologiyalari", "YECHIM · 3.1")
tech = [
    ("Reaktiv quvvat kompensatsiyasi", "Q_k = 3500 kVar avtomatik kondensator (UKRM). "
     "S: 14,12 → 12,63 MVA. Yo'qotish −20 % ≈ 284 MVt·s/yil.", ACCENT),
    ("Chastota o'zgartiruvchi qurilma (ChOQ)", "Nasos yuklamasini PID rostlash. "
     "Tejam ≈ 180 MVt·s/yil, qaytish ≈ 0,9 yil — eng tez.", ACCENT2),
    ("AMI — aqlli hisobga olish", "Masofadan o'qish, ikki tomonlama aloqa. "
     "Tijoriy yo'qotishni keskin kamaytiradi: ≈ 1200 MVt·s/yil.", WARN),
    ("SCADA / PLC / IoT monitoring", "Real vaqtda nazorat va tarmoq balanslash. "
     "Tejam ≈ 240 MVt·s/yil.", DARK),
]
yy = Inches(1.45)
for title, desc, col in tech:
    rect(s, Inches(0.5), yy, Inches(0.18), Inches(1.18), col)
    rect(s, Inches(0.68), yy, Inches(12.15), Inches(1.18), LIGHT)
    txt(s, Inches(0.95), yy+Inches(0.1), Inches(11.7), Inches(0.4), title, size=17, color=col, bold=True)
    txt(s, Inches(0.95), yy+Inches(0.55), Inches(11.7), Inches(0.6), desc, size=14, color=GRAY)
    yy += Inches(1.34)
pagenum(s, 11)

# ---------- 12. IQTISODIY SAMARADORLIK - CHORALAR ----------
s = add_slide(); header(s, "Choralar samaradorligi", "IQTISOD · 3.4")
pic_fit(s, "charts/05_measures.png", Inches(0.4), Inches(1.45), Inches(8.2), Inches(5.6))
rect(s, Inches(8.8), Inches(1.7), Inches(4.1), Inches(5.2), DARK)
txt(s, Inches(9.0), Inches(1.9), Inches(3.7), Inches(0.4), "Majmua (jami)", size=15, color=ACCENT2, bold=True)
mm = [("Tejam", "1904 MVt·s/yil"), ("≈", "1142 mln so'm/yil"),
      ("Investitsiya", "3003 mln so'm"), ("Qaytish (T_q)", "≈ 2,6 yil")]
yy = Inches(2.4)
for lab, val in mm:
    txt(s, Inches(9.0), yy, Inches(3.7), Inches(0.3), lab, size=13, color=RGBColor(0x9f,0xb4,0xd6))
    txt(s, Inches(9.0), yy+Inches(0.3), Inches(3.7), Inches(0.5), val, size=19, color=WHITE, bold=True)
    yy += Inches(1.05)
pagenum(s, 12)

# ---------- 13. NPV / PUL OQIMI ----------
s = add_slide(); header(s, "Iqtisodiy asoslash: NPV va qaytish", "IQTISOD · 3.4")
pic_fit(s, "charts/06_cashflow.png", Inches(0.4), Inches(1.45), Inches(8.2), Inches(5.6))
rect(s, Inches(8.8), Inches(1.7), Inches(4.1), Inches(2.5), ACCENT2)
txt(s, Inches(9.0), Inches(1.95), Inches(3.7), Inches(2.1),
    "NPV ≈ 1930 mln so'm\n(r = 15 %, 8 yil)\n\nNPV > 0 → loyiha iqtisodiy jihatdan ASOSLANGAN",
    size=17, color=WHITE, bold=True)
bullets(s, Inches(8.8), Inches(4.4), Inches(4.1), Inches(2.5), [
    "Sof oqim ≈ 2,7-yilda musbatga o'tadi;",
    "Diskontlangan tejam ≈ 4936 mln so'm;",
    "Tarif oshsa NPV ham ortadi (sezgirlik tahlili).",
], size=14, gap=9)
pagenum(s, 13)

# ---------- 14. CHORALARGACHA / KEYIN ----------
s = add_slide(); header(s, "Natija: choralargacha va keyin", "NATIJA")
pic_fit(s, "charts/07_comparison.png", Inches(0.4), Inches(1.45), Inches(8.2), Inches(5.6))
rect(s, Inches(8.8), Inches(1.7), Inches(4.1), Inches(5.2), LIGHT)
txt(s, Inches(9.0), Inches(1.9), Inches(3.7), Inches(0.4), "Qiyosiy o'zgarish", size=15, color=ACCENT, bold=True)
comp = [("cos φ", "0,85 → 0,95"), ("To'liq quvvat", "14,12 → 12,63 MVA"),
        ("THD", "8,8 % → < 5 %"), ("Umumiy yo'qotish", "≈ 5,0 % → ≈ 3,0 %"),
        ("Tijoriy yo'qotish", "≈ 2,0 % → ≈ 0,5 %")]
yy = Inches(2.4)
for lab, val in comp:
    txt(s, Inches(9.0), yy, Inches(3.7), Inches(0.3), lab, size=13, color=GRAY)
    txt(s, Inches(9.0), yy+Inches(0.28), Inches(3.7), Inches(0.45), val, size=17, color=DARK, bold=True)
    yy += Inches(0.86)
pagenum(s, 14)

# ---------- 15. XAVFSIZLIK ----------
s = add_slide(); header(s, "Hayot faoliyati xavfsizligi", "BOB 3.5")
rect(s, Inches(0.5), Inches(1.55), Inches(6.1), Inches(5.3), LIGHT)
txt(s, Inches(0.75), Inches(1.7), Inches(5.6), Inches(0.4), "Elektr xavfsizligi", size=16, color=ACCENT, bold=True)
bullets(s, Inches(0.75), Inches(2.2), Inches(5.6), Inches(4.5), [
    "Yerga ulash va zanulleniye (GOST 12.1.030);",
    "Tegish kuchlanishi va tok chegaralari (GOST 12.1.038);",
    "Shaxsiy himoya vositalari (SHHV);",
    "Relay himoyasi: maksimal tok, differensial, gaz himoyasi;",
    "Bloklash va ogohlantiruvchi belgilar.",
], size=15, gap=9)
rect(s, Inches(6.9), Inches(1.55), Inches(5.9), Inches(5.3), DARK)
txt(s, Inches(7.15), Inches(1.7), Inches(5.4), Inches(0.4), "Yong'in, ekologiya, sanitariya", size=16, color=ACCENT2, bold=True)
bullets(s, Inches(7.15), Inches(2.2), Inches(5.4), Inches(4.5), [
    "Transformator moyi — yong'in xavfi, moy yig'gich;",
    "Yong'inga qarshi vositalar va avtomatik signalizatsiya;",
    "Elektromagnit maydon va shovqin me'yorlari;",
    "Ishlab chiqarish chiqindilarini boshqarish;",
    "Sanitariya-gigiyena talablariga rioya.",
], size=15, color=WHITE, gap=9)
pagenum(s, 15)

# ---------- 16. XULOSA ----------
s = add_slide(); header(s, "Xulosa va tavsiyalar", "YAKUN")
bullets(s, Inches(0.6), Inches(1.45), Inches(12.4), Inches(4.0), [
    "Yo'qotishlar tabiati nazariy asoslandi: ular tok kvadratiga va reaktiv quvvatga bog'liq.",
    "Yillik texnik yo'qotish 1760 MVt·s (2,9 %), 68 % dan ortig'i — 10 kV bo'g'inda.",
    "cos φ ni 0,95 ga ko'tarish yuklamaga bog'liq yo'qotishlarni ≈ 20 % kamaytiradi.",
    "Transformator rejimini optimallashtirish — xarajatsiz ≈ 153 MVt·s/yil tejam.",
    "Choralar qaytishi 0,9–4,5 yil; majmua uchun NPV ≈ 1930 mln so'm (musbat → asoslangan).",
], size=16, gap=9)
rect(s, Inches(0.5), Inches(5.35), Inches(12.3), Inches(1.55), ACCENT)
txt(s, Inches(0.75), Inches(5.5), Inches(11.8), Inches(0.4), "Tavsiya etilgan ketma-ketlik:", size=15, color=WHITE, bold=True)
txt(s, Inches(0.75), Inches(5.95), Inches(11.8), Inches(0.9),
    "1) Transformator rejimini optimallashtirish (xarajatsiz)  →  2) ChOQ  →  "
    "3) Reaktiv quvvat kompensatsiyasi  →  4) AMI  →  5) SCADA va balanslash",
    size=15, color=WHITE, bold=True)
pagenum(s, 16)

# ---------- 17. RAHMAT ----------
s = add_slide()
rect(s, 0, 0, SW, SH, DARK)
rect(s, Inches(4.5), Inches(3.35), Inches(4.3), Inches(0.06), ACCENT)
txt(s, Inches(0.8), Inches(2.6), Inches(11.7), Inches(1.0),
    "E'tiboringiz uchun rahmat!", size=40, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(3.6), Inches(11.7), Inches(0.6),
    "Savollaringizga javob berishga tayyorman", size=18,
    color=RGBColor(0x9f,0xb4,0xd6), italic=True, align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(6.6), Inches(11.7), Inches(0.5),
    "Vobkent 110/35/10 kV podstansiyasi  ·  Buxoro — 2026", size=13,
    color=RGBColor(0x6f,0x82,0xa6), align=PP_ALIGN.CENTER)

out = "Prezentatsiya_Vobkent_BMI.pptx"
prs.save(out)
print("Saqlandi:", out, "| slaydlar:", len(prs.slides._sldIdLst))
