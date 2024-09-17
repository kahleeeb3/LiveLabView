import tkinter as tk
import tk_helper as tkh
import data

class Content:
    def __init__(self):
        self.load_data()
        self.create_window()
        self.create_location_selection()
        self.create_instructor_selection()
        self.create_filter_menu()

    def load_data(self):
        self.df = data.load_df("meetings.csv")
        self.instructors = data.get_instructors(self.df)
        self.locations = data.get_locations(self.df)

    def create_window(self):
        self.root = tk.Tk()
        self.window = tkh.Window(self.root)
        self.collapsable_width = 40

    def create_location_selection(self):
        location_menu = tkh.Collapsable(master=self.window.bottom_left_frame, row=0, column=0, name="Locations", width=self.collapsable_width)
        location_scroll = tkh.ScrollFrame(location_menu.collapsed_content, width=25, height=100)

        self.location_vars = {}
        for i, l in enumerate(self.locations):
            self.location_vars[l] = tk.BooleanVar()
            tk.Checkbutton(location_scroll.viewPort, text=l, background="White", variable=self.location_vars[l]).grid(row=i, sticky=tk.W)

        location_scroll.pack(side="top", fill="both", expand=True)

    def create_instructor_selection(self):
        instructor_menu = tkh.Collapsable(master=self.window.bottom_left_frame, row=1, column=0, name="Instructors", width=self.collapsable_width)
        instructor_scroll = tkh.ScrollFrame(instructor_menu.collapsed_content, width=25, height=100)

        self.instructor_vars = {}
        for i, inst in enumerate(self.instructors):
            self.instructor_vars[inst] = tk.BooleanVar()
            tk.Checkbutton(instructor_scroll.viewPort, text=inst, background="White", variable=self.instructor_vars[inst]).grid(row=i, sticky=tk.W)

        instructor_scroll.pack(side="top", fill="both", expand=True)

    def create_filter_menu(self):
        
        self.filter_vars = {
            "time": tk.BooleanVar(value=1),
            "day": tk.BooleanVar(value=1),
            "room":tk.BooleanVar(value=0),
            "instructor":tk.BooleanVar(value=0)
        }

        update_button = tk.Button(self.window.bottom_right_frame, text='Update', command=self.on_update_button_press)
        time_button = tk.Checkbutton(self.window.bottom_right_frame, text="Time", background="White", variable=self.filter_vars["time"])
        day_button = tk.Checkbutton(self.window.bottom_right_frame, text="Day", background="White", variable=self.filter_vars["day"])
        room_button = tk.Checkbutton(self.window.bottom_right_frame, text="Room", background="White", variable=self.filter_vars["room"])
        instructor_button = tk.Checkbutton(self.window.bottom_right_frame, text="Instructor", background="White", variable=self.filter_vars["instructor"])

        time_button.grid(row=0, column=0, sticky="ew")
        day_button.grid(row=0, column=1, sticky="ew")
        room_button.grid(row=0, column=2, sticky="ew")
        instructor_button.grid(row=0, column=3, sticky="ew")
        update_button.grid(row=0, column=4, sticky="ew")

    def on_update_button_press(self):
        for filter in self.filter_vars:
            print(self.filter_vars[filter].get())






content = Content()
content.root.mainloop()

"""

    def on_update_button_press():
        
        # get which instructors are selected
        for instructor in instructors_vars:
            if instructors_vars[instructor].get():
                print(instructor)

    # define default filtering values
    
    
    # define filtering options button
    

    
    
    root.mainloop()

"""