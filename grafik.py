from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Create output directory
output_dir = Path("docs/images")
output_dir.mkdir(parents=True, exist_ok=True)

# 1. Veriyi Yükle
print("📊 Grafikler hazırlanıyor...")
try:
    df = pd.read_csv("data/processed/data_cleaned.csv")
except FileNotFoundError:
    print("HATA: 'data/processed/data_cleaned.csv' bulunamadı!")
    exit()

# --- ÖN İŞLEME VE TEMİZLİK ---
# uçuk verileri temizliyoruz
df = df[(df["price"] > 100000) & (df["price"] < 25000000)]  # 25M üstü istisna
df = df[(df["area"] > 20) & (df["area"] < 400)]  # 400m2 üstü istisna

# Gerekli ek sütunları oluştur
df["toplam_oda"] = df["room"] + df["salon"]
df["m2_fiyat"] = df["price"] / df["area"]

# ---------------------------------------------------------
# 1. GRAFİK: Standart Fiyat Dağılımı
plt.figure(figsize=(10, 6))
sns.histplot(df["price"], kde=True, color="blue")
plt.title("1. İzmir Konut Fiyat Dağılımı (Standart)")
plt.xlabel("Fiyat (TL)")
plt.ylabel("Ev Sayısı")
plt.savefig(output_dir / "Rapor_Grafik_1_FiyatDagilimi.png")
plt.close()
print("✅ 1. Grafik kaydedildi: Fiyat Dağılımı")

# ---------------------------------------------------------
# 2. GRAFİK: Metrekare ve Fiyat İlişkisi (Regresyon Analizi) - GÜNCELLENDİ
plt.figure(figsize=(10, 6))

sns.regplot(
    x="area",
    y="price",
    data=df,
    scatter_kws={"alpha": 0.5, "color": "green"},
    line_kws={"color": "red"},
)
plt.title("2. Metrekare ve Fiyat İlişkisi (Regresyon Analizi)")
plt.xlabel("Metrekare (m²)")
plt.ylabel("Fiyat (TL)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.savefig(output_dir / "Rapor_Grafik_2_M2_Fiyat.png")
plt.close()
print("✅ 2. Grafik kaydedildi: M2 - Fiyat İlişkisi (Regresyon)")

# ---------------------------------------------------------
# 3. GRAFİK: En Pahalı 10 İlçe (Ortalama Fiyat)
plt.figure(figsize=(12, 6))
ilce_fiyatlari = df.groupby("district")["price"].mean().sort_values(ascending=False).head(10)
sns.barplot(
    x=ilce_fiyatlari.index,
    y=ilce_fiyatlari.values,
    palette="viridis",
    hue=ilce_fiyatlari.index,
    legend=False,
)
plt.xticks(rotation=45)
plt.title("3. İzmir'in En Pahalı 10 İlçesi (Ortalama Fiyat)")
plt.ylabel("Ortalama Fiyat (TL)")
plt.tight_layout()
plt.savefig(output_dir / "Rapor_Grafik_3_Ilceler.png")
plt.close()
print("✅ 3. Grafik kaydedildi: İlçe Ortalamaları")

# ---------------------------------------------------------
# 4. GRAFİK: Logaritmik Fiyat Dağılımı
plt.figure(figsize=(10, 6))
sns.histplot(np.log1p(df["price"]), kde=True, color="purple", bins=30)
plt.title("4. Logaritmik Fiyat Dağılımı (Normal Dağılıma Yaklaşım)")
plt.xlabel("Log(Fiyat)")
plt.ylabel("Frekans")
plt.savefig(output_dir / "Rapor_Grafik_4_LogFiyat.png")
plt.close()
print("✅ 4. Grafik kaydedildi: Logaritmik Dağılım")

# ---------------------------------------------------------
# 5. GRAFİK: İlçe Bazlı Kutu Grafiği / Boxplot
plt.figure(figsize=(14, 8))
order = df.groupby("district")["price"].median().sort_values(ascending=False).index
sns.boxplot(
    x="district", y="price", data=df, order=order, palette="viridis", hue="district", legend=False
)
plt.xticks(rotation=45, ha="right")
plt.title("5. İlçelere Göre Fiyat Değişkenliği (Boxplot)")
plt.ylabel("Fiyat (TL)")
plt.tight_layout()
plt.savefig(output_dir / "Rapor_Grafik_5_Boxplot.png")
plt.close()
print("✅ 5. Grafik kaydedildi: İlçe Boxplot")

# ---------------------------------------------------------
# 6. GRAFİK: m² Başına En Değerli İlçeler
plt.figure(figsize=(12, 6))
m2_degerleri = df.groupby("district")["m2_fiyat"].mean().sort_values(ascending=False).head(10)
sns.barplot(
    x=m2_degerleri.index,
    y=m2_degerleri.values,
    palette="magma",
    hue=m2_degerleri.index,
    legend=False,
)
plt.xticks(rotation=45)
plt.title("6. Metrekare Başına En Değerli İlçeler")
plt.ylabel("m² Birim Fiyatı (TL/m²)")
plt.tight_layout()
plt.savefig(output_dir / "Rapor_Grafik_6_M2_Degeri.png")
plt.close()
print("✅ 6. Grafik kaydedildi: m² Değeri")

# ---------------------------------------------------------
# 7. GRAFİK: Korelasyon Isı Haritası (Karmaşıklık Matrisi)
plt.figure(figsize=(10, 8))
numeric_df = df[["price", "area", "age", "toplam_oda", "m2_fiyat"]]
numeric_df.columns = ["Fiyat", "Metrekare", "Bina Yaşı", "Oda Sayısı", "m² Değeri"]

sns.heatmap(
    numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm", linewidths=1, linecolor="white"
)
plt.title("7. Özellikler Arası Korelasyon Matrisi")
plt.tight_layout()
plt.savefig(output_dir / "Rapor_Grafik_7_Korelasyon.png")
plt.close()
print("✅ 7. Grafik kaydedildi: Isı Haritası (Matris)")

print("\n🎉 Tebrikler! 7 adet profesyonel grafik başarıyla oluşturuldu.")
