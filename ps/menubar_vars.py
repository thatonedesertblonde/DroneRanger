import tkinter as tk
from tkinter import ttk
import time


def callback():
    print('Callback')
    peopleClass = people_sel.get()
    print(peopleClass)


#Create an instance of Tkinter frame
win = tk.Tk()
#Set the geometry of Tkinter Frame
win.geometry("750x250")

#Initialize a Menu Bar
menubar = tk.Menu(win)

#Setup variables for passing classes
people_sel = tk.IntVar()
cars_sel = tk.IntVar()
trucks_sel = tk.IntVar()
airplanes_sel = tk.IntVar()
bus_sel = tk.IntVar()
boats_sel = tk.IntVar()

# init all classes selected
people_sel.set(1)
cars_sel.set(1)
trucks_sel.set(1)
airplanes_sel.set(1)
bus_sel.set(1)
boats_sel.set(1)

#Add Menu Items in the MenuBar
menu_items = tk.Menu(menubar)
menu_items.add_checkbutton(label="People", onvalue=1, offvalue=0, 
                           variable=people_sel, command=lambda: callback())
menu_items.add_checkbutton(label="Cars", onvalue=1, offvalue=0, 
                           variable=cars_sel, command=lambda: callback())
menu_items.add_checkbutton(label="Trucks", onvalue=1, offvalue=0, 
                           variable=trucks_sel, command=lambda: callback())
menu_items.add_checkbutton(label="Airplanes", onvalue=1, offvalue=0, 
                           variable=airplanes_sel, command=lambda: callback())
menu_items.add_checkbutton(label="Bus", onvalue=1, offvalue=0, 
                           variable=bus_sel, command=lambda: callback())
menu_items.add_checkbutton(label="Boats", onvalue=1, offvalue=0, 
                           variable=boats_sel, command=lambda: callback())


# Add the Viwable Menu to the MenuBar
menubar.add_cascade(label='Classes', menu=menu_items)
win.config(menu=menubar)

win.mainloop()