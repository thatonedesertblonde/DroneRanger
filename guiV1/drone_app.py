import tkinter as tk
from tkinter import ttk
import cv2 
from PIL import Image, ImageTk
import os
import obj_detection.tracker_func as tr
import threading
from tkinter import Label
from tkinter import filedialog
import sqlite3
from contextlib import closing
import shutil

def pilot_setup(connection):
    # init python variables
    fName = ''
    lName = ''
    iD = ''
    dob = 0
    aircraft= ''
    other = ''

    def submit(connection):
        # tkinter var to python
        fName=fName_tk.get()
        lName=lName_tk.get()
        iD =iD_tk.get()
        dob=dob_tk.get()
        aircraft=aircraft_tk.get()
        other=other_tk.get()
        password=password_tk.get()
        reenter=reenter_tk.get()

        if password != reenter:
            #check_pass_tk="Password don't match"
            check_password.config(text="Password don't match")
            
            return
        else:
            pass

        # Write to db
        # init db
        #connection = sqlite3.connect("/app/droneranger/database/droneapp.db")
        
        # do once
        #cursor = connection.cursor()
        #cursor.execute("CREATE TABLE pilots (iD TEXT, password TEXT, fName TEXT, lName TEXT, dob TEXT, aicraft TEXT, other TEXT)")
        
        # write new user values
        cursor = connection.cursor()
        rows=cursor.execute("SELECT iD, password FROM pilots").fetchall()
        cursor.execute("INSERT INTO pilots values(?, ?, ?, ?, ?, ?, ?)", (iD, password, fName, lName, dob, aircraft, other))
        connection.commit()
        cursor.close
        cursor = connection.cursor()
        rows=cursor.execute("SELECT iD, password FROM pilots").fetchall()
        
        logList = [lName, fName, iD, 
                   dob, aircraft, other]
        logListStr = str(logList)
        pilot_lounge = '/app/droneranger/Pilotslounge/'
        name= lName + '_' + fName + '.txt'
        path_name = pilot_lounge + name

        with open(path_name, 'w') as f:
            f.write(logListStr)
            f.write('\n')

        with open('/app/droneranger/log_data.txt', 'a') as f:
            f.write(logListStr)
            f.write('\n')
            
    window = tk.Toplevel()
    window.title("Pilot's Lounge")
    label = tk.Label(window)
    label.pack()
    frame = tk.Frame(window)
    frame.pack()

    # tkinter variables
    fName_tk = tk.StringVar()
    lName_tk = tk.StringVar()
    iD_tk = tk.StringVar()
    dob_tk = tk.StringVar()
    aircraft_tk = tk.StringVar()
    other_tk = tk.StringVar()
    password_tk = tk.StringVar()
    reenter_tk = tk.StringVar()
    check_pass_tk = tk.StringVar(value='')
    
    # function to get text box info
    # Enter button clicked
    # Send tk variables to python variables
    # firestName python version

    pilot_info_frame = tk.LabelFrame(frame, text = "User Info")
    pilot_info_frame.grid(row = 0, column = 0, padx = 20, pady = 20)

    # Entry's
    first_name_entry = tk.Entry(pilot_info_frame, textvariable=fName_tk)
    first_name_entry.grid(row = 1, column = 0, padx = 10, pady = 10)
    last_name_entry = tk.Entry(pilot_info_frame, textvariable=lName_tk)
    last_name_entry.grid(row = 1, column = 1, padx = 10, pady = 10)
    iD_entry = tk.Entry(pilot_info_frame, textvariable= iD_tk)
    iD_entry.grid(row = 1, column = 2,padx = 10, pady = 10)
    dob_entry = tk.Entry(pilot_info_frame, textvariable= dob_tk)
    dob_entry.grid(row =1, column = 3, padx = 10, pady = 10)
    other_entry = tk.Entry(pilot_info_frame, textvariable=other_tk)
    other_entry.grid(row = 4, column = 1, padx = 10, pady = 10)
    password_entry = tk.Entry(pilot_info_frame, textvariable=password_tk)
    password_entry.grid(row = 4,column = 2, pady = 10)
    reenter_entry = tk.Entry(pilot_info_frame, textvariable=reenter_tk)
    reenter_entry.grid(row = 4,column = 3, pady = 10)

    first_name = tk.Label(pilot_info_frame, text = "First Name: ")
    first_name.grid(row = 0, column = 0)
    last_name = tk.Label(pilot_info_frame, text = "Last Name: ")
    last_name.grid(row = 0, column = 1)
    iD = tk.Label(pilot_info_frame, text = " Identification Number: ")
    iD.grid(row = 0, column = 2 )
    dob = tk.Label(pilot_info_frame, text = " DOB: ")
    dob.grid(row = 0, column = 3)
    #dob_entry = tk.Entry(pilot_info_frame)
    #dob_entry.grid(row = 3, column = 0)

    # pull down different drone types
    aircraft = tk.Label(pilot_info_frame, text = "Aircraft: ")
    aircraft.grid(row = 3, column = 0)
    aircraft_combobox = ttk.Combobox(pilot_info_frame, textvariable=aircraft_tk, 
                                    values = ["MQ-9 Reaper", "Bayraktar TB2", "Global Hawk", "Wing Loong II", "Elbert Hermes 900", "CH-5 Rainbow", "MQ-4C Triton" ])
    aircraft_combobox.grid(row = 4, column = 0)
    aircraft_combobox.set(" Select your Aircraft ")

    other = tk.Label(pilot_info_frame, text="Other: ")
    other.grid(row =3, column = 1)
    
    password = tk.Label(pilot_info_frame, text = "Password: ")
    password.grid(row = 3, column= 2, pady= 10)
    reenter = tk.Label(pilot_info_frame, text = "Re-enter Password: ")
    reenter.grid(row = 3, column= 3, pady = 10)
    
    check_password=tk.Label(pilot_info_frame, text='', fg='red')
    check_password.grid(row=6, column=1, pady=10)
    #img_btn = tk.Button(pilot_info_frame, text = "Upload Your Profile Image", command = imageUploader)
    #img_btn.grid(row = 3, column = 3, padx = 10)
    sub_btn=tk.Button(pilot_info_frame, text = 'Submit', command = lambda: submit(connection))
    sub_btn.grid(row=5, column=3, padx = 10, pady = 20)

                
