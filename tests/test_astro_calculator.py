# tests/test_astro_calculator.py
import sys
import os
import json

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)

from astro_bot.astro_calculator import (
    get_ascendant,
    get_planet_position,
    calculate_natal_chart,
    PLANETS,
)
from astro_bot.ephemeris_utils import date_to_julian_day, local_time_to_utc

# Test profilimiz: 15 Haziran 1995, 14:30 İstanbul (UTC+3)
LAT = 41.0082
LON = 28.9784
TZ = 3.0


# =============================================================
# T3: get_ascendant testleri
# =============================================================
print("=" * 60)
print("T3: get_ascendant TESTLERİ")
print("=" * 60)

# Test profilimiz için JD hesapla (UTC dönüşümü yaparak)
utc_hour = local_time_to_utc(14, 30, TZ)  # 14:30 İstanbul → 11.5 UTC
jd_test = date_to_julian_day(1995, 6, 15, utc_hour)
print(f"\nKullanılan JD: {jd_test} (1995-06-15 11:30 UTC)")

# T3.1 — Test profilimiz için ASC
asc1 = get_ascendant(jd_test, LAT, LON)
print(f"\nT3.1: Test profilimiz (1995-06-15 14:30 İstanbul)")
print(f"  Çıktı: {asc1}")
print(f"  Bu sonucu astro.com ile karşılaştırmamız lazım.")

# T3.2 — Mantık testi: Sabah ve akşam ASC farklı olmalı
print(f"\nT3.2: Aynı gün, sabah vs akşam ASC değişmeli mi?")
jd_morning = date_to_julian_day(1995, 6, 15, local_time_to_utc(6, 0, TZ))
jd_evening = date_to_julian_day(1995, 6, 15, local_time_to_utc(20, 0, TZ))
asc_morning = get_ascendant(jd_morning, LAT, LON)
asc_evening = get_ascendant(jd_evening, LAT, LON)
print(f"  Sabah 06:00 → ASC: {asc_morning['ascendant']} {asc_morning['asc_degree']}°")
print(f"  Akşam 20:00 → ASC: {asc_evening['ascendant']} {asc_evening['asc_degree']}°")
ayni_mi = (asc_morning['ascendant'] == asc_evening['ascendant'] and
           abs(asc_morning['asc_degree'] - asc_evening['asc_degree']) < 1)
t3_2 = not ayni_mi
print(f"  Sonuç: {'✅ GEÇTİ (farklılar, doğru)' if t3_2 else '❌ KALDI (aynı çıkıyor, hesap yanlış)'}")

# T3.3 — Mantık testi: Aynı an, farklı şehir ASC farklı olmalı
print(f"\nT3.3: Aynı an, İstanbul vs Tokyo ASC değişmeli mi?")
asc_istanbul = get_ascendant(jd_test, 41.0082, 28.9784)  # İstanbul
asc_tokyo = get_ascendant(jd_test, 35.6762, 139.6503)    # Tokyo
print(f"  İstanbul → ASC: {asc_istanbul['ascendant']} {asc_istanbul['asc_degree']}°")
print(f"  Tokyo    → ASC: {asc_tokyo['ascendant']} {asc_tokyo['asc_degree']}°")
t3_3 = (asc_istanbul['ascendant'] != asc_tokyo['ascendant'] or
        abs(asc_istanbul['asc_degree'] - asc_tokyo['asc_degree']) > 1)
print(f"  Sonuç: {'✅ GEÇTİ' if t3_3 else '❌ KALDI'}")

# T3.4 — Yapı kontrolü: dönen dict'in alanları doğru mu?
print(f"\nT3.4: Dönen dict yapısı kontrolü")
beklenen_alanlar = {"ascendant", "asc_degree", "mc", "mc_degree", "houses"}
mevcut_alanlar = set(asc1.keys())
t3_4 = beklenen_alanlar == mevcut_alanlar
print(f"  Beklenen: {sorted(beklenen_alanlar)}")
print(f"  Mevcut:   {sorted(mevcut_alanlar)}")
print(f"  Houses uzunluğu: {len(asc1['houses'])} (12 olmalı)")
t3_4 = t3_4 and len(asc1['houses']) == 12
print(f"  Sonuç: {'✅ GEÇTİ' if t3_4 else '❌ KALDI'}")


# =============================================================
# T4: get_planet_position testleri
# =============================================================
print("\n" + "=" * 60)
print("T4: get_planet_position TESTLERİ")
print("=" * 60)

# T4.1 — Test profilimiz için Güneş İkizler'de mi?
sun_pos = get_planet_position(jd_test, PLANETS["sun"])
print(f"\nT4.1: 15 Haziran → Güneş İkizler'de olmalı")
print(f"  Çıktı: {sun_pos}")
t4_1 = sun_pos["sign"] == "İkizler"
print(f"  Sonuç: {'✅ GEÇTİ' if t4_1 else '❌ KALDI'}")

