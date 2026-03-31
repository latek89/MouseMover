import tkinter as tk
from tkinter import ttk, messagebox
from main import MouseMover

# ============================
#   Windows 11 Style Colors
# ============================
BG = "#f3f3f3"
FG = "#1a1a1a"
FRAME_BG = "#ffffff"
BORDER = "#d0d0d0"
ACCENT = "#2563eb"
ACCENT_HOVER = "#1e4fc7"

GREEN = "#16a34a"
RED = "#dc2626"

# ============================
#   Main Window
# ============================
root = tk.Tk()
root.title("Mouse Mover — Windows 11 Edition")
root.geometry("420x600")
root.configure(bg=BG)
root.resizable(False, False)

# ============================
#   Rounded Frame Simulation
# ============================
def rounded_frame(parent):
    return tk.Frame(
        parent,
        bg=FRAME_BG,
        highlightbackground=BORDER,
        highlightthickness=1,
        bd=0
    )

# ============================
#   Windows 11 Button
# ============================
def w11_button(parent, text, command):
    btn = tk.Label(
        parent,
        text=text,
        bg=ACCENT,
        fg="white",
        padx=16,
        pady=10,
        cursor="hand2",
        font=("Segoe UI", 10, "bold")
    )
    btn.bind("<Button-1>", lambda e: command())
    btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=ACCENT))
    return btn

# ============================
#   Progress Bar Style
# ============================
style = ttk.Style()
style.theme_use("default")
style.configure(
    "W11.Horizontal.TProgressbar",
    troughcolor=FRAME_BG,
    background=ACCENT,
    bordercolor=FRAME_BG,
    lightcolor=ACCENT,
    darkcolor=ACCENT
)

# ============================
#   Status Label
# ============================
status_label = tk.Label(
    root,
    text="Status: STOPPED",
    bg=BG,
    fg=RED,
    font=("Segoe UI", 12, "bold")
)
status_label.pack(pady=15)

# ============================
#   Main Input Frame
# ============================
main_frame = rounded_frame(root)
main_frame.pack(padx=20, pady=10, fill="both")

def add_field(label_text, row):
    label = tk.Label(
        main_frame,
        text=label_text,
        bg=FRAME_BG,
        fg=FG,
        font=("Segoe UI", 10)
    )
    label.grid(row=row, column=0, sticky="w", padx=12, pady=(12, 2))

    entry = tk.Entry(
        main_frame,
        bg="#fafafa",
        fg=FG,
        relief="flat",
        highlightbackground=BORDER,
        highlightthickness=1,
        font=("Segoe UI", 10)
    )
    entry.grid(row=row + 1, column=0, padx=12, pady=(0, 10), sticky="we")
    return entry

time_entry = add_field("Czas bez ruchu (sekundy):", 0)
interval_entry = add_field("Interwał ruchu (sekundy):", 2)
autostop_entry = add_field("Auto-stop po (minuty, 0 = brak limitu):", 4)
screen_entry = add_field("Rozdzielczość ekranu:", 6)

# ============================
#   Progress Bar
# ============================
progress = ttk.Progressbar(
    root,
    style="W11.Horizontal.TProgressbar",
    length=350
)
progress.pack(pady=15)

# ============================
#   AFK + Runtime Counter
# ============================
counter_label = tk.Label(
    root,
    text="AFK: 0s | Runtime: 0s",
    bg=BG,
    fg=FG,
    font=("Segoe UI", 10)
)
counter_label.pack(pady=(0, 10))

# ============================
#   Callbacks
# ============================
def update_counters(afk, total, active, afk_limit):
    counter_label.config(text=f"AFK: {afk}s | Runtime: {total}s")
    if afk_limit > 0:
        progress["value"] = min((afk / afk_limit) * 100, 100)

def auto_stopped():
    status_label.config(text="Status: AUTO STOP", fg=RED)

# ============================
#   MouseMover Instance
# ============================
mover = MouseMover(update_counters, auto_stopped)

# ============================
#   Start / Stop Logic
# ============================
def start_mover():
    try:
        afk = int(time_entry.get())
        interval = int(interval_entry.get())
        max_runtime = int(autostop_entry.get())

        res = screen_entry.get().lower().replace(" ", "")
        if "x" not in res:
            raise ValueError("Nieprawidłowy format rozdzielczości")

        width, height = map(int, res.split("x"))

        mover.update_settings(
            afk_limit=afk,
            move_interval=interval,
            width=width,
            height=height,
            max_runtime_minutes=max_runtime
        )

        mover.start()
        status_label.config(text="Status: RUNNING", fg=GREEN)

    except Exception as e:
        messagebox.showerror("Błąd", f"Nieprawidłowe dane: {e}")

def stop_mover():
    mover.stop()
    status_label.config(text="Status: STOPPED", fg=RED)
    progress["value"] = 0
    counter_label.config(text="AFK: 0s | Runtime: 0s")

def default_settings():
    time_entry.delete(0, tk.END)
    time_entry.insert(0, "180")

    interval_entry.delete(0, tk.END)
    interval_entry.insert(0, "5")

    autostop_entry.delete(0, tk.END)
    autostop_entry.insert(0, "0")

    screen_entry.delete(0, tk.END)
    screen_entry.insert(0, "1920x1080")

default_settings()

# ============================
#   Buttons
# ============================
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=10)

w11_button(btn_frame, "Start", start_mover).grid(row=0, column=0, padx=10)
w11_button(btn_frame, "Stop", stop_mover).grid(row=0, column=1, padx=10)
w11_button(btn_frame, "Domyślne", default_settings).grid(row=0, column=2, padx=10)

root.mainloop()
