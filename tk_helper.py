import tkinter as tk
import tkinter as tk
import platform


class ScrollFrame(tk.Frame):
    """
    taken from: 
    https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01
    """
    def __init__(self, parent, width=25, height=25):
        super().__init__(parent) # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff", width=width, height=height)          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the canvas frame changes.
            
        self.viewPort.bind('<Enter>', self.onEnter)                                 # bind wheel events when the cursor enters the control
        self.viewPort.bind('<Leave>', self.onLeave)                                 # unbind wheel events when the cursorl leaves the control

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

    def onLeave(self, event):                                                       # unbind wheel events when the cursorl leaves the control
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")

class Collapsable():
    def __init__(self, master, row, column, name, width):

        self.body = tk.Frame(master, bg='purple', width=25, height=50)
        self.body.grid(row=row, column=column, sticky="nsew")

        self.width = width
        self.name = name
        self.create_button_frame()
        self.create_collapsed_content_frame()

    def create_collapsed_content_frame(self):
        self.collapsed_content = tk.Frame(self.body, bg='cyan', width=25, height=25)
        self.collapsed_content.grid(row=1, column=0, sticky="nsew")

    def create_button_frame(self):
        self.button_frame = tk.Frame(self.body, bg='grey', width=25, height=25)
        self.button_frame.grid(row=0, column=0, sticky="nsew")

        self.button = tk.Button(self.button_frame, text=f'{self.name} \u25BC', width=self.width, command=self.collapse)
        self.button.grid(row=0, sticky="nsew")        

    def collapse(self):
        if self.collapsed_content.winfo_ismapped():
            self.collapsed_content.grid_remove()
            self.button.config(text=f'{self.name} \u25B6') 
        else:
            self.collapsed_content.grid()
            self.button.config(text=f'{self.name} \u25BC')

class Window:
    def __init__(self, root):
        self.root = root
        self.create_top_frame()
        self.create_bottom_frame()
        self.create_bottom_left_frame()
        self.create_bottom_right_frame()

    def create_top_frame(self):
        self.top_frame = tk.Frame(self.root, bg='red', width=50, height=25)
        self.top_frame.grid(row=0, sticky="nsew")
        self.top_frame.grid_columnconfigure(0, weight=1)

    def create_bottom_frame(self):
        self.bottom_frame = tk.Frame(self.root, bg='green', width=50, height=25)
        self.bottom_frame.grid(row=1, sticky="nsew")
    
    def create_bottom_left_frame(self):
        self.bottom_left_frame = tk.Frame(self.bottom_frame, bg='blue', width=20, height=190)
        self.bottom_left_frame.grid(row=0, column=0, sticky="nsew")

    def create_bottom_right_frame(self):
        self.bottom_right_frame = tk.Frame(self.bottom_frame, bg='yellow', width=250, height=190)
        self.bottom_right_frame.grid(row=0, column=1, sticky="nsew")
        self.bottom_right_frame.grid_columnconfigure(0, weight=1)