def mode():
    #mode window
    m_frame = tk.Toplevel()
    m_frame.title("MODE: ")
    m_frame.geometry('200x50+0+102')
    #dropbox
    combo_box = ttk.Combobox(m_frame, values=["MANUAL", "AUTOMATIC"])
    combo_box.pack(pady=5)
    combo_box.set("MANUAL")
    combo_box.bind("<<ComboboxSelected>>", mode)

def unauthorized():
    window = tk.Toplevel()
    window.title("WARNING")
    window.geometry('500x150+0+102')
    u_frame = tk.Frame(window)
    u_frame.pack()

    unauthorized_frame = tk.LabelFrame(u_frame, text = "Access Denied")
    unauthorized_frame.grid(row = 0, column = 1, padx = 10, pady = 10)
    
    u_label = tk.Label(unauthorized_frame, text = "WARNING: Restricted Area")
    u_label.grid(row= 1, column=1, padx = 10, pady = 10)
    #u_label.grid(row=0, column= 0)


def personChange(obj):
    print(obj.get())
    DroneApp.person_sel = obj.get()

def carChange(obj):
    DroneApp.car_sel = obj.get()
    
def truckChange(obj):
    DroneApp.truck_sel = obj.get()

def planeChange(obj):
    DroneApp.plane_sel = obj.get()

def boatChange(obj):
    DroneApp.boat_sel = obj.get()

def people_threat(obj):
    DroneApp.person_th = obj.get()
    
def car_threat(obj):
    DroneApp.car_th = obj.get()

def truck_threat(obj):
    DroneApp.truck_th = obj.get()

def plane_threat(obj):
    DroneApp.plane_th = obj.get()

def boat_threat(obj):
    DroneApp.boat_th = obj.get()

def reset(obj):
    if DroneApp.reset_count == 0:
        DroneApp.reset_count = 1
    else:
        DroneApp.reset_count = 0 
    
def submit(c_people, c_cars, c_trucks, c_planes, c_boats):
    DroneApp.people_th_cnt=c_people.get()
    DroneApp.car_th_cnt=c_cars.get()
    DroneApp.truck_th_cnt=c_trucks.get()
    DroneApp.plane_th_cnt=c_planes.get()
    DroneApp.boat_th_cnt=c_boats.get()

def fcRecOnOff(obj):
    # turn facial rec on of off
    # pass variable from tk to python
    DroneApp.face_rec = obj.get()

