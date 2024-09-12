import tkinter as tk
from tkinter import ttk
import tk_helper as tkh
import data


if __name__=="__main__":

    # load in the data
    df = data.load_df("meetings.csv")
    df_now = data.get_now(df)

    # create the tk app
    root = tk.Tk()
    window = tkh.Window(root)

    # define collapsible section
    location_menu = tkh.Collapsable(master=window.bottom_left_frame, row=0, column=0, name="Location", width=13)

    scrollFrame = tkh.ScrollFrame(location_menu.collapsed_content, width=25, height=222)

    locations = sorted(df_now["Location"].unique())
    for i, l in enumerate(locations):
        tk.Checkbutton(scrollFrame.viewPort, text=l).grid(row=i, sticky=tk.W)
        pass

    scrollFrame.pack(side="top", fill="both", expand=True)

    # last update
    update_text = tk.Label(window.top_frame, text='Last Update:')
    update_text.grid(row=0, column=0, sticky="e")

    # define update button
    button = tk.Button(window.bottom_right_frame, text='Update', width=25)
    button.grid(row=0, column=0, sticky="e")

    # create table
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
    
    root.mainloop()