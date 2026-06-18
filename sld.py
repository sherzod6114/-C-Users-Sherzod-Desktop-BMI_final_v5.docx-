# -*- coding: utf-8 -*-
"""«Vobkent» 110/35/10 kV podstansiyasining bir chiziqli (prinsipial) sxemasi."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrow
import os

os.makedirs("charts", exist_ok=True)

NAVY   = "#0B1F3A"
COPPER = "#C47A2C"
STEEL  = "#2E5A88"
RED    = "#C0392B"
INK    = "#1F2A3A"
GRID   = "#E3E8F0"

fig, ax = plt.subplots(figsize=(11.2, 7.2))
ax.set_xlim(0, 12); ax.set_ylim(0, 10)
ax.axis("off")

LW = 2.2

def line(x1, y1, x2, y2, color=NAVY, lw=LW, z=2):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, solid_capstyle="round", zorder=z)

def busbar(x1, x2, y, label, color=NAVY):
    ax.plot([x1, x2], [y, y], color=color, lw=6, solid_capstyle="round", zorder=3)
    ax.text(x1 - 0.15, y, label, ha="right", va="center", fontsize=12,
            fontweight="bold", color=color)

def breaker(x, y, size=0.22):
    # vyklyuchatel — to'ldirilgan kvadrat
    ax.add_patch(Rectangle((x - size/2, y - size/2), size, size,
                 facecolor=NAVY, edgecolor=NAVY, zorder=4))

def disconnector(x, y, h=0.42):
    # razъedinitel — qiya uzilgan kontakt
    line(x, y - h/2, x, y - h/2 + 0.05, color=NAVY)
    ax.plot([x, x + 0.16], [y - 0.06, y + h/2], color=NAVY, lw=LW, zorder=4)
    ax.plot([x, x], [y + h/2, y + h/2 + 0.05], color=NAVY, lw=LW, zorder=4)
    ax.add_patch(Circle((x, y - 0.06), 0.025, color=NAVY, zorder=5))

def winding(x, y, r, label, color=COPPER):
    ax.add_patch(Circle((x, y), r, fill=False, edgecolor=color, lw=2.4, zorder=4))
    ax.text(x, y, label, ha="center", va="center", fontsize=10.5,
            fontweight="bold", color=color)

def feeder(x, y_top, label, sub):
    line(x, y_top, x, y_top - 0.45)
    disconnector(x, y_top - 0.7)
    breaker(x, y_top - 1.15)
    line(x, y_top - 1.27, x, y_top - 1.62)
    ax.add_patch(FancyArrow(x, y_top - 1.62, 0, -0.28, width=0.001,
                 head_width=0.13, head_length=0.16, color=NAVY, zorder=4))
    ax.text(x, y_top - 2.18, label, ha="center", va="top", fontsize=10,
            fontweight="bold", color=INK)
    ax.text(x, y_top - 2.48, sub, ha="center", va="top", fontsize=8, color=STEEL)

# ---- Sarlavha ----
ax.text(6, 9.62, "«VOBKENT» 110/35/10 kV PODSTANSIYASINING BIR CHIZIQLI SXEMASI",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color=NAVY)
ax.plot([1.2, 10.8], [9.32, 9.32], color=COPPER, lw=2.5)

# ---- 110 kV kirish liniyasi ----
ax.add_patch(FancyArrow(6, 9.15, 0, -0.35, width=0.001, head_width=0.16,
             head_length=0.18, color=NAVY, zorder=4))
ax.text(6.25, 9.0, "110 kV liniya\n(manba S_k = 1500 MVA)", ha="left", va="center",
        fontsize=9.5, color=STEEL)
line(6, 8.8, 6, 8.5)

# ---- 110 kV shina ----
busbar(4.2, 7.8, 8.4, "110 kV")

# ---- 110 kV dan transformatorgacha tushish ----
line(6, 8.4, 6, 8.05)
disconnector(6, 7.85)
breaker(6, 7.35)
line(6, 7.23, 6, 6.95)

# ---- Uch chulg'amli transformator 110/35/10 kV ----
winding(6, 6.55, 0.42, "110")           # HV
winding(5.6, 5.9, 0.42, "35")           # MV
winding(6.4, 5.9, 0.42, "10")           # LV
ax.text(7.05, 6.2, "T: 110/35/10 kV\n25 000 kVA\nU_qt = 10,5 %",
        ha="left", va="center", fontsize=9.5, fontweight="bold", color=COPPER)

# ---- 35 kV tomon ----
line(5.6, 5.48, 5.6, 4.95)
line(5.6, 4.95, 3.0, 4.95)
line(3.0, 4.95, 3.0, 4.2)
disconnector(3.0, 4.0)
breaker(3.0, 3.55)
line(3.0, 3.43, 3.0, 3.15)
busbar(1.4, 4.0, 3.0, "35 kV")
# 35 kV fiderlar (2 ta)
for i, x in enumerate([2.0, 3.4], 1):
    line(x, 3.0, x, 2.7)
    disconnector(x, 2.5)
    breaker(x, 2.05)
    line(x, 1.93, x, 1.6)
    ax.add_patch(FancyArrow(x, 1.6, 0, -0.25, width=0.001, head_width=0.12,
                 head_length=0.14, color=NAVY, zorder=4))
    ax.text(x, 1.15, f"35 kV\nfider {i}", ha="center", va="top", fontsize=8.5,
            color=INK)

# ---- 10 kV tomon ----
line(6.4, 5.48, 6.4, 4.95)
line(6.4, 4.95, 8.0, 4.95)
line(8.0, 4.95, 8.0, 4.2)
disconnector(8.0, 4.0)
breaker(8.0, 3.55)
line(8.0, 3.43, 8.0, 3.15)
busbar(6.0, 10.4, 3.15, "10 kV")

# 10 kV fiderlar (8 ta)
fid = [
    ("F-1", "markaz"), ("F-2", "turmush"), ("F-3", "sanoat"),
    ("F-4", "qishloq-1"), ("F-5", "qishloq-2"), ("F-6", "nasos"),
    ("F-7", "aralash"), ("F-8", "zaxira"),
]
xs = [6.3 + i*0.58 for i in range(8)]
for x, (f, s) in zip(xs, fid):
    feeder(x, 3.15, f, s)

# ---- Belgilar legendasi ----
lx, ly = 0.6, 7.9
ax.add_patch(Rectangle((lx - 0.35, ly - 1.55), 2.7, 2.0, facecolor="white",
             edgecolor=GRID, lw=1.5, zorder=1))
ax.text(lx + 1.0, ly + 0.28, "Shartli belgilar", ha="center", fontsize=10,
        fontweight="bold", color=NAVY)
# breaker
ax.add_patch(Rectangle((lx, ly - 0.12), 0.2, 0.2, facecolor=NAVY, zorder=5))
ax.text(lx + 0.4, ly - 0.02, "Vыklyuchatel", fontsize=9, va="center", color=INK)
# disconnector
ax.plot([lx + 0.1, lx + 0.26], [ly - 0.6, ly - 0.4], color=NAVY, lw=2, zorder=5)
ax.add_patch(Circle((lx + 0.1, ly - 0.6), 0.022, color=NAVY, zorder=5))
ax.text(lx + 0.4, ly - 0.5, "Ajratgich", fontsize=9, va="center", color=INK)
# transformer
ax.add_patch(Circle((lx + 0.12, ly - 0.95), 0.12, fill=False, edgecolor=COPPER,
             lw=2, zorder=5))
ax.text(lx + 0.4, ly - 0.95, "Transformator", fontsize=9, va="center", color=INK)
# bus
ax.plot([lx, lx + 0.24], [ly - 1.35, ly - 1.35], color=NAVY, lw=5, zorder=5)
ax.text(lx + 0.4, ly - 1.35, "Shina (sistema)", fontsize=9, va="center", color=INK)

fig.tight_layout()
fig.savefig("charts/00_sld.png", dpi=170, bbox_inches="tight", facecolor="white")
plt.close(fig)
print("SLD saqlandi: charts/00_sld.png")
