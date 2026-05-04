from datetime import datetime
from zoneinfo import ZoneInfo
import time

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from timezonefinder import TimezoneFinder

_geolocator = Nominatim(user_agent="cosmos_ai_astro_bot_v1")
_tz_finder = TimezoneFinder()


def resolve_city(city_name: str, birth_date: str | None = None) -> dict:
    if not city_name or not city_name.strip():
        raise ValueError("Şehir adı boş olamaz.")
    if not birth_date:
        raise ValueError("Doğum tarihi zorunludur.")

    # Türkçe karakter normalizasyonu + retry mekanizması
    cleaned = city_name.strip()
    
    location = None
    last_error = None
    
    for attempt in range(3):  # 3 kez dene
        try:
            time.sleep(1)  # Nominatim rate limit: 1 istek/saniye
            location = _geolocator.geocode(
                cleaned,
                timeout=15,
                language="en"  # İngilizce sonuç daha tutarlı
            )
            if location is not None:
                break
        except GeocoderTimedOut:
            last_error = "zaman aşımı"
            time.sleep(2)
            continue
        except GeocoderServiceError as e:
            raise RuntimeError(f"Geocoding servisine ulaşılamadı: {e}")

    if location is None:
        raise ValueError(
            f"'{city_name}' bulunamadı. "
            f"Lütfen İngilizce şehir adı deneyin (örn: Istanbul, Turkey)."
        )

    latitude = location.latitude
    longitude = location.longitude

    tz_name = _tz_finder.timezone_at(lat=latitude, lng=longitude)
    if tz_name is None:
        raise ValueError(
            f"'{city_name}' için zaman dilimi belirlenemedi."
        )

    try:
        dt = datetime.strptime(birth_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"birth_date 'YYYY-MM-DD' formatında olmalı, gelen: {birth_date}")

    localized = dt.replace(tzinfo=ZoneInfo(tz_name))
    utc_offset_hours = localized.utcoffset().total_seconds() / 3600.0

    # Kısa isim üret (şehir, ülke)
    raw_address = location.address
    parts = [p.strip() for p in raw_address.split(",")]
    short_name = f"{parts[0]}, {parts[-1]}" if len(parts) > 1 else raw_address

    return {
        "latitude": round(latitude, 6),
        "longitude": round(longitude, 6),
        "utc_offset": utc_offset_hours,
        "timezone": tz_name,
        "resolved_name": short_name,  # "Istanbul, Turkey" gibi temiz
    }