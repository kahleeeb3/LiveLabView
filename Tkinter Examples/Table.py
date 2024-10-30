import tkinter as tk
from tkinter import ttk

class Table:

    def __init__(self, master, df, row, column):

        # store table data
        self.df = df
        columns = df.columns.values.tolist()
        
        # create a table
        table = ttk.Treeview(master, show="headings", columns=columns)
        table.grid(row=row, column=column ,sticky="nsew")
        self.table = table

        # configure table to expand with master frame
        master.columnconfigure(column, weight=1) # expand horizontally
        master.rowconfigure(row, weight=1) # expand vertically
        
        # define headings
        for c in columns:
            table.heading(c, text=c, anchor='w', command=lambda _col=c: self.sort_by_column(_col))

        # define rows
        for _ , row in df.iterrows():
            table.insert('', tk.END, values=row.tolist())

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
    taxis = sns.load_dataset('taxis').head()

    root = tk.Tk()
    table = Table(root, df=taxis, row=0, column=0)
    root.mainloop()