# T4.2 — Yapı kontrolü
print(f"\nT4.2: Dönen dict yapısı kontrolü")
beklenen_alanlar = {"longitude", "sign", "degree", "retrograde"}
mevcut_alanlar = set(sun_pos.keys())
t4_2 = beklenen_alanlar == mevcut_alanlar
print(f"  Beklenen: {sorted(beklenen_alanlar)}")
print(f"  Mevcut:   {sorted(mevcut_alanlar)}")
print(f"  Sonuç: {'✅ GEÇTİ' if t4_2 else '❌ KALDI'}")

# T4.3 — Retro tipinin bool olduğu kontrol
print(f"\nT4.3: retrograde alanı bool mu?")
t4_3 = isinstance(sun_pos["retrograde"], bool)
print(f"  Tip: {type(sun_pos['retrograde']).__name__}")
print(f"  Sonuç: {'✅ GEÇTİ' if t4_3 else '❌ KALDI'}")

# T4.4 — Tüm gezegenler hesaplanabiliyor mu (çökmüyorlar mı)?
print(f"\nT4.4: Tüm 10 gezegen için konum hesaplanabiliyor")
basarili = []
hatali = []
for name, pid in PLANETS.items():
    try:
        pos = get_planet_position(jd_test, pid)
        basarili.append(name)
    except Exception as e:
        hatali.append((name, str(e)))
print(f"  Başarılı: {len(basarili)}/10 → {basarili}")
if hatali:
    print(f"  ❌ Hatalı: {hatali}")
t4_4 = len(basarili) == 10
print(f"  Sonuç: {'✅ GEÇTİ' if t4_4 else '❌ KALDI'}")


# =============================================================
# T5: calculate_natal_chart entegre test
# =============================================================
print("\n" + "=" * 60)
print("T5: calculate_natal_chart ENTEGRE TEST")
print("=" * 60)

chart = calculate_natal_chart(1995, 6, 15, 14, 30, LAT, LON, utc_offset=3.0)

print(f"\nT5.1: Tam JSON çıktısı")
print(json.dumps(chart, indent=2, ensure_ascii=False))

# T5.2 — Üst seviye anahtarlar doğru mu?
print(f"\nT5.2: Üst seviye anahtarlar")
beklenen = {"birth_info", "ascendant", "asc_degree", "mc", "mc_degree", "houses", "planets"}
mevcut = set(chart.keys())
t5_2 = beklenen == mevcut
print(f"  Beklenen: {sorted(beklenen)}")
print(f"  Mevcut:   {sorted(mevcut)}")
print(f"  Sonuç: {'✅ GEÇTİ' if t5_2 else '❌ KALDI'}")

# T5.3 — Tüm 10 gezegen var mı?
print(f"\nT5.3: planets içinde 10 gezegen var mı?")
gezegen_sayisi = len(chart["planets"])
print(f"  Gezegen sayısı: {gezegen_sayisi}")
t5_3 = gezegen_sayisi == 10
print(f"  Sonuç: {'✅ GEÇTİ' if t5_3 else '❌ KALDI'}")

# T5.4 — Astroloji açısından makul mu? (15 Haziran → İkizler bekleniyor)
print(f"\nT5.4: 15 Haziran doğumlu birinin Güneş'i İkizler olmalı")
gunes_burcu = chart["planets"]["sun"]["sign"]
print(f"  Güneş burcu: {gunes_burcu}")
t5_4 = gunes_burcu == "İkizler"
print(f"  Sonuç: {'✅ GEÇTİ' if t5_4 else '❌ KALDI'}")


# =============================================================
# ÖZET
# =============================================================
print("\n" + "=" * 60)
print("GENEL ÖZET")
print("=" * 60)
testler = [
    ("T3.1 (ASC çalışıyor)",          True),  # Çıktıyı manuel doğrulayacağız
    ("T3.2 (sabah/akşam farkı)",       t3_2),
    ("T3.3 (İstanbul/Tokyo farkı)",    t3_3),
    ("T3.4 (ASC dict yapısı)",         t3_4),
    ("T4.1 (Güneş İkizler)",           t4_1),
    ("T4.2 (planet dict yapısı)",      t4_2),
    ("T4.3 (retrograde bool)",         t4_3),
    ("T4.4 (10 gezegen çalışıyor)",    t4_4),
    ("T5.2 (chart anahtarları)",       t5_2),
    ("T5.3 (10 gezegen chart'ta)",     t5_3),
    ("T5.4 (Güneş İkizler chart)",     t5_4),
]
gecen = 0
for ad, sonuc in testler:
    print(f"  {ad:<35} {'✅' if sonuc else '❌'}")
    if sonuc:
        gecen += 1
print(f"\n  Toplam: {gecen}/{len(testler)} test geçti")
print("\n  ⚠️ T3.1'i manuel doğrulamak gerek: ASC değerini astro.com'la karşılaştırın")