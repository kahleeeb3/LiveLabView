import pandas as pd
from datetime import datetime
# import tkinter as tk
# from tkinter import ttk



# class DataFrameDisplay:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Live Lab View")

#         # Initialize Treeview
#         self.tree = ttk.Treeview(root)
#         self.tree.pack(expand=True, fill='both')

#         # Schedule the first update
#         self.update_data()

#     def update_data(self):
#         # pull new data
#         df = format_data()
#         curr_time = get_curr_time()
#         df = get_matching_schedule(df, *curr_time)

#         # Clear existing Treeview content
#         for item in self.tree.get_children():
#             self.tree.delete(item)

#         # Define columns based on DataFrame
#         columns = df.columns.tolist()
#         self.tree["columns"] = columns
#         self.tree["show"] = "headings"

#         # Set up the column headings and widths
#         for col in columns:
#             self.tree.heading(col, text=col)
#             self.tree.column(col, width=100, anchor='center')

#         # Insert DataFrame data into the Treeview
#         for index, row in df.iterrows():
#             self.tree.insert('', 'end', values=row.tolist())

#          # Schedule next update
#         self.root.after(600000, self.update_data)  # Update every 5000 ms (5 seconds)

# if __name__=="__main__":
#     root = tk.Tk()
#     root.iconbitmap("icon.ico")
#     app = DataFrameDisplay(root)
#     root.mainloop()


def get_curr_classes(df, day, time):

    def get_time_str(cell):
        return datetime.strftime(cell, "%I:%M%p")
    
    today = df[df["Day"] == day]
    time = datetime.strptime(time, "%I:%M%p") # format the time

    active_class_truth_table = today.apply(lambda x: x["Start"] <= time <= x["End"], axis=1)
    active_class_index = today.index[active_class_truth_table]

    active_class = today.loc[active_class_index]

    active_class[["Start", "End"]] = active_class[["Start", "End"]].map(get_time_str) # convert 9:30p to 9:30PM

    return active_class

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

def load_csv():

    def format_time_str(cell):
        return cell.replace('p', 'PM').replace('a', 'AM')

    def format_instructor_str(cell):
        return cell.replace('\n', ', ')

    def get_time_obj(cell):
        return datetime.strptime(cell, "%I:%M%p")

    df = pd.read_csv('events.csv', usecols=['Name', 'Section', 'Title', 'Day Of Week', 'Location', 'Instructor / Organization', 'Published Start', 'Published End'])

    df = df.rename(columns={'Day Of Week':'Day', 'Instructor / Organization':'Instructor', 'Published Start': 'Start', 'Published End':'End'}) # rename columns
    
    df = df[df['Name'] != 'Not Available'] # Remove non available Courses
    
    df = df.astype(str) # convert to str
    day_order = ["M", "T", "W", "Th", "F"] # define day categories
    df['Day'] = pd.Categorical(df['Day'], categories=day_order, ordered=True) # make days categorical
    df = df.sort_values(by=['Name', 'Day']) # Sort by name and then day

    df[["Start", "End"]] = df[["Start", "End"]].map(format_time_str) # convert 9:30p to 9:30PM
    df[["Instructor"]] = df[["Instructor"]].map(format_instructor_str) # remove \n

    df.to_csv("events_formatted.csv", index=False) # export CSV for better readability

    df[["Start", "End"]] = df[["Start", "End"]].map(get_time_obj) # convert to time

    df.to_pickle("events.pkl")
    print("LOG: Pickle file created!")

    return df

def load_pkl():
    try:
        print("LOG: Loading pickle file...")
        df = pd.read_pickle("events.pkl")
        print("Pickle file loaded successfully!")
        return df
    except FileNotFoundError:
        print("ERROR: Pickle file not found. Attempting to create...")
        return load_csv()

df = load_pkl()

print(get_curr_classes(df, *get_curr_time()))


