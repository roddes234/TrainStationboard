import os
import requests
from dotenv import load_dotenv
from crs import get_crs
from config import MAX_TRAINS

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")


def get_departures(station, platform):
    url = f"https://transportapi.com/v3/uk/train/station/{station}/live.json"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "darwin": "true"
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        trains = data.get("departures", {}).get("all", [])

        results = []

        for t in trains:
            p = str(t.get("platform", "")).strip()

            if p == platform:
                results.append({
                    "time": t.get("aimed_departure_time", ""),
                    "expected": t.get("expected_departure_time"),
                    "dest": get_crs(t.get("destination_name", "")),
                    "full_dest": t.get("destination_name", ""),
                    "status": t.get("status", ""),
                    "calling": t.get("calling_at", []),
                    "operator": t.get("operator_name", ""),
                    "reason": t.get("reason", "")
                })

        return results[:MAX_TRAINS]

    except Exception as e:
        print("API error:", e)
        return []
