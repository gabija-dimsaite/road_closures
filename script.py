import requests
import json
from datetime import datetime

url = "http://restrictions.eismoinfo.lt"
data = requests.get(url).json()

rows = []

for item in data:
    for r in item.get("restrictions", []):
        if r.get("restrictionType") == "roadClosed":

            location = item.get("location", {})

            row = {
                "start_time": (item.get("startTime") or "")[:10],
                "end_time": (item.get("endTime") or "")[:10],
                "description": item.get("description"),
                "location": location.get("polyline"),
                "direction": location.get("direction"),
                "street": location.get("street"),
                "location_description": location.get("location_description"),
                "restrictionType": r.get("restrictionType"),
                "transportType": r.get("transportType"),
            }

            rows.append(row)

# Save to file
with open("road_closed.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2, ensure_ascii=False)

print(f"Saved {len(rows)} records")
