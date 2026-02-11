import tkinter as tk
from tkinter import ttk
from main import MouseMover


# ---------- CALLBACKS ----------

def update_counters(afk, total, active, afk_limit):
    afk_label.config(text=f"AFK: {afk}s")
    total_label.config(text=f"Runtime: {total}s")

    progress["maximum"] = afk_limit
    progress["value"] = afk

    if active:
        status_icon.config(text="🟢 ACTIVE", fg="green")
    else:
        status_icon.config(text="🔴 WAITING", fg="red")


def auto_stopped():
    status_label.config(text="Status: AUTO STOP", fg="orange")
    status_icon.config(text="🔴 STOPPED", fg="red")


mover = MouseMover(
    status_callback=update_counters,
    stop_callback=auto_stopped
)


# ---------- FUNKCJE ----------

def start_mover():
    try:
        afk_time = int(time_entry.get())
        move_interval = int(interval_entry.get())
        width = int(width_entry.get())
        height = int(height_entry.get())
        max_runtime = int(runtime_entry.get())

        mover.update_settings(
            afk_time,
            move_interval,
            width,
            height,
            max_runtime
        )

        mover.start()
        status_label.config(text="Status: RUNNING", fg="green")

    except ValueError:
        status_label.config(text="Błędne dane!", fg="orange")


def stop_mover():
    mover.stop()
    status_label.config(text="Status: STOPPED", fg="red")
    status_icon.config(text="🔴 STOPPED", fg="red")
    afk_label.config(text="AFK: 0s")
    total_label.config(text="Runtime: 0s")
    progress["value"] = 0


def default_settings():
    time_entry.delete(0, tk.END)
    time_entry.insert(0, "180")

    interval_entry.delete(0, tk.END)
    interval_entry.insert(0, "5")

    runtime_entry.delete(0, tk.END)
    runtime_entry.insert(0, "0")

    width, height = mover.screen_width, mover.screen_height
    width_entry.delete(0, tk.END)
    width_entry.insert(0, width)
    height_entry.delete(0, tk.END)
    height_entry.insert(0, height)


# ---------- GUI ----------

root = tk.Tk()
root.title("MouseMover")
root.resizable(False, False)
root.configure(padx=20, pady=20)

tk.Label(root, text="MouseMover", font=("Arial", 16, "bold")).pack(pady=10)

status_label = tk.Label(root, text="Status: STOPPED", fg="red")
status_label.pack()

status_icon = tk.Label(root, text="🔴 STOPPED", font=("Arial", 12, "bold"))
status_icon.pack(pady=5)

# AFK TIME
tk.Label(root, text="Czas bez ruchu (sekundy):").pack()
time_entry = tk.Entry(root, width=10, justify="center")
time_entry.pack(pady=5)

# MOVE INTERVAL
tk.Label(root, text="Interwał ruchu (sekundy):").pack()
interval_entry = tk.Entry(root, width=10, justify="center")
interval_entry.pack(pady=5)

# AUTO STOP
tk.Label(root, text="Auto stop po (minuty, 0 = brak limitu):").pack()
runtime_entry = tk.Entry(root, width=10, justify="center")
runtime_entry.pack(pady=5)

# STATUS
tk.Label(root, text="Postęp do aktywacji:").pack(pady=5)
progress = ttk.Progressbar(root, length=250)
progress.pack()

# RESOLUTION
tk.Label(root, text="Rozdzielczość ekranu:").pack(pady=5)

res_frame = tk.Frame(root)
res_frame.pack()

width_entry = tk.Entry(res_frame, width=8, justify="center")
width_entry.pack(side="left", padx=5)

tk.Label(res_frame, text="x").pack(side="left")

height_entry = tk.Entry(res_frame, width=8, justify="center")
height_entry.pack(side="left", padx=5)

# COUNTERS
afk_label = tk.Label(root, text="AFK: 0s")
afk_label.pack(pady=3)

total_label = tk.Label(root, text="Runtime: 0s")
total_label.pack(pady=3)

# BUTTONS
tk.Button(root, text="Start", width=16, command=start_mover).pack(pady=6)
tk.Button(root, text="Stop", width=16, command=stop_mover).pack()
tk.Button(root, text="Default Settings", width=16, command=default_settings).pack(pady=6)

default_settings()

root.mainloop()
