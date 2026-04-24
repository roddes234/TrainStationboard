import time
import epd2in13g

from config import STATION, PLATFORMS, REFRESH_FAST, REFRESH_NORMAL
from api import get_departures
from display import draw_board
from crs import load_crs


def dynamic_sleep(trains):
    for t in trains:
        if "DUE" in str(t):
            return REFRESH_FAST
    return REFRESH_NORMAL


def main():
    load_crs()

    epd = epd2in13g.EPD()
    epd.init()
    epd.Clear(0xFF)

    i = 0

    while True:
        platform = PLATFORMS[i % len(PLATFORMS)]

        trains = get_departures(STATION, platform)

        draw_board(epd, trains, STATION, platform)

        i += 1

        time.sleep(dynamic_sleep(trains))


if __name__ == "__main__":
    main()
