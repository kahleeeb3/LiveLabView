import tkinter as tk
from tkinter import ttk
import tk_helper as tkh
import data
import datetime as dt
import pandas as pd

class Content:
    def __init__(self):
        self.load_data()
        self.create_window()
        self.create_location_selection()
        self.create_instructor_selection()
        self.create_filter_menu()
        self.create_table()

    def load_data(self):
        self.df = data.load_df("meetings.csv")
        self.instructors = data.get_instructors(self.df)
        self.locations = data.get_locations(self.df)

    def create_window(self):
        self.root = tk.Tk()
        self.window = tkh.Window(self.root)
        self.collapsable_width = 40
        self.collapsable_height = 96

    def create_location_selection(self):
        location_menu = tkh.Collapsable(master=self.window.bottom_left_frame, row=0, column=0, name="Locations", width=self.collapsable_width)
        location_scroll = tkh.ScrollFrame(location_menu.collapsed_content, width=25, height=self.collapsable_height)

        self.location_vars = {}
        for i, l in enumerate(self.locations):
            self.location_vars[l] = tk.BooleanVar()
            tk.Checkbutton(location_scroll.viewPort, text=l, background="White", variable=self.location_vars[l]).grid(row=i, sticky=tk.W)

        location_scroll.pack(side="top", fill="both", expand=True)

    def create_instructor_selection(self):
        instructor_menu = tkh.Collapsable(master=self.window.bottom_left_frame, row=1, column=0, name="Instructors", width=self.collapsable_width)
        instructor_scroll = tkh.ScrollFrame(instructor_menu.collapsed_content, width=25, height=self.collapsable_height)

        self.instructor_vars = {}
        for i, inst in enumerate(self.instructors):
            self.instructor_vars[inst] = tk.BooleanVar()
            tk.Checkbutton(instructor_scroll.viewPort, text=inst, background="White", variable=self.instructor_vars[inst]).grid(row=i, sticky=tk.W)

        instructor_scroll.pack(side="top", fill="both", expand=True)

    def create_filter_menu(self):
        
        self.update_text = tk.Label(self.window.top_frame, text='Last Update:', background="light grey")
        self.update_text.grid(row=0, column=0, sticky="e")
        
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

        time_button.grid(row=0, column=1, sticky="nsew")
        day_button.grid(row=0, column=2, sticky="nsew")
        room_button.grid(row=0, column=3, sticky="nsew")
        instructor_button.grid(row=0, column=4, sticky="nsew")
        update_button.grid(row=0, column=5, sticky="nsew")

    def on_update_button_press(self):
        df = self.df
        today = dt.datetime.today()

        # update the filters
        if self.filter_vars["time"].get():
            df = df[(df["Start"] <= today.time()) & (df["End"] >= today.time())]

        if self.filter_vars["day"].get():
            df = df[(df["Date"] == today.date())]

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

        self.df_update = df
        self.update_table()

    def create_table(self):
        self.treeview = ttk.Treeview(self.window.bottom_right_frame, show="headings")
        self.treeview.grid(row=1, column=0, columnspan = 6,sticky="nsew")
        columns = self.df.columns.values.tolist()
        sizes = {"Name":95,"Title":160, "Start": 60, "End": 60, "Location": 75, "Instructor / Organization": 300}
        self.treeview["columns"] = columns # set column names

        for c in columns:
            self.treeview.heading(c, text=c, anchor='w')
            self.treeview.column(c, width=sizes.get(c, 75), anchor='w')

    def update_table(self):

        # clear previous data
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # update table
        for _ , row in self.df_update.iterrows():
            self.treeview.insert('', 'end', values=row.tolist())

        # modify update text
        self.update_text.config(text=f'Last Update: {dt.datetime.today().strftime('%I:%M %p')}')

if __name__=="__main__":
    content = Content()
    content.root.mainloop()

