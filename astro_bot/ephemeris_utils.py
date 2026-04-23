# ephemeris_utils.py

import swisseph as swe 

def date_to_julian_day(year: int, month: int, day: int, hour: float = 0.0) -> float: 
    #Girilen tarihi Julian gününe çevirir. Saat ondalık olarak verilir.
    jd = swe.julday(year, month, day, hour)
    return jd


def longitude_to_sign(longitude: float) -> dict:
    #Girilen uzunluğun hangi burca ait olduğunu derece aralıklarıyla anlarız.
    #Dict kullandığımız için JSON formatında döndürmeyi kolaylaştırıyoruz. 

    signs = [
        "Koç", "Boğa", "İkizler", "Yengeç",
        "Aslan", "Başak", "Terazi", "Akrep",
        "Yay", "Oğlak", "Kova", "Balık"
    ]
    sign_index = int(longitude // 30)
    degree_in_sign = longitude % 30 #Verdiği kalan sayesinde burcun hang derecede olduğunu anlarız.
    return {
        "sign": signs[sign_index],
        "degree": round(degree_in_sign, 2)
        #JSON formatına geçişi kolaylaştırdığı için dict kullanıyoruz. Burada dereceyi de ekleyerek burcun hangi derecesinde olduğunu göstermek istiyoruz.
    }


def local_time_to_utc(hour: int, minute: int, utc_offset: float) -> float:
   #Yerel saati direkt kullanamayız. UTC'ye çevirmemiz gerekir. Bu fonksiyon, yerel saati UTC'ye çevirir. 
   #Saat ve dakika ayrı ayrı verilir, UTC offset'i ise saat cinsindendir.

    decimal_hour = hour + minute / 60.0
    utc_hour = decimal_hour - utc_offset 
    #Türkiye'de genellikle UTC+3 kullanılır. Bu yüzden yerel saat - 3 yapılır.
    return utc_hour