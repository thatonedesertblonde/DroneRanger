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
        self.download_button = tk.Button(buttonWindow, text="Capture", 
                                        command=self.download_image)
        self.download_button.grid(column=0, row=5)
        
    def update_webcam(self):
        ret, frame = self.video_capture.read()
        frame = cv2.resize(frame, (1820, 1080)) 
        if ret:
            self.current_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
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
# Create an "inner window" frame
#panedwindow = ttk.Panedwindow(root, orient = 'horizontal', alpha=0.3)
panedwindow = ttk.Panedwindow(root, orient = 'horizontal')
panedwindow.pack(fill = 'both', expand = True)

left_button_frame = ttk.Frame(panedwindow, width = 10, height = 300, relief = 'sunken')
video_frame = ttk.Frame(panedwindow, width = 1720, height = 1000, relief = 'sunken')
panedwindow.add(left_button_frame)
panedwindow.add(video_frame, weight = 4)


root.attributes('-alpha', 0.3)

class_title = tk.StringVar()  
classes_lb = tk.Label(left_button_frame, textvariable=class_title, bg='#fff', fg='#000', font='Helvetica 12 bold', relief='raised')
class_title.set("Dectected Classes")

CheckPeople = tk.IntVar() 
CheckVehicles = tk.IntVar() 
CheckBoats = tk.IntVar() 
CheckAirplanes = tk.IntVar()


Button1 = tk.Checkbutton(left_button_frame, 
                    text = "People", 
                    variable = CheckPeople, 
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    width = 10) 

Button2 = tk.Checkbutton(left_button_frame, 
                    text = "Vehicles", 
                    variable = CheckVehicles, 
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    width = 10) 

Button3 = tk.Checkbutton(left_button_frame, 
                    text = "Boats", 
                    variable = CheckBoats, 
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    width = 10) 
   
Button4 = tk.Checkbutton(left_button_frame, 
                    text = "Airplanes", 
                    variable = CheckAirplanes, 
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    width = 10) 

classes_lb.grid()    
Button1.grid() 
Button2.grid() 
Button3.grid() 
Button4.grid() 
#video_window = ttk.Frame(root, relief="sunken")
#video_window.grid() #pack(pady=10, padx=10)
#root.attributes('-zoomed', True)
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