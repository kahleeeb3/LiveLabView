from data import load_pkl, get_curr_classes, get_curr_time


from tkinter import Tk, Entry, END


class LiveLabView:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Lab View")
        self.load_classes()
        self.table_init()

    def load_classes(self):
        self.classes = load_pkl()

    def update_curr_classes(self):
        day, time = get_curr_time()
        curr_classes = get_curr_classes(self.classes, day, time)
        self.df = curr_classes

    def table_init(self):
        self.update_curr_classes()

        # update headers
        headers = self.df.columns.values.tolist()
        for i, h in enumerate(headers):
            self.e = Entry(self.root)
            self.e.grid(row=0, column=i)
            self.e.insert(END, h)

        self.table_update()

    def table_update(self):
        n_rows = len(self.df)

        for i in range(n_rows):
            row = self.df.iloc[i].values.tolist()
            for j, r in enumerate(row):
                self.e = Entry(self.root)
                self.e.grid(row=i+1, column=j)
                self.e.insert(END, r)


def main():
    root = Tk()
    app = LiveLabView(root)
    root.iconbitmap("icon.ico")
    root.mainloop()


if __name__ == "__main__":
    main()
