import tkinter as tk
from tkinter import *
from tkinter import ttk
import time

#entering window
window = tk.Tk() 
window.title('Drone Ranger')
greeting= tk.Label(text = "Welcome to Drone Ranger")
bbutton = tk.Button(window, text = 'Enter', width = 25, command = window.destroy)

#entry
master = tk.Tk()
master.title('Personal Profile')
label1= tk.Label(master, text='First Name').grid(row=0)
label2 = tk.Label(master, text='Last Name').grid(row=1)
e1 = tk.Entry(master)
e2 = tk.Entry(master)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

#checkbox
checkbox = Tk()
checkbox.title('Check Box')
var1 = IntVar()
Checkbutton(checkbox, text='male', variable=var1).grid(row=0, sticky=W)
var2 = IntVar()
Checkbutton(checkbox, text='female', variable=var2).grid(row=1, sticky=W)

#list 
list = Tk()
list.title('List')
Lb = Listbox(list)
Lb.insert(1, 'Python')
Lb.insert(2, 'Java')
Lb.insert(3, 'C++')
Lb.insert(4, 'Any other')

#scrollbar
scroll = Tk()
scroll.title('Scroll Bar')
scrollbar = Scrollbar(scroll)
scrollbar.pack(side=RIGHT, fill=Y)
mylist = Listbox(scroll, yscrollcommand=scrollbar.set)
for line in range(100):
    mylist.insert(END, 'This is line number' + str(line)) 
mylist.pack(side=LEFT, fill=BOTH)
scrollbar.config(command=mylist.yview)

#menu
m = Tk()
m.title('Menu')
menu = Menu(m)
m.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New')
filemenu.add_command(label='Open...')
filemenu.add_separator()
filemenu.add_command(label='Exit', command=m.quit)
helpmenu = Menu(menu)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About')

#drop box
def on_select(event):
    selected_item = combo_box.get()
    label.config(text="Selected Item: " + selected_item)

drop = tk.Tk()
drop.title("Drop Box")

#>>>create label
label = tk.Label(drop, text="Selected Item: ")
label.pack(pady=10)

#>>>create widget
combo_box = ttk.Combobox(drop, values=["Option 1", "Option 2", "Option 3"])
combo_box.pack(pady=5)

#>>>set value
combo_box.set("Option 1")

#>>>combine
combo_box.bind("<<ComboboxSelected>>", on_select)

#progress bar
def start_progress():
    progress.start()

    # >>>simulate a task that takes time to complete
    for i in range(101):
      #>>>simulate work
        time.sleep(0.05)  
        progress['value'] = i
        #>>>update gui
        root.update_idletasks()  
    progress.stop()

root = tk.Tk()
root.title("Progressbar")

#>>>create widget
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=20)

#>>>button to start progress
start_button = tk.Button(root, text="Start Progress", command=start_progress)
start_button.pack(pady=10)

#ticker box
ticker = Tk()
w = Spinbox(ticker, from_=0, to=10)

def add_text_with_newline():
    # Insert some text
    text_widget.insert(tk.END, "First line of text.\n")
    # Insert another line
    text_widget.insert(tk.END, "Second line of text.\n")
    # Insert a blank line
    text_widget.insert(tk.END, "\n")
    # Insert more text
    text_widget.insert(tk.END, "Fourth line of text.\n")

# Create the main window
root = tk.Tk()
root.title("Tkinter Text Widget Example")

# Create a Text widget
text_widget = tk.Text(root, height=10, width=50)
text_widget.pack()

# Create a Button to add text with newlines
add_text_button = tk.Button(root, text="Add Text with Newline", command=add_text_with_newline)
add_text_button.pack()

# Run the application
root.mainloop()

def create_slider_row(frame, row, title, command):
    title_label = tk.Label(frame, text=title)
    title_label.grid(row=row, column=0, padx=5, pady=5)
    
    slider = tk.Scale(frame, from_=0, to=1, orient='horizontal', command=command)
    slider.grid(row=row, column=1, padx=5, pady=5)

    return slider

# Example functions to be activated/deactivated by sliders
def function_1(val):
    if int(val) == 1:
        print("Function 1 activated")
    else:
        print("Function 1 deactivated")

def function_2(val):
    if int(val) == 1:
        print("Function 2 activated")
    else:
        print("Function 2 deactivated")

def function_3(val):
    if int(val) == 1:
        print("Function 3 activated")
    else:
        print("Function 3 deactivated")

# Create the main window
root = tk.Tk()
root.title("Tkinter Slider Activation Example")

# Create a frame to hold the sliders
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Create sliders with titles
slider1 = create_slider_row(frame, 0, "Function 1", function_1)
slider2 = create_slider_row(frame, 1, "Function 2", function_2)
slider3 = create_slider_row(frame, 2, "Function 3", function_3)

# Run the application
root.mainloop()


w.pack()
Lb.pack()
bbutton.pack()
greeting.pack()
drop.mainloop()
root.mainloop()
window.mainloop()