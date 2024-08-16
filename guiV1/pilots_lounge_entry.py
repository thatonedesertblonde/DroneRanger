import tkinter as tk
from tkinter import ttk

#main root window
window = tk.Tk()
window.title("Pilot's Lounge")

frame = tk.Frame(window)
frame.pack()

first_name = tk.StringVar()


pilot_info_frame = tk.LabelFrame(frame, text = "User Info")
pilot_info_frame.grid(row = 0, column = 0, padx = 20, pady = 20)

first_name = tk.Label(pilot_info_frame, text = "First Name: ")
first_name.grid(row = 0, column = 0)
last_name = tk.Label(pilot_info_frame, text = "Last Name: ")
last_name.grid(row = 0, column = 1)

first_name_entry = tk.Entry(pilot_info_frame)
first_name_entry.grid(row = 1, column = 0)
last_name_entry = tk.Entry(pilot_info_frame)
last_name_entry.grid(row = 1, column = 1)

email = tk.Label(pilot_info_frame, text = " Email: ")
email.grid(row = 0, column = 2 )
email_entry = tk.Entry(pilot_info_frame)
email_entry.grid(row = 1, column = 2)

dob = tk.Label(pilot_info_frame, text = " DOB: ")
dob.grid(row = 2, column = 0)
dob_entry = tk.Entry(pilot_info_frame)
dob_entry.grid(row = 3, column = 0)

aircraft = tk.Label(pilot_info_frame, text = "Aircraft: ")
aircraft.grid(row = 2, column = 1)
aircraft_combobox = ttk.Combobox(pilot_info_frame, values = [])
window.mainloop()