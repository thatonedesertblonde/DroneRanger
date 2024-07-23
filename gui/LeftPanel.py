import tkinter as tk
from tkinter import ttk
from tkinter import *
import time
from tkinter.filedialog import askopenfilename


#buttons --- window
menu = tk.Tk()
menu.title("Menu")

# create frames for menu
frame_classifiers = tk.Frame()
frame_flight = tk.Frame()
frame_settings = tk.Frame()


label_classifiers = tk.Button( master = frame_classifiers, text = "Object Detection")
label_classifiers.pack()

label_flight = tk.Button( master = frame_flight, text = "Mission Profile")
label_flight.pack()

label_settings = tk.Button(master = frame_settings, text = "Pilot's Lounge")
label_settings.pack()

frame_classifiers.pack()
frame_flight.pack()
frame_settings.pack()

#class checkboxes --- window
class_frame = Tk()
class_frame.title("Classifications")


class_label = tk.Label(master = class_frame, text = "Classifiers: ")
#class_label.pack()

people = IntVar()
Checkbutton(class_frame, text='people', variable = people).grid(row = 0, sticky=W)
cars = IntVar()
Checkbutton(class_frame, text='cars', variable = cars).grid(row = 1, sticky=W)
trucks = IntVar()
Checkbutton(class_frame, text='trucks', variable = trucks).grid(row = 2, sticky=W)
planes = IntVar()
Checkbutton(class_frame, text='planes', variable = planes).grid(row = 3, sticky=W)

#on/off option --- window
def on_select(event):
    selected_item = combo_box.get()
    label.config(text = "Threat: " + selected_item)

root = tk.Tk()
root.title("Threat")

label = tk.Label(root, text="Threat: ")
label.pack(pady=10)

combo_box = ttk.Combobox(root, values=["ON", "OFF"])
combo_box.pack(pady=5)
combo_box.set("ON")
combo_box.bind("<<ComboboxSelected>>", on_select)

#threat entry --- window
master = Tk()
master.title("Threat Count")

Label(master, text='Threat Count: ').grid(row=0)
entry = Entry(master)
entry.grid(row=0, column=1)

#specialty --- window
facial_window = tk.Tk()
facial_window.title("Facial Recognition")

def open_file():

    filepath = askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not filepath:

        return
    txt_edit.delete("1.0", tk.END)

    with open(filepath, mode="r", encoding="utf-8") as input_file:

        text = input_file.read()

        txt_edit.insert(tk.END, text)

    facial_window.title(f"Simple Text Editor - {filepath}")

btn_open = tk.Button(facial_window, text="Download File", command=open_file)

'''need to add open file/download '''
def start_progress():
    progress.start()

    for i in range(101):
        time.sleep(0.05)  
        progress['value'] = i
        root.update_idletasks()  
    progress.stop()

progress = ttk.Progressbar(facial_window, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=20)

start_button = tk.Button(facial_window, text="Start Progress", command=start_progress)
start_button.pack(pady=10)





root.mainloop()
menu.mainloop()