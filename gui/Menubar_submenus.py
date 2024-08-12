import tkinter as tk
from tkinter import ttk
import cv2 
from PIL import Image, ImageTk
import os
import obj_detection.tracker as tr


def od():
    #OD window
    class_frame = tk.Tk() #.grid(anchor = 'w')
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
    threat_window = tk.Tk()
    threat_window.title("Threat Attributes:")
    threat_window.geometry('600x300')
    
    
    #dropbox
    threat_label = tk.Label(text = "Threat ON/OFF: ")
    combo_box = ttk.Combobox(threat_window, values=["ON", "OFF"])
    combo_box.set("ON")
    combo_box.pack(padx=10, pady=10)
    combo_box.bind(threat_label, "<<ComboboxSelected>>", onOff)
    threat_label.place(sticky = combo_box)
    

    #threat count--VALID
    '''entry = tk.Entry(threat_window)
    entry.grid(row = 0, column = 2, sticky = 'W')
    tk.Label(threat_window, text='Threat Count: ').grid(row=0, column = 1)'''

   
    print("Threat menu needs to pop up")

class DroneApp:
    def __init__(self, videoWindow, person):
        self.videoWindow = videoWindow
        #self.video_capture = cv2.VideoCapture("/app/droneranger/videos/cafe.mp4")
        #self.video_capture = tr.tracker_init()
        self.model, self.cap, self.size = tr.tracker_init()
        self.result = tr.tracker_save(self.size)
        self.classPerson = person
        self.current_image = None
        self.canvas = tk.Canvas(videoWindow, width=1820, height=1080)
        self.canvas.grid(column=1, row=0)
        self.update_frame()

        '''
        ---creates columns to sticky exactly where you want placements
        videoWindow.columconfigure((0, 1, 2), weight = 1)
        videoWindow.rowconfigure((0, 1, 2, 3, 4), weight = 1)
        ''' 
        
    def update_frame(self):
        frame = tr.track_objects(self.model, self.cap, self.size, 
                                 self.result, self.classPerson)
        self.current_image = Image.fromarray(cv2.cvtColor(frame, 
                                                          cv2.COLOR_BGR2RGB))
        self.photo = ImageTk.PhotoImage(image=self.current_image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        #self.classPerson = person
        self.videoWindow.after(1, self.update_frame)
    # download        
    def download_image(self):
        if self.current_image is not None:
            print("button pressed")
            #file_path = os.path("/app/droneranger/DroneRanger/gui/captures/capture.jpg")
            #ADDED
            file_path = '/app/droneranger/captures/capture.jpg'
            self.current_image.save(file_path)
            #self.current_image.save('/app/droneranger/captures/capture.jpg')
        else:
            print('image is none') 

def var(var):
    person = var.get()
    print(person)
    return person
    
root = tk.Tk()
root.title('DroneRanger')
root.geometry('1820x1080')

#menubar + frame
menubar = tk.Menu(root)
root.config(menu=menubar)

#---OBJECTS
od_tab = tk.Menu(menubar, tearoff = False) #button
menubar.add_cascade(menu = od_tab, label = "Object Detection")

od_tab.add_command(label = "Objects",
                   accelerator = 'crtl+O',
                   command = od)

#---THREAT 
od_tab.add_separator() # next line down
threat_tab = tk.Menu(od_tab, tearoff = False) #tab
od_tab.add_command(label = 'Threat',
                       accelerator = 'ctrl+T',
                       command = onOff)



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

#def setways():

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

#root.config(menu=menubar)
panedwindow = ttk.Panedwindow(root, orient = 'horizontal')
panedwindow.pack(fill = 'both', expand = True)
video_frame = ttk.Frame(root, width = 1720, height = 1000, relief = 'sunken')
panedwindow.add(video_frame)
person = 1
app = DroneApp(video_frame, person)
root.mainloop()