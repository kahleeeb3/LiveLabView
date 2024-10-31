import tkinter as tk
import tk_helper as tkh
import data
import datetime as dt
import pandas as pd

class Content:
    def __init__(self, root):

        self.root = root
        self.load_data()
        self.create_window()
        self.create_location_selection()
        self.create_instructor_selection()
        self.create_filter_menu()
        self.create_table()

        # every 10 minutes update the table
        self.auto_update()

    def load_data(self):
        self.df = data.load_df("meetings.csv")
        self.instructors = data.get_instructors(self.df)
        self.locations = data.get_locations(self.df)

    def create_window(self):
        self.window = tkh.Window(self.root)
        self.collapsable_width = 40
    
    def create_location_selection(self):

        # create the collapsable
        location_menu = tkh.Collapsible(master=self.window.left_frame, row=0, column=0, name="Locations", width=self.collapsable_width)

        # add content to the collapsable
        location_scroll = tkh.ScrollFrame(location_menu.collapsed_content, width=self.collapsable_width)
        self.location_vars = {}
        for i, l in enumerate(self.locations):
            self.location_vars[l] = tk.BooleanVar()
            tk.Checkbutton(location_scroll.viewPort, text=l, background="White", variable=self.location_vars[l]).grid(row=i, sticky=tk.W)

        location_scroll.pack(side="top", fill="both", expand=True)

    def create_instructor_selection(self):
        
        # create the collapsable
        instructor_menu = tkh.Collapsible(master=self.window.left_frame, row=1, column=0, name="Instructors", width=self.collapsable_width)

        # add content to the collapsable
        instructor_scroll = tkh.ScrollFrame(instructor_menu.collapsed_content, width=self.collapsable_width)

        self.instructor_vars = {}
        for i, inst in enumerate(self.instructors):
            self.instructor_vars[inst] = tk.BooleanVar()
            tk.Checkbutton(instructor_scroll.viewPort, text=inst, background="White", variable=self.instructor_vars[inst]).grid(row=i, sticky=tk.W)

        instructor_scroll.pack(side="top", fill="both", expand=True)

    def create_filter_menu(self):

        #filter variables
        self.filter_vars = {
            "auto_update": tk.BooleanVar(value=1),
            "date_text" : tk.StringVar(),
            "time": tk.BooleanVar(value=1),
            "date": tk.BooleanVar(value=1),
            "room":tk.BooleanVar(value=0),
            "instructor":tk.BooleanVar(value=0)
        }

        # add widgets
        auto_update_button = tk.Checkbutton(
            self.window.bottom_left_frame, text="Auto Update", background="White", variable=self.filter_vars["auto_update"], command=self.auto_update)
        date_label = tk.Label(self.window.bottom_right_frame, text='Date:', background="White")
        date_entry = tk.Entry(self.window.bottom_right_frame, textvariable=self.filter_vars["date_text"])
        time_button = tk.Checkbutton(self.window.bottom_right_frame, text="Time", background="White", variable=self.filter_vars["time"])
        date_button = tk.Checkbutton(self.window.bottom_right_frame, text="Date", background="White", variable=self.filter_vars["date"])
        room_button = tk.Checkbutton(self.window.bottom_right_frame, text="Room", background="White", variable=self.filter_vars["room"]) 
        instructor_button = tk.Checkbutton(self.window.bottom_right_frame, text="Instructor", background="White", variable=self.filter_vars["instructor"])
        update_button = tk.Button(self.window.bottom_right_frame, text='Update', command=self.on_update_button_press)
        self.update_text = tk.Label(self.window.top_frame, text='Last Update:', background="light grey")

        # define widget locations
        auto_update_button.grid(row=0, column=0, sticky="nsw")
        date_label.grid(row=0, column=0, sticky="nse")
        date_entry.grid(row=0, column=1, sticky="nse")
        time_button.grid(row=0, column=2, sticky="nse")
        date_button.grid(row=0, column=3, sticky="nse")
        room_button.grid(row=0, column=4, sticky="nse")
        instructor_button.grid(row=0, column=5, sticky="nse")
        update_button.grid(row=0, column=6, sticky="nse")
        self.update_text.grid(row=0, column=1, sticky="nse")

        # Expand first column for when you want elements to stick to the right
        self.window.top_frame.grid_columnconfigure(0, weight=1)
        self.window.bottom_right_frame.grid_columnconfigure(0, weight=1)

    def on_update_button_press(self):
        df = self.df
        today = dt.datetime.today()

        # update the filters

        # if a date is provided
        if self.filter_vars["date_text"].get():
            # if you want to filter by that date
            if self.filter_vars["date"].get():
                date_object = dt.datetime.strptime(self.filter_vars["date_text"].get(), "%Y-%m-%d").date()
                df = df[(df["Date"] == date_object)]
        # if a date is not provided, give current date
        else:
            self.filter_vars["date_text"].set(today.strftime('%Y-%m-%d'))
            df = df[(df["Date"] == today.date())]
            
        if self.filter_vars["time"].get():
            df = df[(df["Start"] <= today.time()) & (df["End"] >= today.time())]

        if self.filter_vars["room"].get():
            df_room = df.drop(df.index) # empty df
            for l in self.location_vars:
                if self.location_vars[l].get():
                    temp_df = df[df['Location'].str.contains(l, case=False, na=False)]
                    df_room = pd.concat([df_room, temp_df])

            df = df_room

        if self.filter_vars["instructor"].get():
            df_instructor = df.drop(df.index) # empty df
            for i in self.instructor_vars:
                if self.instructor_vars[i].get():
                    temp_df = df[df["Instructor / Organization"].str.contains(i, case=False, na=False)]
                    df_instructor = pd.concat([df_instructor, temp_df])

            df = df_instructor

        self.table.df = df
        self.table.update_table()

        # modify update text
        self.update_text.config(text=f'Last Update: {dt.datetime.today().strftime('%I:%M %p')}')

    def create_table(self):
        self.table = tkh.Table(self.window.bottom_frame, df=self.df, row=0, column=0)

    def auto_update(self):
        auto_update = self.filter_vars["auto_update"].get()
        if(auto_update):   
            minutes = 10
            seconds = 0
            time_delay = (minutes*60000)+ (seconds * 1000)
            self.on_update_button_press()
            self.root.after(time_delay, self.auto_update)


if __name__=="__main__":
    root = tk.Tk()
    # self.root.state('zoomed')  # Maximize the window
    root.geometry("1200x400")
    root.iconbitmap("icon.ico")
    root.title("LiveLabView")
    content = Content(root)
    content.root.mainloop()