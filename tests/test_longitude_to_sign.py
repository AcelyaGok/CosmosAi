# tests/test_longitude_to_sign.py
import sys
import os

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)

from astro_bot.ephemeris_utils import longitude_to_sign


def test(baslik, sonuc, beklenen_burc, beklenen_derece=None, derece_tolerans=0.1):
    """Burç doğru mu, derece doğru mu kontrol et."""
    burc_ok = sonuc["sign"] == beklenen_burc
    derece_ok = True
    if beklenen_derece is not None:
        derece_ok = abs(sonuc["degree"] - beklenen_derece) < derece_tolerans

    durum = "✅ GEÇTİ" if (burc_ok and derece_ok) else "❌ KALDI"
    print(f"\n{baslik}")
    print(f"  Çıktı:    {sonuc}")
    print(f"  Beklenen burç: {beklenen_burc}", end="")
    if beklenen_derece is not None:
        print(f", derece: ~{beklenen_derece}")
    else:
        print()
    print(f"  Sonuç:    {durum}")
    return burc_ok and derece_ok


print("=" * 60)
print("longitude_to_sign FONKSİYONU TESTLERİ")
print("=" * 60)

# -----------------------------------------------------------
# A. Net değerler — her burcun ortasından
# -----------------------------------------------------------
print("\n--- A grubu: Net değerler ---")

t1 = test("A1: 15° → Koç (ortası)",     longitude_to_sign(15),     "Koç",     15)
t2 = test("A2: 45° → Boğa (ortası)",    longitude_to_sign(45),     "Boğa",    15)
t3 = test("A3: 75° → İkizler (ortası)", longitude_to_sign(75),     "İkizler", 15)
t4 = test("A4: 195° → Terazi",          longitude_to_sign(195),    "Terazi",  15)
t5 = test("A5: 285° → Oğlak",           longitude_to_sign(285),    "Oğlak",   15)
t6 = test("A6: 345° → Balık",           longitude_to_sign(345),    "Balık",   15)

# -----------------------------------------------------------
# B. Sınır değerler — en sık hata burada
# -----------------------------------------------------------
print("\n--- B grubu: Sınır değerleri ---")

# 0° → Koç'un başlangıcı
t7 = test("B1: 0° → Koç (başlangıç)", longitude_to_sign(0), "Koç", 0)

# 29.99° → hâlâ Koç
t8 = test("B2: 29.99° → Koç", longitude_to_sign(29.99), "Koç", 29.99)

# 30° → Boğa'nın başlangıcı (sınır kontrolü)
t9 = test("B3: 30° → Boğa (sınır)", longitude_to_sign(30), "Boğa", 0)

# 359.99° → Balık'ın sonu
t10 = test("B4: 359.99° → Balık", longitude_to_sign(359.99), "Balık", 29.99)

# -----------------------------------------------------------
# C. Edge case'ler — kod çökecek mi?
# -----------------------------------------------------------
print("\n--- C grubu: Edge case'ler (kod çökerse hata gösterir) ---")

print("\nC1: 360° (tam Koç'a dönmeli) ile çağırma...")
try:
    sonuc = longitude_to_sign(360)
    print(f"  Çıktı: {sonuc}")
    if sonuc["sign"] == "Koç":
        print("  Sonuç: ✅ GEÇTİ (modulo doğru çalışıyor)")
        t11 = True
    else:
        print(f"  Sonuç: ❌ KALDI (Koç beklendi)")
        t11 = False
except IndexError as e:
    print(f"  💥 IndexError fırlattı: {e}")
    print("  Sonuç: ❌ KALDI (modulo yapılmıyor)")
    t11 = False
except Exception as e:
    print(f"  💥 Hata: {type(e).__name__}: {e}")
    t11 = False

# -----------------------------------------------------------
# D. Bizim test profilimizin Güneş'i (yaklaşık 84°)
# 15 Haziran → İkizler → 84° civarı
# -----------------------------------------------------------
print("\n--- D grubu: Test profilimiz (15.06.1995) ---")
t12 = test("D1: 84° → İkizler (test profilimizdeki Güneş)", longitude_to_sign(84), "İkizler", 24)

# -----------------------------------------------------------
# ÖZET
# -----------------------------------------------------------
print("\n" + "=" * 60)
print("ÖZET")
print("=" * 60)
testler = [
    ("A1 (15° Koç)",      t1),
    ("A2 (45° Boğa)",     t2),
    ("A3 (75° İkizler)",  t3),
    ("A4 (195° Terazi)",  t4),
    ("A5 (285° Oğlak)",   t5),
    ("A6 (345° Balık)",   t6),
    ("B1 (0° sınır)",     t7),
    ("B2 (29.99° sınır)", t8),
    ("B3 (30° sınır)",    t9),
    ("B4 (359.99° sınır)",t10),
    ("C1 (360° edge)",    t11),
    ("D1 (84° gerçek)",   t12),
]
for ad, sonuc in testler:
    print(f"  {ad:<25} {'✅' if sonuc else '❌'}") 
    #Düzenli yazmayı sağlar

