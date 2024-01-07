import tkinter as tk
from tkinter import ttk

class autoTeachingBoard():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI")
        self.root.geometry("1280x780")

        self.window = [tk.Label(self.root, text="視窗1st"),
                       tk.Label(self.root, text="視窗2nd"),
                       tk.Label(self.root, text="視窗3rd")]
        for i in range(3):
            self.window[i].grid(row=0, column=2*i, pady=10, columnspan=2)#, sticky='ew')

        self.button = [tk.Button(self.root, text="按鍵", command=lambda: self.on_button_click(0)),
                       tk.Button(self.root, text="按鍵", command=lambda: self.on_button_click(1)),
                       tk.Button(self.root, text="按鍵", command=lambda: self.on_button_click(2))]
        for i in range(3):
            self.button[i].grid(row=1, column=2*i, pady=20)

        combobox_values = ["選項1", "選項2", "選項3", "選項4"]
        self.combobox = [ttk.Combobox(self.root, values=combobox_values),
                         ttk.Combobox(self.root, values=combobox_values),
                         ttk.Combobox(self.root, values=combobox_values)]
        for i in range(3):
            self.combobox[i].set("選擇一個選項")
            self.combobox[i].grid(row=1, column=2*i+1, pady=10)

        self.setting = tk.Button(self.root, text="設定", command=lambda: self.on_button_click(0))
        self.setting.grid(row=0, column=6, pady=20)

        #for i in range(self.root.grid_size()[1]):
        #    self.root.grid_rowconfigure(i, weight=1)

        for i in range(self.root.grid_size()[0]-1):
            self.root.grid_columnconfigure(i, weight=3)
        self.root.grid_columnconfigure(self.root.grid_size()[0]-1, weight=1)
        self.root.mainloop()

    def on_button_click(self, th=0):
        selected_item = self.combobox[th].get()
        self.window[th].config(text=f"你選擇了: {selected_item}")
    

t = autoTeachingBoard()