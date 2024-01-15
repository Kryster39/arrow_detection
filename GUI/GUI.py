from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from getWindows import WindowsHandler

class autoTeachingBoard():
    def __init__(self):
        self.buildGUI()
        self.getGameWindows()
        self.root.mainloop()

    def buildGUI(self):
        self.root = tk.Tk()
        self.root.title("GUI")
        self.root.geometry("1280x780")

        # Windows control
        self.window = [tk.Label(self.root, text="視窗1st"),
                       tk.Label(self.root, text="視窗2nd"),
                       tk.Label(self.root, text="視窗3rd")]
        for i in range(3):
            self.window[i].grid(row=0, column=3*i, pady=10, columnspan=2)#, sticky='ew')

        self.enable_button = [tk.Button(self.root, text="啟用中", command=lambda: self.enable(0), fg="white", bg='green'),
                              tk.Button(self.root, text="已暫停", command=lambda: self.enable(1), fg="white", bg='red'),
                              tk.Button(self.root, text="已暫停", command=lambda: self.enable(2), fg="white", bg='red')]
        for i in range(3):
            self.enable_button[i].grid(row=0, column=3*i+2, pady=20)

        combobox_values = ["選項1", "選項2", "選項3", "選項4"]
        self.combobox = [ttk.Combobox(self.root, values=combobox_values),
                         ttk.Combobox(self.root, values=combobox_values),
                         ttk.Combobox(self.root, values=combobox_values)]
        for i in range(3):
            self.combobox[i].set("選擇一個選項")
            self.combobox[i].grid(row=1, column=3*i, columnspan=3, pady=10)
        #selected_item = self.combobox[th].get()
        #self.window[th].config(text=f"你選擇了: {selected_item}")
            
        self.check_button = [tk.Button(self.root, text="檢視", command=lambda: self.check(0)),
                             tk.Button(self.root, text="檢視", command=lambda: self.check(1)),
                             tk.Button(self.root, text="檢視", command=lambda: self.check(2))]
        for i in range(3):
            self.check_button[i].grid(row=2, column=3*i, columnspan=3)

        # Setting
        self.setting_button = tk.Button(self.root, text="設定", command=lambda: self.on_button_click(0))
        self.setting_button.grid(row=0, column=9, pady=20)

        self.refresh_button = tk.Button(self.root, text="重新偵測", command=lambda: self.refresh())
        self.refresh_button.grid(row=1, column=9, pady=20)

        # Demonstrate
        image_path = r"D:/github/arrow_detection/detection_model/source/0.png"
        image = Image.open(image_path)
        image_size_ratio = image.size[1]/image.size[0]
        self.image_size = (1000, int(1000*image_size_ratio))
        image = image.resize(self.image_size)
        self.image = ImageTk.PhotoImage(image)

        self.game_image = tk.Canvas(self.root, width=1000, height=int(1000*image_size_ratio))
        self.image_item = self.game_image.create_image(0, 0, anchor='nw')
        self.game_image.itemconfig(self.image_item, image=self.image)
        self.game_image.grid(row=3, column=0, pady=10, columnspan=9)

        # formatting
        for i in range(self.root.grid_size()[0]-1):
            self.root.grid_columnconfigure(i, weight=3)
        self.root.grid_columnconfigure(self.root.grid_size()[0]-1, weight=1)
        #self.root.mainloop()

    def getGameWindows(self):
        self.handler = WindowsHandler()
        self.refreshTitles()

    def enable(self, th=0):
        if self.enable_button[th]["text"] == "啟用中":
            self.enable_button[th].config(text="已暫停", bg="red")
        else:
            self.enable_button[th].config(text="啟用中", bg="green")
    
    def check(self, th=0):
        #screenshot = self.handler.targetWindow(self.combobox[th].get())
        screenshot = self.handler.background_screenshot(self.combobox[th].get())
        image = Image.fromarray(screenshot)
        #gray_image = color_image.convert('L')
        image = image.resize(self.image_size)
        self.image = ImageTk.PhotoImage(image)
        self.game_image.itemconfig(self.image_item, image=self.image)
        #check window image
    
    def refresh(self):
        self.handler.getAllTitles()
        self.refreshTitles()

    def refreshTitles(self):
        game_list = [*filter(lambda x: "九陰真經" in x or "9yin" in x, self.handler.window_titles)]
        for i in range(3):
            self.combobox[i].config(values=game_list)