import csv

CRS_MAP = {}

def load_crs():
    global CRS_MAP
    with open("stations_full.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name") or row.get("Station Name")
            code = row.get("crs") or row.get("CRS Code")

            if name and code:
                CRS_MAP[name.strip()] = code.strip()


def get_crs(name):
    return CRS_MAP.get(name, name[:3].upper())
