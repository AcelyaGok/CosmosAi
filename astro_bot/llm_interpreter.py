from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_turkish_interpretation(astro_data: dict) -> str:
    prompt = f"""
Sen eğlenceli, samimi ve biraz da esprili bir astroloji uzmanısın. 
Yorumlarını sanki arkadaşınla sohbet ediyormuş gibi yaz — doğal, akıcı ve insani.

Kişilik:
- Espirili ve şakacı ama saçmalama
- Aşk ve ilişki konularında duygusal ve anlayışlı ol
- Kariyer ve para konularında pratik ve mantıklı ol
- Bazen hafif uyarılar ver ama hep pozitif bitir
- SADECE TÜRKÇE yaz, başka hiçbir dil kullanma

Yapman gerekenler:
- Yükselen burca göre kişiliği anlat
- Güneş burcuna göre genel enerjisini yorumla  
- Ay burcuna göre duygusal dünyasını açıkla
- Retrograde gezegenleri varsa hafifçe değin ("dikkatli ol ama panik yapma" tarzında)
- 5-6 cümle, samimi bir dille yaz

ASTRO_JSON:
{json.dumps(astro_data, ensure_ascii=False)}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Sen Türkçe konuşan, eğlenceli ve samimi bir astroloji uzmanısın. Asla başka dil kullanma, sadece Türkçe yaz."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":

    astro_data = {
        "birth_info": {
            "date": "1995-06-15",
            "time": "14:30",
            "latitude": 41.0082,
            "longitude": 28.9784,
            "utc_offset": 3.0
        },
        "ascendant": "Terazi",
        "asc_degree": 11.67,
        "planets": {
            "sun": {"sign": "İkizler", "degree": 23.91, "retrograde": False},
            "moon": {"sign": "Oğlak", "degree": 26.69, "retrograde": False},
            "mercury": {"sign": "İkizler", "degree": 9.93, "retrograde": True},
            "venus": {"sign": "İkizler", "degree": 5.84, "retrograde": False},
            "mars": {"sign": "Başak", "degree": 10.09, "retrograde": False},
            "jupiter": {"sign": "Yay", "degree": 8.77, "retrograde": True},
            "saturn": {"sign": "Balık", "degree": 24.39, "retrograde": False},
            "uranus": {"sign": "Oğlak", "degree": 29.82, "retrograde": True},
            "neptune": {"sign": "Oğlak", "degree": 24.97, "retrograde": True},
            "pluto": {"sign": "Akrep", "degree": 28.55, "retrograde": True}
        }
    }

    print("Groq bağlantısı test ediliyor...\n")
    try:
        yorum = get_turkish_interpretation(astro_data)
        print("✅ Bağlantı başarılı! Gelen yorum:\n")
        print(yorum)
    except Exception as e:
        print(f"❌ Hata: {e}")