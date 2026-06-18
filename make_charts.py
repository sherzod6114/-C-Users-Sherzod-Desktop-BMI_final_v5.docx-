# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs("charts", exist_ok=True)
plt.rcParams.update({"font.size": 13, "axes.grid": True, "grid.alpha": 0.3})

ACCENT = "#1f6feb"
ACCENT2 = "#2ea043"
WARN = "#e3611c"
RED = "#cf222e"

# 1) Sutkalik yuklama grafigi
hours = list(range(24))
# kt=0.75, Pmax=12, Por=9.05 ga mos tipik profil
load = [7.2,6.8,6.5,6.3,6.4,6.9,7.8,8.9,9.6,10.1,10.4,10.2,
        9.8,9.6,9.7,10.0,10.6,11.4,12.0,11.7,10.8,9.7,8.6,7.7]
fig, ax = plt.subplots(figsize=(8,4.2))
ax.plot(hours, load, marker="o", color=ACCENT, lw=2.2)
ax.fill_between(hours, load, alpha=0.12, color=ACCENT)
ax.axhline(9.05, color=WARN, ls="--", lw=1.8, label="O'rtacha P = 9,05 MVt")
ax.axhline(12.0, color=RED, ls=":", lw=1.8, label="Maksimal P = 12,0 MVt")
ax.set_xlabel("Soat"); ax.set_ylabel("Aktiv quvvat, MVt")
ax.set_title("Sutkalik yuklama grafigi (10 kV shinalar)")
ax.set_xticks(range(0,24,2)); ax.legend(); fig.tight_layout()
fig.savefig("charts/01_load.png", dpi=140); plt.close(fig)

# 2) Yo'qotishlar tarkibi (pie)
labels = ["Tr. salt yurish\n219", "Tr. yuklama\n131", "110 kV liniya\n210",
          "10 kV fiderlar\n866", "10/0,4 kV tr.\n334"]
sizes = [219,131,210,866,334]
colors = ["#8957e5","#bc8cff","#1f6feb","#e3611c","#2ea043"]
fig, ax = plt.subplots(figsize=(7,5))
w,_,_ = ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors,
               startangle=90, wedgeprops=dict(width=0.45, edgecolor="white"))
ax.set_title("Yillik texnik yo'qotishlar tarkibi (jami 1760 MVt·s)")
fig.tight_layout(); fig.savefig("charts/02_losses_pie.png", dpi=140); plt.close(fig)

# 3) Fider yo'qotishlari (bar)
fid = ["F-1","F-2","F-3","F-4","F-5","F-6","F-7","F-8"]
dw = [142.8,153.4,99.2,154.0,130.6,64.9,90.9,29.8]
bar_colors = [RED if v>=130 else ACCENT for v in dw]
fig, ax = plt.subplots(figsize=(8,4.2))
bars = ax.bar(fid, dw, color=bar_colors)
ax.set_ylabel("Yillik yo'qotish, MVt·s")
ax.set_title("10 kV fiderlar bo'yicha energiya yo'qotishlari")
for b,v in zip(bars,dw):
    ax.text(b.get_x()+b.get_width()/2, v+2, f"{v:.0f}", ha="center", fontsize=10)
fig.tight_layout(); fig.savefig("charts/03_feeders.png", dpi=140); plt.close(fig)

# 4) Garmonik spektr
orders = ["5","7","11","13","17","19"]
mags = [4.5,5.8,3.6,1.8,2.4,1.2]
fig, ax = plt.subplots(figsize=(8,4.2))
ax.bar(orders, mags, color=ACCENT)
ax.axhline(5.0, color=ACCENT2, ls="--", lw=1.8, label="Tartibli garmonika chegarasi")
ax.set_xlabel("Garmonika tartibi"); ax.set_ylabel("Amplituda, %")
ax.set_title("Kuchlanish garmonik spektri (THD = 8,8 %)")
ax.legend(); fig.tight_layout(); fig.savefig("charts/04_thd.png", dpi=140); plt.close(fig)

# 5) Choralar: tejamkorlik va qaytish muddati
measures = ["Reaktiv\nkomp.","ChOQ","AMI","SCADA"]
saving = [284,180,1200,240]
payback = [3.1,0.9,2.4,4.5]
fig, ax1 = plt.subplots(figsize=(8,4.2))
x = np.arange(len(measures))
ax1.bar(x, saving, color=ACCENT, width=0.55)
ax1.set_ylabel("Tejamkorlik, MVt·s/yil", color=ACCENT)
ax1.set_xticks(x); ax1.set_xticklabels(measures)
ax2 = ax1.twinx()
ax2.plot(x, payback, color=RED, marker="D", lw=2.2)
ax2.set_ylabel("Qaytish muddati, yil", color=RED); ax2.grid(False)
for xi,p in zip(x,payback):
    ax2.text(xi, p+0.1, f"{p} yil", color=RED, ha="center", fontsize=10)
ax1.set_title("Choralar: yillik tejamkorlik va investitsiya qaytishi")
fig.tight_layout(); fig.savefig("charts/05_measures.png", dpi=140); plt.close(fig)

# 6) Kumulyativ pul oqimi (NPV)
years = list(range(9))
cum_nom = [-3003,-1903,-803,297,1397,2497,3597,4697,5797]
cum_npv = [-3003,-2047,-1215,-492,137,684,1160,1574,1934]
fig, ax = plt.subplots(figsize=(8,4.2))
ax.plot(years, cum_nom, marker="o", color=ACCENT, lw=2.2, label="Kumulyativ (nominal)")
ax.plot(years, cum_npv, marker="s", color=ACCENT2, lw=2.2, label="Kumulyativ (NPV, r=15%)")
ax.axhline(0, color="black", lw=1)
ax.axvline(2.7, color=RED, ls="--", lw=1.6, label="Qaytish ≈ 2,7 yil")
ax.set_xlabel("Yil"); ax.set_ylabel("Pul oqimi, mln so'm")
ax.set_title("Choralar majmuasining kumulyativ pul oqimi")
ax.legend(); fig.tight_layout(); fig.savefig("charts/06_cashflow.png", dpi=140); plt.close(fig)

# 7) Choralargacha va keyin (qiyoslash)
cats = ["cos φ","To'liq quvvat\nMVA","Yo'qotish\n%","THD, %"]
before = [0.85,14.12,5.0,8.8]
after  = [0.95,12.63,3.0,4.8]
x = np.arange(len(cats)); w=0.35
fig, ax = plt.subplots(figsize=(8,4.2))
ax.bar(x-w/2, before, w, label="Choralargacha", color=WARN)
ax.bar(x+w/2, after, w, label="Choralardan keyin", color=ACCENT2)
ax.set_xticks(x); ax.set_xticklabels(cats)
ax.set_title("Asosiy ko'rsatkichlar: choralargacha va keyin")
for i,(b,a) in enumerate(zip(before,after)):
    ax.text(i-w/2, b, f"{b}", ha="center", va="bottom", fontsize=9)
    ax.text(i+w/2, a, f"{a}", ha="center", va="bottom", fontsize=9)
ax.legend(); fig.tight_layout(); fig.savefig("charts/07_comparison.png", dpi=140); plt.close(fig)

print("Charts created:", os.listdir("charts"))