def imageUploader(nametk):
    fileTypes = [("Upload Your Profile Picture")]
    path = tk.filedialog.askopenfilenames()
    name=nametk.get()
    print('Name:', name, 'Path: ', path)
    auth_path = os.path.join("/app/droneranger/authorized_users/", name)
    print(auth_path)
    os.mkdir(auth_path)
    for file_path in path:
        if os.path.isfile(file_path):
            shutil.copy(file_path, auth_path)
        else:
            print(f"File not found: {file_path}")


def fr_win():
    #fr frame
    class_frame = tk.Toplevel() #.grid(anchor = 'w')
    class_frame.title("Facial Recognition:")
    class_frame.geometry('360x140+0+102')

    fr_onoff_tk = tk.IntVar(value=0)
    name_tk = tk.StringVar(value="")
    
    count_people = tk.IntVar()
    tk.Checkbutton(class_frame, text='Face Recognition', variable=fr_onoff_tk,
                onvalue=1, offvalue=0, 
                command=lambda:fcRecOnOff(fr_onoff_tk)).grid(row = 1, column=0, 
                                                                padx=10, pady=10, 
                                                                sticky='W')
    tk.Label(class_frame, text='Name: ').grid(row=2, column = 0, 
                                                    padx=10, pady=10)
    tk.Entry(class_frame, textvariable=name_tk).grid(row=2, column=1, 
                                                        pady=10, sticky='W')
    
    #name=name_tk.get() 
    tk.Button(class_frame, text='Add Face Rec. Pics', 
              command=lambda: imageUploader(name_tk)).grid(row=3, column=0, 
                                                    pady=10, sticky='W')

def od():    
    #OD window
    class_frame = tk.Toplevel() #.grid(anchor = 'w')
    class_frame.title("Required Object Detections:")
    class_frame.geometry('550x260+0+102')
    #classes
    people_tk = tk.IntVar(value=1)
    threat_people = tk.IntVar(value=0)
    count_people = tk.IntVar(value=100000000)
    tk.Checkbutton(class_frame, text='People', variable=people_tk,
                onvalue=1, offvalue=0, 
                command=lambda:personChange(people_tk)).grid(row = 1, column=0, 
                                                                padx=10, pady=10, 
                                                                sticky='W')
    tk.Checkbutton(class_frame, text='People Threat On/Off',
                variable=threat_people, 
                command=lambda: people_threat(threat_people)).grid(row=1, column=1, 
                                                                 pady=10, sticky='W')
    tk.Label(class_frame, text='People Count: ').grid(row=1, column = 2, 
                                                    padx=10, pady=10)
    tk.Entry(class_frame, textvariable=count_people).grid(row=1, column=3, 
                                                        pady=10, sticky='W')
    cars_tk = tk.IntVar(value=1)
    threat_car = tk.IntVar(value=0)
    count_cars = tk.IntVar(value=100000000)
    tk.Checkbutton(class_frame, text='Cars', variable=cars_tk, 
                onvalue=1, offvalue=0, 
                command=lambda:carChange(cars_tk)).grid(row = 2, column=0, 
                                                        padx=10, pady=10, 
                                                        sticky='W')
    tk.Checkbutton(class_frame, text='Car Threat On/Off',
                variable=threat_car, 
                command=lambda: car_threat(threat_car)).grid(row=2, column=1, 
                                                             pady=10, sticky='W')
    tk.Label(class_frame, text='Car Count: ').grid(row=2, column = 2, 
                                                    padx=10, pady=10)
    tk.Entry(class_frame, textvariable=count_cars).grid(row=2, column=3, 
                                                        pady=10, sticky='W') 
    trucks_tk = tk.IntVar(value=1)
    threat_trucks = tk.IntVar(value=0)
    count_trucks = tk.IntVar(value=100000000)
    tk.Checkbutton(class_frame, text='Trucks', variable = trucks_tk,  
                onvalue=1, offvalue=0, relief='groove',
                command= lambda: truckChange(trucks_tk)).grid(row = 3, column=0, 
                                                            padx=10, pady=10, 
                                                            sticky='W')
    tk.Checkbutton(class_frame, text='Trucks Threat On/Off',
                variable=threat_trucks, 
                command=lambda: truck_threat(threat_trucks)).grid(row=3, column=1, 
                                                                  pady=10, sticky='W')
    tk.Label(class_frame, text='Truck Count: ').grid(row=3, column=2, 
                                                    padx=10, pady=10)
    tk.Entry(class_frame, textvariable=count_trucks).grid(row=3, column=3, 
                                                        pady=10, sticky='W')    
    planes_tk = tk.IntVar(value=1)
    threat_plane = tk.IntVar(value=0)
    count_plane = tk.IntVar(value=100000000)
    tk.Checkbutton(class_frame, text='Planes', variable = planes_tk, 
                onvalue=1, offvalue=0, 
                command= lambda: planeChange(planes_tk)).grid(row = 4, column=0, 
                                                                padx=10, pady=10, 
                                                                sticky='W')
    tk.Checkbutton(class_frame, text='Plane Threat On/Off',
                variable=threat_plane, 
                command=lambda: plane_threat(threat_plane)).grid(row=4, column=1, 
                                                                 pady=10, sticky='W')

    tk.Label(class_frame, text='Plane Count: ').grid(row=4, column=2, 
                                                    padx=10, pady=10)
    plane_entry = tk.Entry(class_frame, textvariable=count_plane).grid(row=4, column=3, 
                                                        pady=10, sticky='W')
    boats_tk = tk.IntVar(value=1)
    threat_boats = tk.IntVar(value=0)
    count_boats = tk.IntVar(value=100000000)
    tk.Checkbutton(class_frame, text='Boats', variable = boats_tk, 
                onvalue=1, offvalue=0, 
                command= lambda: boatChange(boats_tk)).grid(row = 5, column=0, 
                                                            padx=10, pady=10,
                                                            sticky='W')
    tk.Checkbutton(class_frame, text='Boat Threat On/Off',
                variable=threat_boats, 
                command=lambda: boat_threat(threat_boats)).grid(row=5, column=1, 
                                                                 sticky='W')
    tk.Label(class_frame, text='Boat Count: ').grid(row=5, column=2, 
                                                    padx=10, pady=10)
    tk.Entry(class_frame, textvariable=count_boats).grid(row=5, column=3, 
                                                        pady=10, sticky='W')
    #submit button
    tk.Button(class_frame, text = 'Apply', 
              command = lambda: submit(count_people, count_cars, count_trucks, 
                                       count_plane, count_boats)).grid(row=6, column=2, 
                                           pady=10, sticky='W')

    #reset counter button
    reset_counter_tk=tk.IntVar()
    tk.Button(class_frame, text = 'Reset', 
              command = lambda: reset(reset_counter_tk)).grid(row=6, column=3, 
                                           pady=10, sticky='W')

