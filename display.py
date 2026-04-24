from PIL import Image, ImageDraw, ImageFont
from toc import get_logo
from datetime import datetime

WIDTH = 250
HEIGHT = 122


def minutes_to_departure(timestr):
    try:
        now = datetime.now()
        dep = datetime.strptime(timestr, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )

        diff = int((dep - now).total_seconds() / 60)

        if diff <= 0:
            return "DUE"
        elif diff == 1:
            return "1M"
        elif diff < 60:
            return f"{diff}M"
        else:
            return timestr
    except:
        return timestr


def format_status(t):
    if "cancel" in t["status"].lower():
        return "CANC"

    if t["expected"] and t["expected"] != t["time"]:
        return minutes_to_departure(t["expected"])

    return minutes_to_departure(t["time"])


def format_calling(stops):
    if not stops:
        return ""

    if len(stops) <= 4:
        return "Calling at " + ", ".join(stops)

    return "Calling at " + ", ".join(stops[:3]) + " then " + stops[-1]


def draw_board(epd, trains, station, platform):
    image = Image.new('1', (HEIGHT, WIDTH), 0)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 13
    )

    y = 0

    # Header
    draw.text((0, y), f"{station}  P{platform}", font=font, fill=255)

    if trains:
        logo = get_logo(trains[0]["operator"])
        if logo:
            image.paste(logo.resize((40, 20)), (200, 0))

    y += 18

    draw.text((0, y), "TIME  DEST  ST", font=font, fill=255)
    y += 14

    draw.line((0, y, 250, y), fill=255)
    y += 4

    for t in trains:
        status = format_status(t)
        line = f"{t['time']} {t['dest']:<4} {status:<4}"

        if status not in ["ON T"]:
            draw.rectangle((0, y, 250, y+14), fill=255)
            draw.text((0, y), line, font=font, fill=0)
        else:
            draw.text((0, y), line, font=font, fill=255)

        y += 14

    if trains:
        y += 2
        draw.line((0, y, 250, y), fill=255)
        y += 4

        text = format_calling(trains[0]["calling"])
        draw.text((0, y), text[:32], font=font, fill=255)

    image = image.rotate(90, expand=True)
    epd.display(epd.getbuffer(image))
