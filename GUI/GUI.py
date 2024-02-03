from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from getWindows import WindowsHandler
import subprocess
import struct

class autoTeachingBoard():
    #############################################################
    #
    #   __init__
    #
    #############################################################
    def __init__(self):
        self.buildGUI()
        self.getGameWindows()
        self.root.mainloop()

    #############################################################
    #
    #   buildGUI:
    #       window:         window control place label
    #       enable_button:  check control place activate or not
    #       combobox:       show windows titles list
    #       check_button:   show screenshot about the windows in combobox
    #       game_image:     show screenshot
    #       setting_button: adjust detect detail
    #       refresh_button: redetect windows titles
    #       starting_button:start program
    #
    #############################################################
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

        self.enable_button_state = [tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()]
        self.enable_button_state[0].set(True)
        self.enable_button_state[1].set(False)
        self.enable_button_state[2].set(False)
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
        self.setting_button.grid(row=0, column=9, rowspan=2, pady=20)

        self.refresh_button = tk.Button(self.root, text="重新偵測", command=self.refresh)
        self.refresh_button.grid(row=1, column=9, rowspan=2, pady=20)
        
        # Starting
        self.start_button_state = tk.BooleanVar()
        self.start_button_state.set(False)
        self.start_button = tk.Button(self.root, text="開始", command=self.startDetect)
        self.start_button.grid(row=8, column=9, rowspan=2, columnspan=2, sticky='nsew', padx=20, pady=20)

        # Overlay (with starting button)
        self.overlay_visible = tk.BooleanVar()
        self.overlay_visible.set(False)
        self.transparent_image = Image.new("RGBA", (1280, 780), (0, 0, 0, 60))
        self.transparent_image = ImageTk.PhotoImage(self.transparent_image)
        self.overlay = tk.Canvas(self.root, width=780, height=1280)
        self.overlay.create_image(0, 0, anchor='nw', image=self.transparent_image)
        self.overlay.place_forget()

        # Demonstrate
        image_path = r"D:/github/arrow_detection/detection_model/source/0.png"
        image = Image.open(image_path)
        image_size_ratio = image.size[1]/image.size[0]
        self.image_size = (1000, int(1000*image_size_ratio))
        image = image.resize(self.image_size)
        self.image = ImageTk.PhotoImage(image)

        self.game_image = tk.Canvas(self.root, width=1000, height=int(1000*image_size_ratio))
        self.image_item = self.game_image.create_image(0, 0, anchor='nw', image=self.image)
        self.game_image.grid(row=3, column=0, pady=10, rowspan=7, columnspan=9)

        # formatting
        for i in range(self.root.grid_size()[0]):
            self.root.grid_columnconfigure(i, weight=1)
        #self.root.grid_columnconfigure(self.root.grid_size()[0]-1, weight=1)
        
    #############################################################
    #
    #   functions
    #
    #############################################################
    def getGameWindows(self):
        self.handler = WindowsHandler()
        self.refreshTitles()

    def enable(self, th=0):
        if self.enable_button_state[th].get():
            self.enable_button[th].config(text="已暫停", bg="red")
            self.enable_button_state[th].set(False)
        else:
            self.enable_button[th].config(text="啟用中", bg="green")
            self.enable_button_state[th].set(True)
    
    def check(self, th=0):
        #screenshot = self.handler.targetWindow(self.combobox[th].get())
        screenshot = self.handler.background_screenshot(self.combobox[th].get())
        '''
        image = Image.fromarray(screenshot)
        #gray_image = color_image.convert('L')
        image = image.resize(self.image_size)
        self.image = ImageTk.PhotoImage(image)
        self.game_image.itemconfig(self.image_item, image=self.image)
        #check window image
        '''

    def refresh(self):
        self.handler.getAllTitles()
        self.refreshTitles()

    def refreshTitles(self):
        game_list = [*filter(lambda x: "九陰真經" in x or "9yin" in x, self.handler.window_titles)]
        for i in range(3):
            self.combobox[i].config(values=game_list)

    def startOverlay(self):
        if self.overlay_visible.get():
            # disable overlay
            self.overlay.place_forget()  
        else:
            # show overlay
            self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)  
            #self.overlay.lift()
            self.start_button.lift()
        self.overlay_visible.set(not self.overlay_visible.get())
    
    def startKeypressMessage(self):
        self.top = tk.Toplevel(self.root)
        self.top.title("提示")
        self.top.geometry("320x180")
        
        label = tk.Label(self.top, text="按下任意鍵", font=32)
        label.grid(row=0, column=0, sticky='nsew')
        self.top.grid_columnconfigure(0, weight=1)
        self.top.grid_rowconfigure(0, weight=1)

    def startDetect(self):
        self.startOverlay()
        if self.start_button_state.get(): # false for not start
            self.start_button.config(text="開始")
            self.start_button_state.set(False)

        else:
            self.start_button.config(text="中斷")
            self.start_button_state.set(True)

            self.startKeypressMessage()
            program_path = 'Interception/HelloWorld.exe'

            array_to_send = [1, 2, 3, 4, 5]

            binary_data = struct.pack('i' * len(array_to_send), *array_to_send)

            process = subprocess.Popen([program_path], stdin=subprocess.PIPE)
            process.communicate(input=binary_data)
            process.wait()