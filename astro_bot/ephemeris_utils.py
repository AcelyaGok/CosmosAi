# ephemeris_utils.py

import swisseph as swe

def date_to_julian_day(year: int, month: int, day: int, hour: float = 0.0) -> float:
    """
    Tarihi Julian Day formatına çevirir.
    Swiss Ephemeris tüm hesaplamalarını JD üzerinden yapar.
    hour: UTC cinsinden ondalıklı saat (örn. 14.5 = 14:30)
    """
    jd = swe.julday(year, month, day, hour)
    return jd


def longitude_to_sign(longitude: float) -> dict:
    """
    0-360 derece arasındaki boylam değerini
    burç adına ve o burç içindeki dereceye çevirir.
    """
    signs = [
        "Koç", "Boğa", "İkizler", "Yengeç",
        "Aslan", "Başak", "Terazi", "Akrep",
        "Yay", "Oğlak", "Kova", "Balık"
    ]
    sign_index = int(longitude // 30)
    degree_in_sign = longitude % 30
    return {
        "sign": signs[sign_index],
        "degree": round(degree_in_sign, 2)
    }


def local_time_to_utc(hour: int, minute: int, utc_offset: float) -> float:
    """
    Yerel saati UTC'ye çevirir.
    utc_offset: Türkiye için +3.0
    Döndürür: ondalıklı saat (float), örn. 14.5 = 14:30
    """
    decimal_hour = hour + minute / 60.0
    utc_hour = decimal_hour - utc_offset
    return utc_hour