from tkinter import *
import psutil
import sys
import os


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)


def is_app_running(app_name):
    for proc in psutil.process_iter(['name']):
        if app_name.lower() in proc.info['name'].lower():
            proc.kill()
            return True
    return False


def terminateBadPrograms():
    is_app_running(badprograms.get() + ".exe")
    print("Worked/Closed Programs")


window = Tk()
window.geometry("400x400")
window.title("Budget App")

logo = PhotoImage(file=resource_path("logo.png"))
window.iconphoto(True, logo)
window.configure(background="#0f1117")


terminate = Button(window, text="Terminate", fg="white", bg="#e05252",
                activebackground="#f07070", activeforeground="white",
                relief="flat", font=("Helvetica", 11, "bold"),
                cursor="hand2", command=terminateBadPrograms, padx=16, pady=6)
terminate.pack(side="right", pady=10)


badprograms = Entry(window, fg="#e8eaf0", bg="#1c1f2b", insertbackground="#4f8ef7",
              relief="flat", font=("Helvetica", 13),
              highlightthickness=1, highlightbackground="#2a2d3d",
              highlightcolor="#4f8ef7", width=20)

badprograms.pack(side="left", padx=10, ipady=6)


window.mainloop()