# tests/test_longitude_to_sign.py
import sys
import os

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)

from astro_bot.ephemeris_utils import longitude_to_sign


def test(baslik, sonuc, beklenen_burc, beklenen_derece=None, derece_tolerans=0.1):
    """Burç doğru mu, derece doğru mu kontrol et."""
    burc_ok = sonuc["sign"] == beklenen_burc
    derece_ok = True
    if beklenen_derece is not None:
        derece_ok = abs(sonuc["degree"] - beklenen_derece) < derece_tolerans

    durum = "✅ GEÇTİ" if (burc_ok and derece_ok) else "❌ KALDI"
    print(f"\n{baslik}")
    print(f"  Çıktı:    {sonuc}")
    print(f"  Beklenen burç: {beklenen_burc}", end="")
    if beklenen_derece is not None:
        print(f", derece: ~{beklenen_derece}")
    else:
        print()
    print(f"  Sonuç:    {durum}")
    return burc_ok and derece_ok


print("=" * 60)
print("longitude_to_sign FONKSİYONU TESTLERİ")
print("=" * 60)

# -----------------------------------------------------------
# A. Net değerler — her burcun ortasından
# -----------------------------------------------------------
print("\n--- A grubu: Net değerler ---")

t1 = test("A1: 15° → Koç (ortası)",     longitude_to_sign(15),     "Koç",     15)
t2 = test("A2: 45° → Boğa (ortası)",    longitude_to_sign(45),     "Boğa",    15)
t3 = test("A3: 75° → İkizler (ortası)", longitude_to_sign(75),     "İkizler", 15)
t4 = test("A4: 195° → Terazi",          longitude_to_sign(195),    "Terazi",  15)
t5 = test("A5: 285° → Oğlak",           longitude_to_sign(285),    "Oğlak",   15)
t6 = test("A6: 345° → Balık",           longitude_to_sign(345),    "Balık",   15)

# -----------------------------------------------------------
# B. Sınır değerler — en sık hata burada
# -----------------------------------------------------------
print("\n--- B grubu: Sınır değerleri ---")

# 0° → Koç'un başlangıcı
t7 = test("B1: 0° → Koç (başlangıç)", longitude_to_sign(0), "Koç", 0)

# 29.99° → hâlâ Koç
t8 = test("B2: 29.99° → Koç", longitude_to_sign(29.99), "Koç", 29.99)

# 30° → Boğa'nın başlangıcı (sınır kontrolü)
t9 = test("B3: 30° → Boğa (sınır)", longitude_to_sign(30), "Boğa", 0)

# 359.99° → Balık'ın sonu
t10 = test("B4: 359.99° → Balık", longitude_to_sign(359.99), "Balık", 29.99)

# -----------------------------------------------------------
# C. Edge case'ler — kod çökecek mi?
# -----------------------------------------------------------
print("\n--- C grubu: Edge case'ler (kod çökerse hata gösterir) ---")

print("\nC1: 360° (tam Koç'a dönmeli) ile çağırma...")
try:
    sonuc = longitude_to_sign(360)
    print(f"  Çıktı: {sonuc}")
    if sonuc["sign"] == "Koç":
        print("  Sonuç: ✅ GEÇTİ (modulo doğru çalışıyor)")
        t11 = True
    else:
        print(f"  Sonuç: ❌ KALDI (Koç beklendi)")
        t11 = False
except IndexError as e:
    print(f"  💥 IndexError fırlattı: {e}")
    print("  Sonuç: ❌ KALDI (modulo yapılmıyor)")
    t11 = False
except Exception as e:
    print(f"  💥 Hata: {type(e).__name__}: {e}")
    t11 = False

# -----------------------------------------------------------
# D. Bizim test profilimizin Güneş'i (yaklaşık 84°)
# 15 Haziran → İkizler → 84° civarı
# -----------------------------------------------------------
print("\n--- D grubu: Test profilimiz (15.06.1995) ---")
t12 = test("D1: 84° → İkizler (test profilimizdeki Güneş)", longitude_to_sign(84), "İkizler", 24)

# -----------------------------------------------------------
# ÖZET
# -----------------------------------------------------------
print("\n" + "=" * 60)
print("ÖZET")
print("=" * 60)
testler = [
    ("A1 (15° Koç)",      t1),
    ("A2 (45° Boğa)",     t2),
    ("A3 (75° İkizler)",  t3),
    ("A4 (195° Terazi)",  t4),
    ("A5 (285° Oğlak)",   t5),
    ("A6 (345° Balık)",   t6),
    ("B1 (0° sınır)",     t7),
    ("B2 (29.99° sınır)", t8),
    ("B3 (30° sınır)",    t9),
    ("B4 (359.99° sınır)",t10),
    ("C1 (360° edge)",    t11),
    ("D1 (84° gerçek)",   t12),
]
for ad, sonuc in testler:
    print(f"  {ad:<25} {'✅' if sonuc else '❌'}")

gecen = 0
for ad, sonuc in testler:
    if sonuc:
        gecen += 1
print(f"\n  Toplam: {gecen}/{len(testler)} test geçti")