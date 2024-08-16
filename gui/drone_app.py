import tkinter as tk
from tkinter import ttk
import cv2 
from PIL import Image, ImageTk
import os
import obj_detection.tracker_func as tr
import threading

                
def onOff():
    #threat window
    threat_frame = tk.Tk()
    threat_frame.title("Threat ON/OFF:")
    threat_frame.geometry('300x300')
    #dropbox
    threat_people = tk.IntVar()
    combo_box = tk.Checkbutton(threat_frame, text='People',
                             variable=threat_people).grid(row=1, 
                                                          sticky='W')
    #combo_box.pack(pady=5)
    combo_box.set("ON")
    #combo_box.bind("<<ComboboxSelected>>", onOff)

    threat_window = tk.Label(master = threat_frame, text = "Threat ON/OFF: ")
    
    print("Threat menu needs to pop up")
    
def tc():
    tc_frame= tk.Tk()
    tc_frame.title("Threat Count")
    tc_frame.geometry('300x300')

    entry = tk.Entry(tc_frame)
    entry.grid(row = 0, column = 2, sticky = 'W')
    tk.Label(tc_frame, text='Threat Count: ').grid(row=0, column = 1)

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

def personChange(obj):
    DroneApp.person_sel = obj.get()
    print('person button click ************************: ', DroneApp.person_sel)

def carChange(obj):
    DroneApp.car_sel = obj.get()
    print('car button click ************************: ', DroneApp.car_sel)
    
def truckChange(obj):
    DroneApp.truck_sel = obj.get()
    print('truck button click ************************: ', DroneApp.truck_sel)

def planeChange(obj):
    DroneApp.plane_sel = obj.get()
    print('plane button click ************************: ', DroneApp.plane_sel)

def boatChange(obj):
    DroneApp.boat_sel = obj.get()
    print('boat button click ************************: ', DroneApp.boat_sel)


def od():
    #OD window
    class_frame = tk.Tk() #.grid(anchor = 'w')
    class_frame.title("Required Object Detections:")
    class_frame.geometry('550x220')
    #od_window = tk.Label(master = class_frame, text = "Required Object Detections: ")
 
    #classes
    people_tk = tk.IntVar(value=1)
    threat_people = tk.IntVar()
    count_people = tk.StringVar()
    tk.Checkbutton(class_frame, text='People', variable=people_tk,
                   onvalue=1, offvalue=0, 
                   command=lambda:personChange(people_tk)).grid(row = 1, column=0, 
                                                                padx=10, pady=10, 
                                                                sticky='W')
    tk.Checkbutton(class_frame, text='People Threat On/Off',
                   variable=threat_people).grid(row=1, column=1, 
                                                pady=10, sticky='W')
    tk.Label(class_frame, text='People Count: ').grid(row=1, column = 2, 
                                                      padx=10, pady=10)
    tk.Entry(class_frame, textvariable=count_people).grid(row=1, column=3, 
                                                          pady=10, sticky='W')
 
    cars_tk = tk.IntVar(value=1)
    threat_car = tk.IntVar()
    count_cars = tk.StringVar()
    tk.Checkbutton(class_frame, text='Cars', variable=cars_tk, 
                   onvalue=1, offvalue=0, 
                   command=lambda:carChange(cars_tk)).grid(row = 2, column=0, 
                                                           padx=10, pady=10, 
                                                           sticky='W')
    tk.Checkbutton(class_frame, text='Car Threat On/Off',
                   variable=threat_car).grid(row=2, column=1, 
                                             pady=10, sticky='W')
    tk.Label(class_frame, text='Car Count: ').grid(row=2, column = 2, 
                                                      padx=10, pady=10)
    tk.Entry(class_frame, textvariable=count_cars).grid(row=2, column=3, 
                                                          pady=10, sticky='W') 
    
    trucks_tk = tk.IntVar(value=1)
    threat_trucks = tk.IntVar()
    count_trucks = tk.StringVar()
    tk.Checkbutton(class_frame, text='Trucks', variable = trucks_tk,  
                   onvalue=1, offvalue=0, 
                   command= lambda: truckChange(trucks_tk)).grid(row = 3, column=0, 
                                                             padx=10, pady=10, 
                                                             sticky='W')
    tk.Checkbutton(class_frame, text='Trucks Threat On/Off',
                   variable=threat_trucks).grid(row=3, column=1, 
                                                pady=10, sticky='W')
    tk.Label(class_frame, text='Truck Count: ').grid(row=3, column=2, 
                                                      padx=10, pady=10)
    tk.Entry(class_frame, textvariable=count_trucks).grid(row=3, column=3, 
                                                          pady=10, sticky='W')    
    
    planes_tk = tk.IntVar(value=1)
    threat_plane = tk.IntVar()
    count_plane = tk.StringVar()
    tk.Checkbutton(class_frame, text='Planes', variable = planes_tk, 
                   onvalue=1, offvalue=0, 
                   command= lambda: planeChange(planes_tk)).grid(row = 4, column=0, 
                                                                 padx=10, pady=10, 
                                                                 sticky='W')
    tk.Checkbutton(class_frame, text='Plane Threat On/Off',
                   variable=threat_plane).grid(row=4, column=1, 
                                               pady=10, sticky='W')
    tk.Label(class_frame, text='Plane Count: ').grid(row=4, column=2, 
                                                      padx=10, pady=10)
    tk.Entry(class_frame, textvariable=count_plane).grid(row=4, column=3, 
                                                         pady=10, sticky='W')
    
    boats_tk = tk.IntVar(value=1)
    threat_boats = tk.IntVar()
    count_boats = tk.StringVar()
    tk.Checkbutton(class_frame, text='Boats', variable = boats_tk, 
                   onvalue=1, offvalue=0, 
                   command= lambda: boatChange(boats_tk)).grid(row = 5, column=0, 
                                                               padx=10, pady=10,
                                                               sticky='W')
    tk.Checkbutton(class_frame, text='Boat Threat On/Off',
                   variable=threat_boats, ).grid(row=5, column=1, sticky='W')
    tk.Label(class_frame, text='Boat Count: ').grid(row=5, column=2, 
                                                      padx=10, pady=10)
    tk.Entry(class_frame, textvariable=count_boats).grid(row=5, column=3, 
                                                         pady=10, sticky='W')



