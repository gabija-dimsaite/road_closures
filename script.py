import requests
import csv

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

# Save CSV
with open("road_closed.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved {len(rows)} rows to road_closed.csv")
