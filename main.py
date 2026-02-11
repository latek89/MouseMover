# MouseMover by Piotr Latka
# logika + konfiguracja

import pyautogui as pag
import random
import time
import threading
from tkinter import ttk


pag.FAILSAFE = True


class MouseMover:
    def __init__(self, status_callback=None):
        self.running = False
        self.thread = None
        self.status_callback = status_callback

        self.afk_limit = 180
        self.move_interval = 5
        self.sleep_time = 1

        self.screen_width, self.screen_height = pag.size()

        self.afk_seconds = 0
        self.total_seconds = 0
        self.active_mode = False

    def update_settings(self, afk_limit, move_interval, width, height):
        self.afk_limit = afk_limit
        self.move_interval = move_interval
        self.screen_width = width
        self.screen_height = height

    def start(self):
        if not self.running:
            self.running = True
            self.afk_seconds = 0
            self.total_seconds = 0
            self.active_mode = False
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False

    def run(self):
        curr_coords = pag.position()

        while self.running:
            current_pos = pag.position()
            self.total_seconds += 1

            if current_pos != curr_coords:
                self.afk_seconds = 0
                self.active_mode = False
                curr_coords = current_pos
            else:
                self.afk_seconds += 1

            if self.afk_seconds >= self.afk_limit:
                self.active_mode = True

            # Aktualizacja GUI
            if self.status_callback:
                self.status_callback(
                    self.afk_seconds,
                    self.total_seconds,
                    self.active_mode,
                    self.afk_limit
                )

            if self.active_mode:
                x = random.randint(0, self.screen_width - 1)
                y = random.randint(0, self.screen_height - 1)

                pag.moveTo(x, y, duration=0.5)
                curr_coords = pag.position()

                time.sleep(self.move_interval)
            else:
                time.sleep(self.sleep_time)
