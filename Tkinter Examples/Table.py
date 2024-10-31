import tkinter as tk
from tkinter import ttk

class Table:

    def __init__(self, master, df, row, column):

        # store table data
        self.df = df
        columns = df.columns.values.tolist()
        
        # create a table
        self.table = ttk.Treeview(master, show="headings", columns=columns)
        self.table.grid(row=row, column=column ,sticky="nsew")

        # configure table to expand with master frame
        master.columnconfigure(column, weight=1) # expand horizontally
        master.rowconfigure(row, weight=1) # expand vertically
        
        # define headings
        for c in columns:
            self.table.heading(c, text=c, anchor='w', command=lambda _col=c: self.sort_by_column(_col))

        # define rows
        for _ , row in df.iterrows():
            self.table.insert('', tk.END, values=row.tolist())

        # Bind resize event to adjust columns
        master.bind("<Configure>", self.adjust_column_widths)

    def adjust_column_widths(self, event):
        # Get the available width for the table
        total_width = event.width
        num_columns = len(self.df.columns)
        
        # Set each column width as a proportion of the total width
        if num_columns > 0:
            column_width = total_width // num_columns
            for c in self.df.columns:
                self.table.column(c, width=column_width)

    def sort_by_column(self, column):
        self.df = self.df.sort_values(by=column, ascending=True)
        self.update_table()

    def update_table(self):
        # clear previous data
        for child in self.table.get_children():
            self.table.delete(child)

        # update table
        for _ , row in self.df.iterrows():
            self.table.insert('', 'end', values=row.tolist())


if __name__=="__main__":
    
    # some example dataset
    import seaborn as sns
    taxis = sns.load_dataset('taxis').head(11)

    root = tk.Tk()
    root.geometry("1200x400")
    table = Table(root, df=taxis, row=0, column=0)
    root.mainloop()