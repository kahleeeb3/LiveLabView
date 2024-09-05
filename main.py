import tkinter as tk
from tkinter import ttk
from data import load_pkl, get_curr_time, get_curr_classes

class LiveLabView:
    def __init__(self, root):
        self.root = root
        self.get_all_classes() # assign data to self.classes
        self.get_curr_classes() # assign data to self.curr_classes
        self.create_table() # create the table headers & sizes
        self.update_table() # load data into table

    def get_all_classes(self):
        self.classes = load_pkl()

    def get_curr_classes(self):
        day, time = get_curr_time()
        self.curr_classes = get_curr_classes(self.classes, day, time)
    
    def create_table(self):
        self.treeview = ttk.Treeview(root, show="headings")
        self.treeview.pack(expand=True, fill='both')
        columns = self.curr_classes.columns.values.tolist()
        sizes = {"Name":75, "Section":75, "Title":160, "Start": 60, "End": 60, "Location": 75, "Instructor": 300}
        self.treeview["columns"] = columns # set column names

        for i, c in enumerate(columns):
            self.treeview.heading(c, text=c, anchor='w')
            self.treeview.column(c, width=sizes.get(c, 75), anchor='w')

    def update_table(self):

        self.get_curr_classes() # query new data

        # clear previous data
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # update table
        for _ , row in self.curr_classes.iterrows():
            self.treeview.insert('', 'end', values=row.tolist())

        self.root.after(600000, self.update_table) # update every 10 min

if __name__=="__main__":
    root = tk.Tk()
    app = LiveLabView(root)
    root.mainloop()
