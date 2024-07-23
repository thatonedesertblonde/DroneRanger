
import tkinter as tk
from matplotlib import pyplot as plt


w = tk.Tk()
tk.Label(w, text='DroneRanger')
button_destroy = tk.Button(w, text='First Button', width=25, command=w.destroy)
button_destroy.pack()
w.mainloop()

