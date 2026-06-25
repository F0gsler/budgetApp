from tkinter import *
import psutil
import sys
import os
import threading
import time
import pystray
from pystray import MenuItem as item
from PIL import Image
import json


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)


def get_save_path():
    appdata = os.getenv('APPDATA')
    folder = os.path.join(appdata, "BudgetApp")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "blocked_apps.json")


def save_list():
    with open(get_save_path(), 'w') as f:
        json.dump(blocked_apps, f)


def load_list():
    try:
        with open(get_save_path(), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def is_app_running(app_name):
    closed = False
    for proc in psutil.process_iter(['name']):
        try:
            if app_name.lower() in proc.info['name'].lower():
                proc.kill()
                closed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return closed


def add_to_list():
    app = badprograms.get()
    if app and app not in blocked_apps:
        blocked_apps.append(app)
        listbox.insert(END, app)
        save_list()  # Gem efter tilføjelse
    badprograms.delete(0, END)


def remove_from_list():
    selected = listbox.curselection()
    if selected:
        app = listbox.get(selected[0])
        blocked_apps.remove(app)
        listbox.delete(selected[0])
        save_list()  # Gem efter fjernelse


def kill_loop():
    while True:
        for app in blocked_apps:
            is_app_running(app)
        time.sleep(10)


def hide_window():
    window.withdraw()


def show_window(icon, item):
    window.deiconify()


def quit_app(icon, item):
    save_list()  # Gem når man lukker helt
    icon.stop()
    os._exit(0)


def setup_tray():
    image = Image.open(resource_path("logo.png"))
    menu = pystray.Menu(
        item("Åbn", show_window),
        item("Luk", quit_app)
    )
    icon = pystray.Icon("BudgetApp", image, "Budget App", menu)
    icon.run()


# Load listen når programmet starter
blocked_apps = load_list()

window = Tk()
window.geometry("400x400")
window.title("Budget App")

logo = PhotoImage(file=resource_path("logo.png"))
window.iconphoto(True, logo)
window.configure(background="#0f1117")

window.protocol("WM_DELETE_WINDOW", hide_window)

# Input felt
badprograms = Entry(window, fg="#e8eaf0", bg="#1c1f2b", insertbackground="#4f8ef7",
              relief="flat", font=("Helvetica", 13),
              highlightthickness=1, highlightbackground="#2a2d3d",
              highlightcolor="#4f8ef7", width=20)
badprograms.pack(pady=10, ipady=6)

# Knapper
btn_frame = Frame(window, bg="#0f1117")
btn_frame.pack()

add_btn = Button(btn_frame, text="Tilføj", fg="white", bg="#4f8ef7",
                activebackground="#6aaaf7", activeforeground="white",
                relief="flat", font=("Helvetica", 11, "bold"),
                cursor="hand2", command=add_to_list, padx=16, pady=6)
add_btn.pack(side="left", padx=5)

remove_btn = Button(btn_frame, text="Fjern", fg="white", bg="#e05252",
                activebackground="#f07070", activeforeground="white",
                relief="flat", font=("Helvetica", 11, "bold"),
                cursor="hand2", command=remove_from_list, padx=16, pady=6)
remove_btn.pack(side="left", padx=5)

# Liste
listbox = Listbox(window, fg="#e8eaf0", bg="#1c1f2b",
                  relief="flat", font=("Helvetica", 12),
                  highlightthickness=1, highlightbackground="#2a2d3d",
                  selectbackground="#4f8ef7", width=30, height=10)
listbox.pack(pady=10)

# Fyld listbox med gemte programmer
for app in blocked_apps:
    listbox.insert(END, app)

# Start tråde
threading.Thread(target=kill_loop, daemon=True).start()
threading.Thread(target=setup_tray, daemon=True).start()

window.withdraw()

window.mainloop()