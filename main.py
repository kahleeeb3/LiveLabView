import tkinter as tk
from tkinter import ttk
import tk_helper as tkh
import data
import datetime as dt
import pandas as pd

class Content:
    def __init__(self):

        self.root = tk.Tk()
        self.root.iconbitmap("icon.ico")
        self.root.title("LiveLabView")

        self.load_data()
        # self.create_file_menu()
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

    def create_file_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='Open')
        filemenu.add_command(label='Save')

    def create_window(self):
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
            "auto_update": tk.BooleanVar(value=1),
            "date_text" : tk.StringVar(),
            "time": tk.BooleanVar(value=1),
            "date": tk.BooleanVar(value=1),
            "room":tk.BooleanVar(value=0),
            "instructor":tk.BooleanVar(value=0)
        }

        # Filter Buttons
        auto_update_button = tk.Checkbutton(
            self.window.bottom_right_frame, text="Auto Update", background="White", variable=self.filter_vars["auto_update"], command=self.auto_update)
        date_label = tk.Label(self.window.bottom_right_frame, text='Date:')
        date_entry = tk.Entry(self.window.bottom_right_frame, textvariable=self.filter_vars["date_text"])
        update_button = tk.Button(self.window.bottom_right_frame, text='Update', command=self.on_update_button_press)
        time_button = tk.Checkbutton(self.window.bottom_right_frame, text="Time", background="White", variable=self.filter_vars["time"])
        date_button = tk.Checkbutton(self.window.bottom_right_frame, text="Date", background="White", variable=self.filter_vars["date"])
        room_button = tk.Checkbutton(self.window.bottom_right_frame, text="Room", background="White", variable=self.filter_vars["room"])
        instructor_button = tk.Checkbutton(self.window.bottom_right_frame, text="Instructor", background="White", variable=self.filter_vars["instructor"])

        # Filter Layout
        auto_update_button.grid(row=0, column=0, sticky="nsw")
        date_label.grid(row=0, column=1, sticky="nsw")
        date_entry.grid(row=0, column=2, sticky="nsw")
        time_button.grid(row=0, column=3, sticky="nsew")
        date_button.grid(row=0, column=4, sticky="nsew")
        room_button.grid(row=0, column=5, sticky="nsew")
        instructor_button.grid(row=0, column=6, sticky="nsew")
        update_button.grid(row=0, column=7, sticky="nsew")

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

        self.df_update = df
        self.update_table()

    def create_table(self):
        self.treeview = ttk.Treeview(self.window.bottom_right_frame, show="headings")
        self.treeview.grid(row=1, column=0, columnspan = 10,sticky="nsew")
        columns = self.df.columns.values.tolist()
        sizes = {"Name":95,"Title":160, "Start": 60, "End": 60, "Location": 75, "Instructor / Organization": 300}
        self.treeview["columns"] = columns # set column names

        for c in columns:
            self.treeview.heading(c, text=c, anchor='w', command=lambda _col=c: self.sort_by_column(_col))
            self.treeview.column(c, width=sizes.get(c, 75), anchor='w')

    def sort_by_column(self, column):
        self.df_update = self.df_update.sort_values(by=column, ascending=True)
        self.update_table()

    def update_table(self):

        # clear previous data
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # update table
        for _ , row in self.df_update.iterrows():
            self.treeview.insert('', 'end', values=row.tolist())

        # modify update text
        self.update_text.config(text=f'Last Update: {dt.datetime.today().strftime('%I:%M %p')}')

    def auto_update(self):
        auto_update = self.filter_vars["auto_update"].get()
        if(auto_update):   
            minutes = 10
            seconds = 0
            time_delay = (minutes*60000)+ (seconds * 1000)
            self.on_update_button_press()
            self.root.after(time_delay, self.auto_update)


if __name__=="__main__":
    content = Content()
    content.root.mainloop()