class menu_bar:
    person_sel = 1
    car_sel = 1
    truck_sel = 1
    plane_sel =1
    boat_sel=1
    
    def __init__(self, master):
        self.master = master          
        menubar = tk.Menu(master)
        master.config(menu=menubar)
        
        od_tab = tk.Menu(menubar, tearoff = False) #button
        menubar.add_cascade(menu = od_tab, label = "Object Detection")

        od_tab.add_command(label = "Objects",
                   accelerator = 'crtl+O',
                   command = od)

        #OD window
        class_frame = tk.Tk() #.grid(anchor = 'w')
        class_frame.title("Required Object Detections:")
        class_frame.geometry('550x220')
        #od_window = tk.Label(master = class_frame, text = "Required Object Detections: ")
    
        #classes
        people_tk = tk.IntVar(value=1)
        threat_people = tk.IntVar()
        count_people = tk.StringVar()
        tk.Checkbutton(class_frame, text='People', variable=people_tk,
                    onvalue=1, offvalue=0, 
                    command=lambda:personChange(people_tk)).grid(row = 1, column=0, 
                                                                    padx=10, pady=10, 
                                                                    sticky='W')
        tk.Checkbutton(class_frame, text='People Threat On/Off',
                    variable=threat_people).grid(row=1, column=1, 
                                                    pady=10, sticky='W')
        tk.Label(class_frame, text='People Count: ').grid(row=1, column = 2, 
                                                        padx=10, pady=10)
        tk.Entry(class_frame, textvariable=count_people).grid(row=1, column=3, 
                                                            pady=10, sticky='W')
    
        cars_tk = tk.IntVar(value=1)
        threat_car = tk.IntVar()
        count_cars = tk.StringVar()
        tk.Checkbutton(class_frame, text='Cars', variable=cars_tk, 
                    onvalue=1, offvalue=0, 
                    command=lambda:carChange(cars_tk)).grid(row = 2, column=0, 
                                                            padx=10, pady=10, 
                                                            sticky='W')
        tk.Checkbutton(class_frame, text='Car Threat On/Off',
                    variable=threat_car).grid(row=2, column=1, 
                                                pady=10, sticky='W')
        tk.Label(class_frame, text='Car Count: ').grid(row=2, column = 2, 
                                                        padx=10, pady=10)
        tk.Entry(class_frame, textvariable=count_cars).grid(row=2, column=3, 
                                                            pady=10, sticky='W') 
        
        trucks_tk = tk.IntVar(value=1)
        threat_trucks = tk.IntVar()
        count_trucks = tk.StringVar()
        tk.Checkbutton(class_frame, text='Trucks', variable = trucks_tk,  
                    onvalue=1, offvalue=0, 
                    command= lambda: truckChange(trucks_tk)).grid(row = 3, column=0, 
                                                                padx=10, pady=10, 
                                                                sticky='W')
        tk.Checkbutton(class_frame, text='Trucks Threat On/Off',
                    variable=threat_trucks).grid(row=3, column=1, 
                                                    pady=10, sticky='W')
        tk.Label(class_frame, text='Truck Count: ').grid(row=3, column=2, 
                                                        padx=10, pady=10)
        tk.Entry(class_frame, textvariable=count_trucks).grid(row=3, column=3, 
                                                            pady=10, sticky='W')    
        
        planes_tk = tk.IntVar(value=1)
        threat_plane = tk.IntVar()
        count_plane = tk.StringVar()
        tk.Checkbutton(class_frame, text='Planes', variable = planes_tk, 
                    onvalue=1, offvalue=0, 
                    command= lambda: planeChange(planes_tk)).grid(row = 4, column=0, 
                                                                    padx=10, pady=10, 
                                                                    sticky='W')
        tk.Checkbutton(class_frame, text='Plane Threat On/Off',
                    variable=threat_plane).grid(row=4, column=1, 
                                                pady=10, sticky='W')
        tk.Label(class_frame, text='Plane Count: ').grid(row=4, column=2, 
                                                        padx=10, pady=10)
        tk.Entry(class_frame, textvariable=count_plane).grid(row=4, column=3, 
                                                            pady=10, sticky='W')
        
        boats_tk = tk.IntVar(value=1)
        threat_boats = tk.IntVar()
        count_boats = tk.StringVar()
        tk.Checkbutton(class_frame, text='Boats', variable = boats_tk, 
                    onvalue=1, offvalue=0, 
                    command= lambda: boatChange(boats_tk)).grid(row = 5, column=0, 
                                                                padx=10, pady=10,
                                                                sticky='W')
        tk.Checkbutton(class_frame, text='Boat Threat On/Off',
                    variable=threat_boats, ).grid(row=5, column=1, sticky='W')
        tk.Label(class_frame, text='Boat Count: ').grid(row=5, column=2, 
                                                        padx=10, pady=10)
        tk.Entry(class_frame, textvariable=count_boats).grid(row=5, column=3, 
                                                             pady=10, sticky='W')


        
        
        
        '''
        #---OBJECTS
        od_tab = tk.Menu(menubar, tearoff=0) #button
        od_menubar = tk.Menu(od_tab)
        od_menubar.add_checkbutton(label="People", variable=people_tk, 
                                   onvalue=1, offvalue=0,
                                   command= lambda: personChange(people_tk))        
        od_menubar.add_checkbutton(label="Cars", variable=cars_tk,
                                   onvalue=1, offvalue=0,
                                   command= lambda: carChange(cars_tk))
        od_menubar.add_checkbutton(label="Trucks", variable=trucks_tk,
                                   onvalue=1, offvalue=0,
                                   command= lambda: truckChange(trucks_tk))
        od_menubar.add_checkbutton(label="Planes", variable=planes_tk, 
                                   onvalue=1, offvalue=0, 
                                   command= lambda: planeChange(planes_tk))
        od_menubar.add_checkbutton(label="Boats", variable=boats_tk,
                                   onvalue=1, offvalue=0,
                                   command= lambda: boatChange(boats_tk))

        od_tab.add_cascade(menu=od_menubar, label="Objects", underline=0)
        menubar.add_cascade(label="ObjDetect", underline=0, menu=od_tab)

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
        '''

