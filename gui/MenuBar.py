import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title('DroneRanger')
root.geometry('400x300')

def od():
    #OD window
    class_frame = tk.Tk()
    class_frame.title("Required Object Detections:")
    class_frame.geometry('600x300')
    od_window = tk.Label(master = class_frame, text = "Required Object Detections: ")
    
    #classes
    people = tk.IntVar()
    tk.Checkbutton(class_frame, text='people', 
               variable = people).grid(row = 1, sticky='W')
    cars = tk.IntVar()
    tk.Checkbutton(class_frame, text='cars', 
               variable = cars).grid(row = 2, sticky='W')
    trucks = tk.IntVar()
    tk.Checkbutton(class_frame, text='trucks', 
               variable = trucks).grid(row = 3, sticky='W')
    planes = tk.IntVar()
    tk.Checkbutton(class_frame, text='planes', 
               variable = planes).grid(row = 4, sticky='W')
    boats = tk.IntVar()
    tk.Checkbutton(class_frame, text='boats', 
               variable = boats).grid(row = 5, sticky='W')

    print("Object detection menu needs to pop up")

                   
def onOff():
    #threat window
    threat_frame = tk.Tk()
    threat_frame.title("Threat ON/OFF:")
    threat_frame.geometry('300x300')
    #dropbox
    combo_box = ttk.Combobox(threat_frame, values=["ON", "OFF"])
    combo_box.pack(pady=5)
    combo_box.set("ON")
    combo_box.bind("<<ComboboxSelected>>", onOff)

    threat_window = tk.Label(master = threat_frame, text = "Threat ON/OFF: ")
    
    print("Threat menu needs to pop up")
   
def tc():
    tc_frame= tk.Tk()
    tc_frame.title("Threat Count")
    tc_frame.geometry('300x300')

    entry = tk.Entry(tc_frame)
    entry.grid(row = 0, column = 2, sticky = 'W')
    tk.Label(tc_frame, text='Threat Count: ').grid(row=0, column = 1)



#menubar + frame
menubar = tk.Menu()
root.config(menu = menubar)

#---OBJECTS
od_tab = tk.Menu(menubar, tearoff = False) #button
menubar.add_cascade(menu = od_tab, label = "Object Detection")

od_tab.add_command(label = "Objects",
                   accelerator = 'crtl+O',
                   command = od)

#---THREAT ON/OFF
od_tab.add_separator() # next line down
threat_tab = tk.Menu(od_tab, tearoff = False) #tab
od_tab.add_command(label = 'Threat',
                       accelerator = 'ctrl+T',
                       command = onOff)

#---THREAT COUNT
od_tab.add_separator()
threat_count = tk.Menu(od_tab, tearoff = False)
od_tab.add_command(label = 'Threat Count',
                   accelerator = 'crtl+C',
                   command = tc)


# mission profile
mp_tab = tk.Menu(menubar,tearoff = False)
menubar.add_cascade(menu = mp_tab, label = "Mission Profile")

def mode():
    #mode window
    m_frame = tk.Tk()
    m_frame.title("MODE: ")
    m_frame.geometry('600x300')
    #dropbox
    combo_box = ttk.Combobox(m_frame, values=["MANUAL", "AUTOMATIC"])
    combo_box.pack(pady=5)
    combo_box.set("MANUAL")
    combo_box.bind("<<ComboboxSelected>>", mode)

def setways():
    
#---MODE   
m = tk.Menu(mp_tab, tearoff = False)
mp_tab.add_command(label = "Mode",
                   accelerator = 'crtl+M',
                   command = mode)

#---SET WAY POINTS
mp_tab.add_separator()
wp = tk.Menu(mp_tab,tearoff = False)
mp_tab.add_command(label = 'Set Way Points',
                   accelerator = 'crtl+W')
                   #command = setways)
#pilots lounge
pl_tab = tk.Menu(menubar, tearoff = False)
menubar.add_cascade(menu = pl_tab, label = "Pilot's Lounge")




#menubar.add_separator()
#menubar.add_command(label="Exit", command=root.destroy)

root.config(menu = menubar)
root.mainloop()