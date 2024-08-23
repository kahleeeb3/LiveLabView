import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk

def format_data():
    df = pd.read_excel('Schedule.xlsx', index_col=None, header=0, dtype=str)

    # format start time
    df["Published Start"] = df["Published Start"].apply(lambda x: x.replace('p', 'PM').replace('a', 'AM')) # convert 9:30p to 9:30PM
    df["Published Start"] = df["Published Start"].apply(lambda x: datetime.strptime(x, "%I:%M%p")) # convert 9:30PM to 09:30PM

    # format end time
    df["Published End"] = df["Published End"].apply(lambda x: x.replace('p', 'PM').replace('a', 'AM')) # convert 9:30p to 9:30PM
    df["Published End"] = df["Published End"].apply(lambda x: datetime.strptime(x, "%I:%M%p")) # convert 9:30PM to 09:30PM

    return df

def get_curr_time():
    curr_time = datetime.today()

    # get the day
    day = curr_time.strftime('%A')
    day_abbrv = {
        'Monday': 'M',
        'Tuesday': 'T',
        'Wednesday': 'W',
        'Thursday': 'Th',
        'Friday': 'F',
        'Saturday': 'S',
        'Sunday': 'Su'
    }
    day = day_abbrv[day]

    # get the time
    time = curr_time.strftime('%I:%M%p')

    return [day, time]

def get_matching_schedule(df, day, time):
    
    today = df[df["Day Of Week"] == day]
    time = datetime.strptime(time, "%I:%M%p") # format the time

    active_class_truth_table = today.apply(lambda x: x["Published Start"] <= time <= x["Published End"], axis=1)
    active_class_index = today.index[active_class_truth_table]

    active_class = today.loc[active_class_index]

    return active_class[["Location", "Name", "Title", "Instructor / Organization", "Section"]]

class DataFrameDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Lab View")

        # Initialize Treeview
        self.tree = ttk.Treeview(root)
        self.tree.pack(expand=True, fill='both')

        # Schedule the first update
        self.update_data()

    def update_data(self):
        # pull new data
        df = format_data()
        curr_time = get_curr_time()
        df = get_matching_schedule(df, *curr_time)

        # Clear existing Treeview content
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Define columns based on DataFrame
        columns = df.columns.tolist()
        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        # Set up the column headings and widths
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        # Insert DataFrame data into the Treeview
        for index, row in df.iterrows():
            self.tree.insert('', 'end', values=row.tolist())

         # Schedule next update
        self.root.after(600000, self.update_data)  # Update every 5000 ms (5 seconds)

if __name__=="__main__":
    root = tk.Tk()
    root.iconbitmap("icon.ico")
    app = DataFrameDisplay(root)
    root.mainloop()