class DroneApp(menu_bar):
    def __init__(self, master, videoWindow):
        self.master = master
        self.videoWindow = videoWindow
        self.menu_bar = menu_bar(master)
        self.current_image = None
        self.canvas = tk.Canvas(videoWindow, 
                                width=1820, 
                                height=1080)
        self.canvas.grid(column=1, row=0)
        self.od = tr.tracker(DroneApp.person_sel, DroneApp.car_sel, 
                             DroneApp.truck_sel, DroneApp.plane_sel,
                             DroneApp.boat_sel)
        self.update_frame()
        
    def update_frame(self):
        self.frame = self.od.track_objects(DroneApp.person_sel, DroneApp.car_sel, 
                                           DroneApp.truck_sel, DroneApp.plane_sel,
                                           DroneApp.boat_sel)
        self.current_image = Image.fromarray(cv2.cvtColor(self.frame, 
                                                          cv2.COLOR_BGR2RGB))
        self.photo = ImageTk.PhotoImage(image=self.current_image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.videoWindow.after(1, self.update_frame)
    
    # download        
    def download_image(self):
        if self.current_image is not None:
            print("button pressed")
            file_path = '/app/droneranger/captures/capture.jpg'
            self.current_image.save(file_path)
        else:
            print('image is none') 

def main():    
    root = tk.Tk()
    root.title('DroneRanger')
    root.geometry('1920x1080')

    panedwindow = ttk.Panedwindow(root, orient='horizontal')
    panedwindow.pack(fill='both', expand=True)
    video_frame = ttk.Frame(root, width=1920, height=1080, relief='sunken')
    panedwindow.add(video_frame)
 
    app = DroneApp(root, video_frame)
    root.mainloop()


if __name__ == '__main__':
    main()