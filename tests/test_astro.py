import json
from astro_bot.astro_calculator import calculate_natal_chart

result = calculate_natal_chart(
    year=1995, month=6, day=15,
    hour=14, minute=30,
    latitude=41.0082,
    longitude=28.9784,
    utc_offset=3.0
)

print(json.dumps(result, ensure_ascii=False, indent=2))