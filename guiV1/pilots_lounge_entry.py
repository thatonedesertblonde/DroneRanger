import tkinter as tk
from tkinter import ttk

# init python variables
fName = ''
lName = ''

def submit():
    # tkinter var to python
    fName=fName_tk.get()
    lName=lName_tk.get()
    print('************')
    print(fName, lName)
    
    

#main root window
window = tk.Tk()
window.title("Pilot's Lounge")

frame = tk.Frame(window)
frame.pack()

# tkinter variables
fName_tk = tk.StringVar()
lName_tk = tk.StringVar()

# function to get text box info
# Enter button clicked
# Send tk variables to python variables
# firestName python version

pilot_info_frame = tk.LabelFrame(frame, text = "User Info")
pilot_info_frame.grid(row = 0, column = 0, padx = 20, pady = 20)

first_name = tk.Label(pilot_info_frame, text = "First Name: ")
first_name.grid(row = 0, column = 0)
last_name = tk.Label(pilot_info_frame, text = "Last Name: ")
last_name.grid(row = 0, column = 1)

# Entry's
first_name_entry = tk.Entry(pilot_info_frame, textvariable=fName_tk)
first_name_entry.grid(row = 1, column = 0)
last_name_entry = tk.Entry(pilot_info_frame, textvariable=lName_tk)
last_name_entry.grid(row = 1, column = 1)

email = tk.Label(pilot_info_frame, text = " Email: ")
email.grid(row = 0, column = 2 )
email_entry = tk.Entry(pilot_info_frame)
email_entry.grid(row = 1, column = 2)

dob = tk.Label(pilot_info_frame, text = " DOB: ")
dob.grid(row = 2, column = 0)
dob_entry = tk.Entry(pilot_info_frame)
dob_entry.grid(row = 3, column = 0)

# pull down different drone types
aircraft = tk.Label(pilot_info_frame, text = "Aircraft: ")
aircraft.grid(row = 2, column = 1)
aircraft_combobox = ttk.Combobox(pilot_info_frame, values = [])

sub_btn=tk.Button(pilot_info_frame, text = 'Submit', command = submit)
sub_btn.grid(row=3, column=2)
window.mainloop()