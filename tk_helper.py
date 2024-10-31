import tkinter as tk
from tkinter import ttk
import platform

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

class ScrollFrame(tk.Frame):
    """
    taken from: 
    https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01
    """
    def __init__(self, parent, width=0, height=0):
        super().__init__(parent) # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="white", width=width, height=height)          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, background="white")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the canvas frame changes.
            
        self.viewPort.bind('<Enter>', self.onEnter)                                 # bind wheel events when the cursor enters the control
        self.viewPort.bind('<Leave>', self.onLeave)                                 # unbind wheel events when the cursor leaves the control

        self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.

    def onMouseWheel(self, event):                                                  # cross platform scroll wheel event
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll( -1, "units" )
            elif event.num == 5:
                self.canvas.yview_scroll( 1, "units" )
    
    def onEnter(self, event):                                                       # bind wheel events when the cursor enters the control
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, event):                                                       # unbind wheel events when the cursor leaves the control
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")

class Collapsible():
    def __init__(self, master, row, column, name, width):

        self.body = tk.Frame(master, bg='white', width=width)
        self.body.grid(row=row, column=column, sticky="nsew")
        tk.Grid.rowconfigure(master, row, weight=1)
        
        self.master = master
        self.row = row
        self.width = width
        self.name = name
        self.create_button_frame()
        self.create_collapsed_content_frame()

    def create_button_frame(self):
        self.button_frame = tk.Frame(self.body, bg='white', width=25, height=25)
        self.button_frame.grid(row=0, column=0, sticky="nsew")

        self.button = tk.Button(self.button_frame, text=f'{self.name} \u25BC', width=self.width, command=self.collapse)
        self.button.grid(row=0, sticky="nsew")

    def create_collapsed_content_frame(self):
        self.collapsed_content = tk.Frame(self.body, bg='white')
        self.collapsed_content.grid(row=1, column=0, sticky="nsew")
        tk.Grid.rowconfigure(self.body, 1, weight=1)

    def collapse(self):
        if self.collapsed_content.winfo_ismapped():
            self.collapsed_content.grid_remove()
            self.button.config(text=f'{self.name} \u25B6')
            tk.Grid.rowconfigure(self.master, self.row, weight=0)
        else:
            self.collapsed_content.grid()
            self.button.config(text=f'{self.name} \u25BC')
            tk.Grid.rowconfigure(self.master, self.row, weight=1)

class Window:
    def __init__(self, root):
        self.root = root
        self.create_top_frame()
        self.create_left_frame()
        self.create_bottom_left_frame()
        self.create_bottom_right_frame()
        self.create_bottom_frame()

    def create_top_frame(self):
        top_frame = tk.Frame(self.root, bg='light grey', height=10)
        top_frame.grid(row=0, sticky="nsew", columnspan=3)
        self.root.columnconfigure(1, weight=1)
        self.top_frame = top_frame

    def create_left_frame(self):
        left_frame = tk.Frame(self.root, bg='white', width=10)
        left_frame.grid(row=1, column=0, sticky="nsew", rowspan=2)
        self.root.rowconfigure(2, weight=1)
        self.left_frame = left_frame
    
    def create_bottom_left_frame(self):
        bottom_left_frame = tk.Frame(self.root, bg='white', height=10)
        bottom_left_frame.grid(row=1, column=1, sticky="nsew")
        self.bottom_left_frame = bottom_left_frame

    def create_bottom_right_frame(self):
        bottom_right_frame = tk.Frame(self.root, bg='white', height=10)
        bottom_right_frame.grid(row=1, column=2, sticky="nsew")
        self.root.columnconfigure(2, weight=1)
        self.bottom_right_frame = bottom_right_frame

    def create_bottom_frame(self):
        bottom_frame = tk.Frame(self.root, bg='white', width=50, height=25)
        bottom_frame.grid(row=2, column=1, sticky="nsew", columnspan=2)
        self.bottom_frame = bottom_frame