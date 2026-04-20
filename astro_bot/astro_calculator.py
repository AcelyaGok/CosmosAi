# astro_calculator.py

import swisseph as swe
from ephemeris_utils import date_to_julian_day, longitude_to_sign, local_time_to_utc

swe.set_ephe_path(None)
#Gezegen verilerini kütüphanenin kendi varsayılan yolunu kullanır.

PLANETS = {
    "sun":     swe.SUN, #swiss ephemeris'te gezegenler için tanımlanmış sabitler kullanılır. Bu sayede hangi gezegenin hangi ID'ye sahip olduğunu bilmemiz gerekmez. Örneğin swe.SUN=0, swe.MOON=1 gibi.
    "moon":    swe.MOON,
    "mercury": swe.MERCURY,
    "venus":   swe.VENUS,
    "mars":    swe.MARS,
    "jupiter": swe.JUPITER,
    "saturn":  swe.SATURN,
    "uranus":  swe.URANUS,
    "neptune": swe.NEPTUNE,
    "pluto":   swe.PLUTO,
}


def get_planet_position(jd: float, planet_id: int) -> dict: #Gezegen konumunu hesaplar. 
    result, _ = swe.calc_ut(jd, planet_id) #Bu paket enlem, boylam, hız gibi bilgileri içerir. 
    longitude = result[0] #Gezegenin ekliptik boylamını alırız.
    speed = result[3] #Gezegenin hızını alırız. <0 ise retrodadır. 
    sign_info = longitude_to_sign(longitude)
    return {
        "longitude": round(longitude, 4),
        "sign": sign_info["sign"],
        "degree": sign_info["degree"],
        "retrograde": speed < 0
    }


def get_ascendant(jd: float, latitude: float, longitude: float) -> dict: #Enlem boylam sayesinde yükselen hesaplanır.
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P') #b'P' parametresi Placidus ev sistemini kullanır. cusps evlerin başlangıç noktalarını, ascmc ise yükselen ve orta nokta gibi bilgileri içerir.
    asc_longitude = ascmc[0] #Yükselen
    mc_longitude  = ascmc[1] #En yüksek nokta (MC)
    asc_sign = longitude_to_sign(asc_longitude)
    mc_sign  = longitude_to_sign(mc_longitude)
    return {
        "ascendant": asc_sign["sign"],
        "asc_degree": asc_sign["degree"],
        "mc": mc_sign["sign"],
        "mc_degree": mc_sign["degree"],
        "houses": [round(c, 2) for c in cusps]
    }


def calculate_natal_chart(year: int, month: int, day: int,
                           hour: int, minute: int,
                           latitude: float, longitude: float,
                           utc_offset: float = 3.0) -> dict:
    utc_hour = local_time_to_utc(hour, minute, utc_offset)
    jd = date_to_julian_day(year, month, day, utc_hour)
    #Önce yerel saat çevrilir sonra Julian Day çevirmesi yapılır.

    planets_data = {}
    for planet_name, planet_id in PLANETS.items():
        planets_data[planet_name] = get_planet_position(jd, planet_id)
        #Gezegenlerin konumları hesaplanır ve bir sözlükte saklanır. Bu sayede JSON formatında kolayca döndürülebilirler.

    asc_data = get_ascendant(jd, latitude, longitude)

    return {
        "birth_info": {
            "date": f"{year}-{month:02d}-{day:02d}",
            "time": f"{hour:02d}:{minute:02d}",
            "latitude": latitude,
            "longitude": longitude,
            "utc_offset": utc_offset
        },
        "ascendant": asc_data["ascendant"],
        "asc_degree": asc_data["asc_degree"],
        "mc": asc_data["mc"],
        "mc_degree": asc_data["mc_degree"],
        "houses": asc_data["houses"],
        "planets": planets_data
    }
#JSON verisi burdan gider.