def submit_em(root, em_window, iD, password):
    # login page
    target_id=iD.get()
    target_password=password.get()
    connection = sqlite3.connect("/app/droneranger/database/droneapp.db")
    cursor = connection.cursor()
    rows=cursor.execute("SELECT password FROM pilots WHERE iD = ?", (target_id,),).fetchall()
    print(rows)
    if rows == []:
        print("don't match")
    elif rows[0][0] == target_password:
        print('passswords match')
        em_window.destroy()  
    else:
        print("somethins iwrong in login screen")
 
def existing_member(root):
    em_window= tk.Toplevel() 
    em_window.geometry('1920x1080')
    em_window.title("Welcome Back")
    em_frame = tk.Frame(em_window)
    em_frame.pack()

    # convert id and password to python
    id_tk  = tk.StringVar(value="")
    password_tk = tk.StringVar(value="")
    # create frame
    em_frame = tk.LabelFrame(em_frame, text = "Login")
    em_frame.grid(row = 0, column = 0, padx = 20, pady = 20)
    # create entry's 
    id_entry = tk.Entry(em_frame, textvariable= id_tk)
    id_entry.grid(row = 0, column = 2)
    password_entry = tk.Entry(em_frame, textvariable= password_tk)
    password_entry.grid(row = 1, column = 2)
    # create labels
    id_label = tk.Label(em_frame, text='ID: ')
    id_label.grid(row = 0, column = 1)
    pass_label = tk.Label(em_frame, text='Password: ')
    pass_label.grid(row = 1, column = 1)
    sub_btn=tk.Button(em_frame, text = 'Submit', 
                      command = lambda: submit_em(root, em_window, id_tk, password_tk))
    sub_btn.grid(row=3, column=2, padx = 10, pady = 20)
    
    root.wait_window(em_window)
    

