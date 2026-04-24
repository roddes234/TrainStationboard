from PIL import Image

TOC_MAP = {
    "LNER": "logos/lner.bmp",
    "Northern": "logos/northern.bmp",
    "TransPennine Express": "logos/tpexpress.bmp"
}

def get_logo(operator):
    path = TOC_MAP.get(operator)
    if path:
        try:
            return Image.open(path)
        except:
            return None
    return None
