# GUI

import tkinter as tk
from main import MouseMover

# ---------- GUI CALLBACK ----------

def update_counters(afk, total):
    afk_label.config(text=f"AFK: {afk}s")
    total_label.config(text=f"Runtime: {total}s")


mover = MouseMover(status_callback=update_counters)

# ---------- FUNKCJE ----------

def start_mover():
    try:
        afk_time = int(time_entry.get())
        width = int(width_entry.get())
        height = int(height_entry.get())

        mover.update_settings(afk_time, width, height)
        mover.start()
        status_label.config(text="Status: RUNNING", fg="green")

    except ValueError:
        status_label.config(text="Błędne dane!", fg="orange")


def stop_mover():
    mover.stop()
    status_label.config(text="Status: STOPPED", fg="red")
    afk_label.config(text="AFK: 0s")
    total_label.config(text="Runtime: 0s")


def default_settings():
    time_entry.delete(0, tk.END)
    time_entry.insert(0, "180")

    width, height = mover.screen_width, mover.screen_height
    width_entry.delete(0, tk.END)
    width_entry.insert(0, width)
    height_entry.delete(0, tk.END)
    height_entry.insert(0, height)


# ---------- GUI ----------

root = tk.Tk()
root.title("MouseMover")
root.geometry("420x360")
root.resizable(False, False)

tk.Label(root, text="MouseMover", font=("Arial", 16, "bold")).pack(pady=10)

status_label = tk.Label(root, text="Status: STOPPED", fg="red")
status_label.pack()

# --- AFK TIME ---
tk.Label(root, text="Czas bez ruchu (sekundy):").pack()
time_entry = tk.Entry(root, width=10, justify="center")
time_entry.pack(pady=5)

# --- RESOLUTION (OBOK SIEBIE) ---
tk.Label(root, text="Rozdzielczość ekranu:").pack()

res_frame = tk.Frame(root)
res_frame.pack(pady=5)

width_entry = tk.Entry(res_frame, width=8, justify="center")
width_entry.pack(side="left", padx=5)

tk.Label(res_frame, text="x").pack(side="left")

height_entry = tk.Entry(res_frame, width=8, justify="center")
height_entry.pack(side="left", padx=5)

# --- COUNTERS ---
afk_label = tk.Label(root, text="AFK: 0s")
afk_label.pack(pady=3)

total_label = tk.Label(root, text="Runtime: 0s")
total_label.pack(pady=3)

# --- BUTTONS ---
tk.Button(root, text="Start", width=16, command=start_mover).pack(pady=6)
tk.Button(root, text="Stop", width=16, command=stop_mover).pack()
tk.Button(root, text="Default Settings", width=16, command=default_settings).pack(pady=6)

default_settings()
root.mainloop()
