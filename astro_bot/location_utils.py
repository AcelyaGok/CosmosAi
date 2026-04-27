# Şehir adını Swiss Ephemeris'in istediği koordinat + UTC offset formatına çevirir.

from datetime import datetime
from zoneinfo import ZoneInfo

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from timezonefinder import TimezoneFinder

_geolocator = Nominatim(user_agent="cosmos_ai_astro_bot")
_tz_finder = TimezoneFinder()


def resolve_city(city_name: str, birth_date: str | None = None) -> dict:
    """
    Şehir adını enlem/boylam ve UTC offset bilgisine çevirir. 
    Yaz saati uygulaması gibi sebepler UTC değişimine sebep olabilir. 

    """

    if not city_name or not city_name.strip():
        raise ValueError("Şehir adı boş olamaz.")
    if not birth_date:
        raise ValueError("Doğum tarihi zorunludur.")

    # Adım: Şehir adına göre enlem boylam belirlemesi yapılır. 
    try:
        location = _geolocator.geocode(city_name.strip(), timeout=10)
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        raise RuntimeError(f"Geocoding servisine ulaşılamadı: {e}")

    if location is None:
        raise ValueError(f"'{city_name}' için konum bulunamadı. Lütfen geçerli bir şehir ismi girin.")

    latitude = location.latitude
    longitude = location.longitude

    # Koordinat IANA timezone ile bölge adı belirlenerek alan kısıtlanır. (örn. "Europe/Istanbul")
    tz_name = _tz_finder.timezone_at(lat=latitude, lng=longitude)
    if tz_name is None:
        raise ValueError(
            f"'{city_name}' için zaman dilimi belirlenemedi (koordinat: {latitude}, {longitude})."
        )

    # Timezone + tarih → UTC offset (saat cinsinden float)
    # Yaz saati yüzünden offset yıllara göre değişir, bu yüzden doğum tarihi lazım.
    try:
            dt = datetime.strptime(birth_date, "%Y-%m-%d")
    except ValueError:
            raise ValueError(f"birth_date 'YYYY-MM-DD' formatında olmalı, gelen: {birth_date}")


    localized = dt.replace(tzinfo=ZoneInfo(tz_name))
    utc_offset_hours = localized.utcoffset().total_seconds() / 3600.0

    return {
        "latitude": round(latitude, 6),
        "longitude": round(longitude, 6),
        "utc_offset": utc_offset_hours,
        "timezone": tz_name,
        "resolved_name": location.address,
    }


if __name__ == "__main__":
    # Hızlı test — bu modül doğrudan çalıştırıldığında çalışır
    test_cases = [
    #Test verileri 
        ("İstanbul", "1995-06-15"),
        ("Ankara", "2000-01-01"),
        ("New York", "1990-12-25"),

    #Türkiye'de yaz saati uygulması 2016'da kaldırıldı. Öncesi ve sonrası test verileri. 
        ("İstanbul", "2015-03-28"),
        ("İstanbul", "2016-09-08"),

    #Hatalı girdiler
     ("", "2000-01-01"),               
    ("Xyzabc123", "2000-01-01"),      
    ("İstanbul", "tarih-degil"),      
    ("İstanbul", "1995-13-45"),       
    ]

    for city, date in test_cases:
        print(f"\n--- {city} ({date}) ---")
        try:
            result = resolve_city(city, date)
            for key, value in result.items():
                print(f"  {key}: {value}")
        except (ValueError, RuntimeError) as e:
            print(f"  HATA: {e}")