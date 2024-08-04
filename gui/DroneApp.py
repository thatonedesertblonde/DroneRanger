import tkinter as tk
from tkinter import ttk
import cv2 
from PIL import Image, ImageTk
import os


class DroneApp:
    def __init__(self, buttonWindow, videoWindow):
        
        self.buttonWindow = buttonWindow
        self.videoWindow = videoWindow
        self.video_capture = cv2.VideoCapture("/app/droneranger/videos/cafe.mp4")
        self.current_image = None
        self.canvas = tk.Canvas(videoWindow, width=1820, height=1080)
        self.canvas.grid(column=1, row=0)
        self.update_webcam()
        self.menu_button = tk.Button(buttonWindow, text="Menu", 
                                        command=self.menuButton)
        self.menu_button.grid(column=0, row=5)
    
    def menuButton(self):
        menu = tk.Toplevel()
        menu.grab_set()
        menu.title("Menu")
        frame_classifiers = tk.Frame()
        frame_flight = tk.Frame()
        frame_settings = tk.Frame()
        label_classifiers = tk.Button(frame_classifiers, 
                                      text = "Object Detection")
        label_classifiers.pack()
        label_flight = tk.Button(frame_flight, 
                                 text = "Mission Profile")
        label_flight.pack()
        label_settings = tk.Button(frame_settings, 
                                   text = "Pilot's Lounge")    
        label_settings.pack()

        frame_classifiers.pack()
        frame_flight.pack() 
        frame_settings.pack()


    def update_webcam(self):
        ret, frame = self.video_capture.read()
        frame = cv2.resize(frame, (1820, 1080)) 
        if ret:
            self.current_image = Image.fromarray(cv2.cvtColor(frame, 
                                                              cv2.COLOR_BGR2RGB))
            self.photo = ImageTk.PhotoImage(image=self.current_image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.videoWindow.after(5, self.update_webcam)
            
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


root = tk.Tk()
root.title("DroneRANGER")

# Create an "inner window" frame
#panedwindow = ttk.Panedwindow(root, orient = 'horizontal', alpha=0.3)
panedwindow = ttk.Panedwindow(root, orient = 'horizontal')
panedwindow.pack(fill = 'both', expand = True)

left_button_frame = ttk.Frame(panedwindow, width = 10, height = 300, relief = 'sunken')
video_frame = ttk.Frame(panedwindow, width = 1720, height = 1000, relief = 'sunken')
panedwindow.add(left_button_frame)
panedwindow.add(video_frame, weight = 4)


root.attributes('-alpha', 0.3)

app = DroneApp(left_button_frame, video_frame)

#specialty
specialty_title = tk.StringVar()  
specialty_lb = tk.Label(left_button_frame, textvariable=specialty_title, bg='#fff', fg='#000', font='Helvetica 12 bold', relief='raised')
specialty_title.set("Facial Recognition")

CheckFacialRecognition = tk.IntVar()
Button5 = tk.Checkbutton(left_button_frame, 
                    text = "Threat", 
                    variable = CheckFacialRecognition, 
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    width = 10) 




specialty_lb.grid()
Button5.grid()

root.mainloop()


#if __name__ == 'main':