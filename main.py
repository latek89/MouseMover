# MouseMover by Piotr Latka (fixed)

import pyautogui as pag
import random
import time

pag.FAILSAFE = True  # przesunięcie myszy w róg ekranu przerywa program

curr_coords = pag.position()
afk_counter = 0

# pobierz rozmiar ekranu dynamicznie
screen_width, screen_height = pag.size()

while True:
    current_pos = pag.position()

    if current_pos == curr_coords:
        afk_counter += 1
    else:
        afk_counter = 0
        curr_coords = current_pos

    if afk_counter >= 5:
        x = random.randint(0, screen_width - 1)
        y = random.randint(0, screen_height - 1)

        pag.moveTo(x, y, duration=0.5)
        curr_coords = pag.position()
        afk_counter = 0  # reset po ruchu

    print(f"AFK counter: {afk_counter}")
    time.sleep(2)
