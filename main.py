import tkinter as tk
from tkinter import ttk
import tk_helper as tkh
import data



if __name__=="__main__":

    # load in the data
    df = data.load_df("meetings.csv")
    instructors = data.get_instructors(df)
    locations = data.get_locations(df)
    # df_now = data.get_now(df)

    # create the tk app
    root = tk.Tk()
    window = tkh.Window(root)

    # define collapsable width
    collapsable_width = 40

    # define collapsible section for location filtering
    location_menu = tkh.Collapsable(master=window.bottom_left_frame, row=0, column=0, name="Locations", width=collapsable_width)
    location_scroll = tkh.ScrollFrame(location_menu.collapsed_content, width=25, height=100)

    for i, l in enumerate(locations):
        tk.Checkbutton(location_scroll.viewPort, text=l, background="White").grid(row=i, sticky=tk.W)

    location_scroll.pack(side="top", fill="both", expand=True)

    # define collapsible section for Instructor filtering
    instructor_menu = tkh.Collapsable(master=window.bottom_left_frame, row=1, column=0, name="Instructors", width=collapsable_width)
    instructor_scroll = tkh.ScrollFrame(instructor_menu.collapsed_content, width=25, height=100)

    for i, l in enumerate(instructors):
        tk.Checkbutton(instructor_scroll.viewPort, text=l, background="White").grid(row=i, sticky=tk.W)

    instructor_scroll.pack(side="top", fill="both", expand=True)

    # last update
    # update_text = tk.Label(window.top_frame, text='Last Update:')
    # update_text.grid(row=0, column=0, sticky="e")

    # define update button
    update_button = tk.Button(window.bottom_right_frame, text='Update')
    time_button = tk.Checkbutton(window.bottom_right_frame, text="Time", background="White") # filter for current time
    day_button = tk.Checkbutton(window.bottom_right_frame, text="Day", background="White") # filter for current day
    room_button = tk.Checkbutton(window.bottom_right_frame, text="Room", background="White") # filter by room
    instructor_button = tk.Checkbutton(window.bottom_right_frame, text="Instructor", background="White") # filter by instructor

    time_button.grid(row=0, column=0, sticky="ew")
    day_button.grid(row=0, column=1, sticky="ew")
    room_button.grid(row=0, column=2, sticky="ew")
    instructor_button.grid(row=0, column=3, sticky="ew")
    update_button.grid(row=0, column=4, sticky="ew")

    # create table

    """
    treeview = ttk.Treeview(window.bottom_right_frame, show="headings")
    treeview.grid(row=1, column=0, sticky="w")
    columns = df_now.columns.values.tolist()
    sizes = {"Name":75, "Section":75, "Title":160, "Start": 60, "End": 60, "Location": 75, "Instructor": 300}
    treeview["columns"] = columns # set column names

    for i, c in enumerate(columns):
        treeview.heading(c, text=c, anchor='w')
        treeview.column(c, width=sizes.get(c, 75), anchor='w')

    # update table
    for _ , row in df_now.iterrows():
        treeview.insert('', 'end', values=row.tolist())
    """
    
    root.mainloop()