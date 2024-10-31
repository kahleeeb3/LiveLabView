import tkinter as tk
from Resizing import Window
from Collapsible import Collapsible
from Table import Table
import seaborn as sns

def create_widgets(window):

    #filter variables
    filter_vars = {
        "auto_update": tk.BooleanVar(value=1),
        "date_text" : tk.StringVar(),
        "time": tk.BooleanVar(value=1),
        "date": tk.BooleanVar(value=1),
        "room":tk.BooleanVar(value=0),
        "instructor":tk.BooleanVar(value=0)
    }

    # add widgets
    auto_update_button = tk.Checkbutton(
        window.bottom_left_frame, text="Auto Update", background="White", variable=filter_vars["auto_update"], command=auto_update)
    date_label = tk.Label(window.bottom_right_frame, text='Date:')
    date_entry = tk.Entry(window.bottom_right_frame, textvariable=filter_vars["date_text"])
    time_button = tk.Checkbutton(window.bottom_right_frame, text="Time", background="White", variable=filter_vars["time"])
    date_button = tk.Checkbutton(window.bottom_right_frame, text="Date", background="White", variable=filter_vars["date"])
    room_button = tk.Checkbutton(window.bottom_right_frame, text="Room", background="White", variable=filter_vars["room"]) 
    instructor_button = tk.Checkbutton(window.bottom_right_frame, text="Instructor", background="White", variable=filter_vars["instructor"])
    update_button = tk.Button(window.bottom_right_frame, text='Update', command=on_update_button_press)
    update_text = tk.Label(window.top_frame, text='Last Update:', background="light grey")

    # define widget locations
    auto_update_button.grid(row=0, column=0, sticky="nsw")
    date_label.grid(row=0, column=0, sticky="nse")
    date_entry.grid(row=0, column=1, sticky="nse")
    time_button.grid(row=0, column=2, sticky="nse")
    date_button.grid(row=0, column=3, sticky="nse")
    room_button.grid(row=0, column=4, sticky="nse")
    instructor_button.grid(row=0, column=5, sticky="nse")
    update_button.grid(row=0, column=6, sticky="nse")
    update_text.grid(row=0, column=1, sticky="nse")

    # Expand first column for when you want elements to stick to the right
    window.top_frame.grid_columnconfigure(0, weight=1)
    window.bottom_right_frame.grid_columnconfigure(0, weight=1)

    # collapsable
    collapsable_width = 25
    location_menu = Collapsible(master=window.left_frame, row=0, column=0, name="Locations", width=collapsable_width)
    instructor_menu = Collapsible(master=window.left_frame, row=1, column=0, name="Instructors", width=collapsable_width)

    # table
    taxis = sns.load_dataset('taxis').head()
    table = Table(window.bottom_frame, df=taxis, row=0, column=0)

def on_update_button_press():
    print("Pressed Button")

def auto_update():
    print("Auto Updated")

if __name__=="__main__":
    root = tk.Tk()
    # root.state('zoomed')
    root.geometry("1200x400")
    window = Window(root)
    create_widgets(window)
    root.mainloop()