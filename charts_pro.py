# -*- coding: utf-8 -*-
"""Professional, izchil dizaynli diagrammalar to'plami (himoya uchun)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import os

os.makedirs("charts", exist_ok=True)

# ---- Dizayn tizimi: energetik palitra (navy + mis/copper) ----
NAVY   = "#0B2545"   # quyuq ko'k (asosiy)
BLUE   = "#1F4E79"   # po'lat ko'k
TEAL   = "#2A9D8F"   # turkuaz urg'u
GREEN  = "#2E7D32"   # to'q yashil
AMBER  = "#E0A100"   # oltin/amber
RED    = "#B3261E"   # signal qizil
PURPLE = "#6D597A"   # vazmin siyohrang
COPPER = "#C0792B"   # mis (energetik urg'u)
SLATE  = "#41506B"   # kulrang-ko'k matn
GRID   = "#D7DEEA"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 13,
    "axes.edgecolor": SLATE,
    "axes.linewidth": 0.9,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "axes.titlesize": 15,
    "axes.titleweight": "bold",
    "axes.titlecolor": NAVY,
    "text.color": NAVY,
    "axes.labelcolor": SLATE,
    "xtick.color": SLATE,
    "ytick.color": SLATE,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})


def style(ax, grid_axis="y"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if grid_axis == "y":
        ax.grid(axis="x", visible=False)
    elif grid_axis == "x":
        ax.grid(axis="y", visible=False)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"charts/{name}", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ===== 1. Sutkalik yuklama grafigi (jadval 16 dagi aniq qiymatlar) =====
hours = list(range(24))
P = [6.8,6.2,5.8,5.6,5.7,6.5,8.2,9.6,10.4,10.8,10.9,10.6,
     10.2,10.0,10.1,10.5,11.2,12.0,11.8,11.0,9.8,8.7,7.8,7.1]
fig, ax = plt.subplots(figsize=(9,4.6))
ax.plot(hours, P, color=BLUE, lw=2.6, marker="o", ms=5, zorder=3)
ax.fill_between(hours, P, color=BLUE, alpha=0.10, zorder=1)
ax.axhline(9.05, color=AMBER, ls="--", lw=2, label="O'rtacha  P = 9,05 MVt")
ax.axhline(12.0, color=RED, ls=":", lw=2, label="Maksimal  P = 12,0 MVt")
ax.annotate("Cho'qqi 17:00\n12,0 MVt", xy=(17,12.0), xytext=(13.2,11.2),
            fontsize=11, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
ax.set_xlabel("Sutka soatlari"); ax.set_ylabel("Aktiv quvvat, MVt")
ax.set_title("«Vobkent» PS 10 kV shinalaridagi sutkalik yuklama grafigi")
ax.set_xticks(range(0,24,2)); ax.set_xlim(-0.5,23.5); ax.set_ylim(0,13.5)
ax.legend(loc="lower center", ncol=2, frameon=False, fontsize=11)
style(ax); save(fig, "01_load.png")

# ===== 2. Yo'qotishlar balansi (donut, jadval 4) =====
labels = ["10 kV fiderlar", "10/0,4 kV tr.", "Tr. salt yurish", "110 kV liniya", "Tr. yuklama"]
sizes  = [866, 334, 219, 210, 131]
pcts   = [49.2, 19.0, 12.4, 11.9, 7.4]
colors = [RED, AMBER, BLUE, TEAL, PURPLE]
fig, ax = plt.subplots(figsize=(8.2,5.2))
wedges,_ = ax.pie(sizes, colors=colors, startangle=90,
                  wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2))
ax.text(0,0.12,"1760", ha="center", va="center", fontsize=34, fontweight="bold", color=NAVY)
ax.text(0,-0.22,"MVt·s / yil", ha="center", va="center", fontsize=13, color=SLATE)
ax.text(0,-0.45,"(uzatilgan energiyaning 2,9 %)", ha="center", va="center", fontsize=10, color=SLATE)
leg = [f"{l} — {s} MVt·s ({p} %)" for l,s,p in zip(labels,sizes,pcts)]
ax.legend(wedges, leg, loc="center left", bbox_to_anchor=(1.0,0.5),
          frameon=False, fontsize=11.5)
ax.set_title("Yillik texnik energiya yo'qotishlarining tarkibi", pad=18)
save(fig, "02_balance.png")

# ===== 3. Fider yo'qotishlari (jadval 3) =====
fid = ["F-1","F-2","F-3","F-4","F-5","F-6","F-7","F-8"]
dw  = [142.8,153.4,99.2,154.0,130.6,64.9,90.9,29.8]
cols = [RED if v>=130 else BLUE for v in dw]
fig, ax = plt.subplots(figsize=(9,4.6))
bars = ax.bar(fid, dw, color=cols, width=0.62, zorder=3)
for b,v in zip(bars,dw):
    ax.text(b.get_x()+b.get_width()/2, v+2.5, f"{v:.1f}",
            ha="center", fontsize=10.5, color=NAVY, fontweight="bold")
ax.set_ylabel("Yillik yo'qotish, MVt·s")
ax.set_title("10 kV fiderlar bo'yicha energiya yo'qotishlari (jami 865,6 MVt·s)")
ax.set_ylim(0,175)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=RED,label="Yuqori yo'qotishli (uzun qishloq fiderlari)"),
                   Patch(color=BLUE,label="Boshqa fiderlar")],
          frameon=False, fontsize=10.5, loc="upper right")
style(ax); save(fig, "03_feeders.png")

# ===== 4. Garmonik spektr (jadval 6) =====
orders = ["5","7","11","13"]
mags   = [5.8,3.6,2.4,1.2]
fig, ax = plt.subplots(figsize=(9,4.6))
bars = ax.bar(orders, mags, color=PURPLE, width=0.55, zorder=3)
for b,v in zip(bars,mags):
    ax.text(b.get_x()+b.get_width()/2, v+0.12, f"{v} %",
            ha="center", fontsize=11, color=NAVY, fontweight="bold")
ax.axhline(8.0, color=RED, ls="--", lw=2, label="THD me'yoriy chegara = 8 %")
ax.text(3.05, 8.95, "THD hisoblangan = 8,8 %  (chegaradan yuqori)",
        color=RED, fontsize=11, fontweight="bold", ha="right")
ax.set_xlabel("Garmonika tartibi, n"); ax.set_ylabel("Ulush  Uₙ/U₁, %")
ax.set_title("10 kV shinalardagi kuchlanish garmonik spektri")
ax.set_ylim(0,9.8); ax.legend(loc="upper center", frameon=False, fontsize=11)
style(ax); save(fig, "04_thd.png")

# ===== 5. Oylik iste'mol va yo'qotish (jadval 18) =====
months = ["Yan","Fev","Mar","Apr","May","Iyn","Iyl","Avg","Sen","Okt","Noy","Dek"]
cons   = [5600,5100,4600,4300,4600,5400,5900,5800,4800,4400,4700,5200]
loss   = [164,149,135,126,135,158,173,170,141,129,138,152]
fig, ax = plt.subplots(figsize=(9,4.6))
ax.bar(months, cons, color=BLUE, width=0.6, zorder=3, label="Iste'mol, MVt·s")
ax.set_ylabel("Oylik iste'mol, MVt·s", color=BLUE)
ax.set_ylim(0,6800)
ax2 = ax.twinx()
ax2.plot(months, loss, color=RED, lw=2.4, marker="D", ms=6, label="Yo'qotish, MVt·s")
ax2.set_ylabel("Oylik yo'qotish, MVt·s", color=RED); ax2.grid(False)
ax2.set_ylim(0,210)
ax.set_title("Yillik energiya iste'moli va yo'qotishlarining oylar bo'yicha taqsimoti")
l1,lb1 = ax.get_legend_handles_labels(); l2,lb2 = ax2.get_legend_handles_labels()
ax.legend(l1+l2, lb1+lb2, loc="upper center", ncol=2, frameon=False, fontsize=11)
style(ax); save(fig, "05_monthly.png")

# ===== 6. Choralar: tejam va qaytish (jadval 10) =====
m = ["Reaktiv\nkomp.","ChOQ","AMI","SCADA"]
sav = [284,180,1200,240]
pb  = [3.1,0.9,2.4,4.5]
x = np.arange(len(m))
fig, ax1 = plt.subplots(figsize=(9,4.6))
bars = ax1.bar(x, sav, color=TEAL, width=0.55, zorder=3)
for b,v in zip(bars,sav):
    ax1.text(b.get_x()+b.get_width()/2, v+18, f"{v}", ha="center",
             fontsize=11, color=NAVY, fontweight="bold")
ax1.set_ylabel("Yillik tejam, MVt·s", color=TEAL)
ax1.set_xticks(x); ax1.set_xticklabels(m); ax1.set_ylim(0,1380)
ax2 = ax1.twinx()
ax2.plot(x, pb, color=RED, lw=2.4, marker="o", ms=8, zorder=4)
for xi,p in zip(x,pb):
    ax2.text(xi, p+0.18, f"{p} yil", ha="center", color=RED, fontsize=10.5, fontweight="bold")
ax2.set_ylabel("Qaytish muddati, yil", color=RED); ax2.grid(False); ax2.set_ylim(0,5.5)
ax1.set_title("Choralar bo'yicha yillik tejam va investitsiya qaytish muddati")
style(ax1); save(fig, "06_measures.png")

# ===== 7. Kumulyativ pul oqimi / NPV (jadval 19) =====
years = list(range(9))
nom = [-3003,-1903,-803,297,1397,2497,3597,4697,5797]
npv = [-3003,-2047,-1215,-492,137,684,1160,1574,1934]
fig, ax = plt.subplots(figsize=(9,4.6))
ax.plot(years, nom, color=BLUE, lw=2.6, marker="o", ms=6, label="Kumulyativ oqim (nominal)")
ax.plot(years, npv, color=GREEN, lw=2.6, marker="s", ms=6, label="Kumulyativ NPV (r = 15 %)")
ax.axhline(0, color=SLATE, lw=1.2)
ax.axvline(2.73, color=RED, ls="--", lw=1.8)
ax.annotate("Qaytish ≈ 2,7 yil", xy=(2.73,0), xytext=(3.2,-1500),
            color=RED, fontsize=11, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
ax.fill_between(years, npv, 0, where=[v>=0 for v in npv], color=GREEN, alpha=0.10)
ax.set_xlabel("Loyihaning amal qilish yili"); ax.set_ylabel("Pul oqimi, mln so'm")
ax.set_title("Choralar majmuasining kumulyativ pul oqimi va NPV")
ax.legend(loc="upper left", frameon=False, fontsize=11)
style(ax, "x"); save(fig, "07_cashflow.png")

# ===== 8. Choralargacha va keyin (normalizatsiyalangan, jadval 24) =====
cats = ["cos φ","To'liq quvvat\nMVA","Umumiy\nyo'qotish, %","Tijoriy\nyo'qotish, %","THD, %"]
before = [0.85,14.12,5.0,2.0,8.8]
after  = [0.95,12.63,3.0,0.5,4.8]
x = np.arange(len(cats)); w=0.38
fig, ax = plt.subplots(figsize=(9.2,4.6))
b1 = ax.bar(x-w/2, before, w, color=AMBER, zorder=3, label="Choralargacha")
b2 = ax.bar(x+w/2, after,  w, color=GREEN, zorder=3, label="Choralardan keyin")
for bars in (b1,b2):
    for b in bars:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.15,
                f"{b.get_height():g}", ha="center", fontsize=10, color=NAVY, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(cats)
ax.set_title("Choralardan oldin va keyin: asosiy ko'rsatkichlar qiyosi")
ax.set_ylim(0,16); ax.legend(loc="upper right", frameon=False, fontsize=11)
style(ax); save(fig, "08_comparison.png")

# ===== 9. Transformator rejimi: 2 ta vs 1 ta (jadval 5) =====
modes = ["Ikkita\ntransformator","Bitta\ntransformator\n(optimal)"]
xx = np.arange(2); w=0.38
xy = [438,219]; load_l = [65,131]
fig, ax = plt.subplots(figsize=(8,4.6))
b1 = ax.bar(xx-w/2, xy, w, color=PURPLE, zorder=3, label="Salt yurish yo'qotishi")
b2 = ax.bar(xx+w/2, load_l, w, color=BLUE, zorder=3, label="Yuklama yo'qotishi")
tot = [503,350]
for i,t in enumerate(tot):
    ax.text(i, max(xy[i],load_l[i])+18, f"Jami: {t}", ha="center",
            fontsize=11, color=NAVY, fontweight="bold")
ax.set_xticks(xx); ax.set_xticklabels(modes)
ax.set_ylabel("Yillik yo'qotish, MVt·s")
ax.set_title("Transformator ish rejimini optimallashtirish samarasi")
ax.set_ylim(0,560); ax.legend(frameon=False, fontsize=11, loc="upper right")
ax.annotate("−153 MVt·s/yil\n(xarajatsiz)", xy=(1,350), xytext=(0.45,470),
            color=GREEN, fontsize=11, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.6))
style(ax); save(fig, "09_transformer.png")

# ===== 10. Fider kuchlanish pasayishi (jadval 17) =====
du = [1.64,2.08,1.11,2.98,2.90,1.08,1.74,0.80]
cols = [RED if v>2.5 else (AMBER if v>1.8 else TEAL) for v in du]
fig, ax = plt.subplots(figsize=(9,4.3))
bars = ax.bar(fid, du, color=cols, width=0.6, zorder=3)
for b,v in zip(bars,du):
    ax.text(b.get_x()+b.get_width()/2, v+0.05, f"{v}", ha="center",
            fontsize=10.5, color=NAVY, fontweight="bold")
ax.axhline(5.0, color=SLATE, ls=":", lw=1.5)
ax.set_ylabel("Kuchlanish pasayishi  ΔU, %")
ax.set_title("10 kV fiderlardagi kuchlanish pasayishi (me'yor ≤ 5 %)")
ax.set_ylim(0,3.6)
style(ax); save(fig, "10_voltage.png")

print("PRO charts:", sorted(os.listdir("charts")))
