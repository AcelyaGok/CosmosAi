# tests/test_date_to_jd.py
import sys
import os

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)

from astro_bot.ephemeris_utils import date_to_julian_day


def test(baslik, sonuc, beklenen, tolerans=0.001):
    fark = abs(sonuc - beklenen)
    durum = "✅ GEÇTİ" if fark < tolerans else "❌ KALDI"
    print(f"\n{baslik}")
    print(f"  Beklenen: {beklenen}")
    print(f"  Alınan:   {sonuc}")
    print(f"  Fark:     {fark}")
    print(f"  Sonuç:    {durum}")
    return fark < tolerans


print("=" * 60)
print("date_to_julian_day FONKSİYONU TESTLERİ")
print("=" * 60)

# TEST 1: J2000 referansı
# 1 Ocak 2000, 12:00 = 12.0 ondalık saat
sonuc1 = date_to_julian_day(2000, 1, 1, 12.0)
test_1 = test(
    "TEST 1: J2000 referansı (2000-01-01 12:00 → 2451545.0)",
    sonuc1,
    2451545.0
)

# TEST 2: Gece yarısı
# 1 Ocak 2000, 00:00 = 0.0 ondalık saat
sonuc2 = date_to_julian_day(2000, 1, 1, 0.0)
test_2 = test(
    "TEST 2: Gece yarısı (2000-01-01 00:00 → 2451544.5)",
    sonuc2,
    2451544.5
)

# TEST 3: Test profilimiz (15.06.1995, 14:30)
# 14 saat 30 dakika = 14 + 30/60 = 14.5 ondalık saat
sonuc3 = date_to_julian_day(1995, 6, 15, 14.5)
print(f"\nTEST 3: Test profilimiz (1995-06-15 14:30 → 14.5 ondalık)")
print(f"  Çıktı: {sonuc3}")
print(f"  (Bu sayıyı not edin, T3-T5 testlerinde kullanacağız)")

# TEST 4: Dakika hassasiyeti
# 14:30 = 14.5,  14:00 = 14.0, fark 0.5 saat = 0.5/24 gün
jd_1430 = date_to_julian_day(2000, 1, 1, 14.5)
jd_1400 = date_to_julian_day(2000, 1, 1, 14.0)
fark_dakika = jd_1430 - jd_1400
beklenen_fark = 0.5 / 24  # yarım saat gün cinsinden
print(f"\nTEST 4: Yarım saatlik fark testi")
print(f"  Beklenen fark: {beklenen_fark:.6f}")
print(f"  Alınan fark:   {fark_dakika:.6f}")
test_4 = abs(fark_dakika - beklenen_fark) < 0.0001
print(f"  Sonuç:         {'✅ GEÇTİ' if test_4 else '❌ KALDI'}")

# ÖZET
print("\n" + "=" * 60)
print("ÖZET")
print("=" * 60)
print(f"  Test 1 (J2000):         {'✅' if test_1 else '❌'}")
print(f"  Test 2 (Gece yarısı):   {'✅' if test_2 else '❌'}")
print(f"  Test 4 (Yarım saat):    {'✅' if test_4 else '❌'}")