class menu_bar:
    person_sel=1
    car_sel=1
    truck_sel=1
    plane_sel=1
    boat_sel=1
    person_th=0
    car_th=0
    truck_th=0
    plane_th=0
    boat_th=0
    people_th_cnt=10
    car_th_cnt=10
    truck_th_cnt=10
    plane_th_cnt=10
    boat_th_cnt=10
    face_rec=0  
    reset_count=0
    
    def __init__(self, master):
        self.master = master          
        menubar = tk.Menu(master)
        self.connection = sqlite3.connect("/app/droneranger/database/droneapp.db")
        master.config(menu=menubar)
        od_tab = tk.Menu(menubar, tearoff = False) #button
        menubar.add_cascade(menu = od_tab, label = "Object Detection")
        od_tab.add_command(label = "Objects",
                accelerator = 'crtl+O',
                command = od)

        # face rec
        #fr_tab = tk.Menu(menubar, tearoff = False) #button
        #menubar.add_cascade(menu = od_tab, label = "Face Detection")
        od_tab.add_command(label = "Face Rec",
                accelerator = 'crtl+O',
                command = fr_win)
        
        # mission profile
        mp_tab = tk.Menu(menubar,tearoff = False)
        menubar.add_cascade(menu = mp_tab, label = "Mission Profile")
        
        # MODE   
        m = tk.Menu(mp_tab, tearoff = False)
        mp_tab.add_command(label = "Mode",
                        accelerator = 'crtl+M',
                        command = unauthorized)

        #---SET WAY POINTS
        mp_tab.add_separator()
        wp = tk.Menu(mp_tab,tearoff = False)    
        mp_tab.add_command(label = 'Set Way Points',
                        accelerator = 'crtl+W',
                        command = unauthorized)
        
        #pilots lounge
        pl_tab = tk.Menu(menubar, tearoff = False)
        menubar.add_cascade(menu = pl_tab, label = "Pilot's Lounge")
        pl_tab.add_command(label='New Member', command=lambda: pilot_setup(self.connection))


class DroneApp(menu_bar):
    def __init__(self, master, videoWindow):
        self.master = master
        #self.face_rec = 1
        self.videoWindow = videoWindow
        self.menu_bar = menu_bar(master)
        self.current_image = None
        self.canvas = tk.Canvas(videoWindow, 
                                width=1820, 
                                height=1080)
        self.canvas.grid(column=1, row=0)
        self.od = tr.tracker(DroneApp.person_sel, DroneApp.car_sel, 
                             DroneApp.truck_sel, DroneApp.plane_sel,
                             DroneApp.boat_sel, DroneApp.person_th, DroneApp.car_th,
                             DroneApp.truck_th, DroneApp.plane_th, DroneApp.boat_th,
                             DroneApp.people_th_cnt, DroneApp.car_th_cnt,
                             DroneApp.truck_th_cnt, DroneApp.plane_th_cnt,
                             DroneApp.boat_th_cnt, DroneApp.reset_count)
        self.update_frame()
        
    def update_frame(self):
        if self.face_rec == 0:
            self.frame = self.od.track_objects(DroneApp.person_sel, DroneApp.car_sel, 
                                            DroneApp.truck_sel, DroneApp.plane_sel,
                                            DroneApp.boat_sel, DroneApp.person_th, 
                                            DroneApp.car_th, DroneApp.truck_th, 
                                            DroneApp.plane_th, DroneApp.boat_th,
                                            DroneApp.people_th_cnt, DroneApp.car_th_cnt,
                                            DroneApp.truck_th_cnt, DroneApp.plane_th_cnt,
                                            DroneApp.boat_th_cnt, DroneApp.reset_count)
            self.current_image = Image.fromarray(cv2.cvtColor(self.frame, 
                                                            cv2.COLOR_BGR2RGB))
            self.photo = ImageTk.PhotoImage(image=self.current_image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.videoWindow.after(1, self.update_frame)
        else:
            self.frame = self.od.face_recognition()
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

class DialogWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Dialog")

        tk.Label(self, text="This is a dialog window").pack()
        tk.Button(self, text="Close", command=self.destroy).pack()


def main():    
    root = tk.Tk()
    root.title('DroneRanger')
    root.geometry('1920x1080')
    panedwindow = ttk.Panedwindow(root, orient='horizontal')
    panedwindow.pack(fill='both', expand=True)
    video_frame = ttk.Frame(root, width=1920, height=1080, relief='sunken')
    panedwindow.add(video_frame)
    root.withdraw()
    existing_member(root)
    # Wait for the toplevel window to be closed
    print("Top Level Window has been Closed!")
    root.deiconify()
    app = DroneApp(root, video_frame)
    root.mainloop()


if __name__ == '__main__':
    main()