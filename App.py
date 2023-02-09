import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class App:
    def __init__(self, master):
        self.master = master
        master.title("Tabs App")

        self.tab_control = ttk.Notebook(master)

        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Tab 1')
        self.tab_control.add(self.tab2, text='Tab 2')

        self.tab_control.pack(expand=1, fill='both')

        self.label1 = tk.Label(self.tab1, text="Directory 1:")
        self.label1.pack()
        self.entry1 = tk.Entry(self.tab1, width=50)
        self.entry1.pack()
        self.browse_button1 = tk.Button(self.tab1, text="Browse", command=self.browse_dir1)
        self.browse_button1.pack()

        self.label2 = tk.Label(self.tab1, text="Directory 2:")
        self.label2.pack()
        self.entry2 = tk.Entry(self.tab1, width=50)
        self.entry2.pack()
        self.browse_button2 = tk.Button(self.tab1, text="Browse", command=self.browse_dir2)
        self.browse_button2.pack()

        self.selected_dirs = tk.Label(self.tab2, text="")
        self.selected_dirs.pack()

    def browse_dir1(self):
        dir1 = filedialog.askdirectory(initialdir = "/", title = "Select directory 1")
        self.entry1.delete(0, tk.END)
        self.entry1.insert(0, dir1)
        self.show_directories()

    def browse_dir2(self):
        dir2 = filedialog.askdirectory(initialdir = "/", title = "Select directory 2")
        self.entry2.delete(0, tk.END)
        self.entry2.insert(0, dir2)
        self.show_directories()

    def show_directories(self):
        directory1 = self.entry1.get()
        directory2 = self.entry2.get()
        self.selected_dirs.config(text=f"Directory 1: {directory1}\nDirectory 2: {directory2}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()



















