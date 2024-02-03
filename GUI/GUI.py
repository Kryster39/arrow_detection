from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from GUI.getWindows import WindowsHandler
import subprocess
import threading
import random
import time
import numpy as np
import cv2

num2word = {0:'n', 1:'w', 2:'s', 3:'a', 4:'d', 5:'j', 6:'k'}

def detectArrow(model, image, code=True):
    pred = np.array(image.convert('L'))[np.newaxis,:,:,np.newaxis]
    pred = model.predict(pred)
    pred = np.reshape(pred, (192, 704, 7))
    if np.sum(pred) < 400:
        return 0
    pred = np.argmax(pred, axis=-1)

    arrow_list = []
    for i in range(6):
        zero = np.zeros_like(pred, np.uint8)
        zero[pred==i+1] = 1
        contours, _ = cv2.findContours(zero, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 400:
                continue
            (x,y), r = cv2.minEnclosingCircle(contour)
            arrow_list.append((x, i+1))

    if arrow_list == []:
        return 0
    
    arrow_list = [ y[1] for y in sorted(arrow_list, key=lambda x: x[0]) ]
    if code: # return key code
        return arrow_list
    else: #return key word
        word = ""
        for al in arrow_list:
            word += num2word[al]
        return word

def keyPressMessageGenerater(key_list):
    bp_flag = False
    if len(key_list) == 0:
        return 0
    msg = " "
    inter_key_time = " "
    outer_key_time = " "

    msg += str(key_list[0])
    inter_key_time += str(random.randint(10,30))
    outer_key_time += str(random.randint(530, 980))
    for k in key_list[1:]:
        msg += " " + str(k)
        inter_key_time += " " + str(random.randint(10,30))

        if bp_flag and k < 5: 
            outer_key_time += " " + str(random.randint(320, 710))
            bp_flag = False
        else:
            outer_key_time += " " + str(random.randint(150, 350))

        if k >=5:
            bp_flag = True
    
    return str(len(key_list)) + msg + inter_key_time + outer_key_time + "\n"

class autoTeachingBoard():
    #############################################################
    #
    #   __init__
    #
    #############################################################
    def __init__(self, model):
        self.model = model
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
        self.setting_button.grid(row=0, column=9, sticky='ew', pady=20)

        self.refresh_button = tk.Button(self.root, text="重新偵測", command=self.refresh)
        self.refresh_button.grid(row=1, column=9, sticky='ew', pady=20)
        
        self.test_flag = tk.BooleanVar()
        self.test_flag.set(False)
        self.test_button = tk.Button(self.root, text="運行測試", command=self.testBoard)
        self.test_button.grid(row=2, column=9, sticky='ew', pady=20)
        
        # Starting
        self.start_button_state = tk.BooleanVar()
        self.start_button_state.set(False)
        self.start_button = tk.Button(self.root, text="開始", command=self.start, bg="lightgreen")
        self.start_button.grid(row=8, column=9, rowspan=2, columnspan=2,
                               sticky='nsew', padx=20, pady=20)
        self.exit_flag = False
        self.keypress_lock = threading.Lock()

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
        self.handler = WindowsHandler(["九陰真經", "9yin"])
        self.refresh()

    def enable(self, th=0):
        if self.enable_button_state[th].get():
            self.enable_button[th].config(text="已暫停", bg="red")
            self.enable_button_state[th].set(False)
        else:
            self.enable_button[th].config(text="啟用中", bg="green")
            self.enable_button_state[th].set(True)
    
    def check(self, th=0):
        screenshot = self.handler.background_screenshot(self.combobox[th].get())
        
        image = Image.fromarray(screenshot)
        image = image.resize(self.image_size)
        self.image = ImageTk.PhotoImage(image)
        self.game_image.itemconfig(self.image_item, image=self.image)

    def refresh(self):
        self.handler.getAllTitles()
        #game_list = self.handler.window_titles
        game_list = list(self.handler.window_title_hwnd.keys())
        for i in range(3):
            self.combobox[i].config(values=game_list)

    def testDetect(self, th, image, item, pred):
        while(self.test_flag.get()):
            screenshot = self.handler.background_screenshot(self.combobox[th].get())
            
            img = Image.fromarray(screenshot)
            img = img.resize((1920, 1080))
            img = img.crop((610,700,1314,892))
            
            arrow_list = detectArrow(self.model, img, code=False)

            img = ImageTk.PhotoImage(img)#[700:892, 610:1314]
            if not self.test_flag.get():
                break

            if arrow_list == 0:
                image.itemconfig(item, image=img)
            else:
                image.itemconfig(item, image=img)
                pred.config(text=arrow_list)
                
            time.sleep(2)

    def testBoard(self):
        self.test_flag.set(True)
        enable_window = []
        title = "測試 ("
        for i in range(3):
            if self.enable_button_state[i].get():
                enable_window.append(i)
                title += str(i+1)+" "
        title += "已啟用)"
        
        self.test_place = tk.Toplevel(self.root)
        self.test_place.title(title)
        self.test_place.geometry("1200x650") #6 * 3
        def on_closing():
            self.test_flag.set(False)
            self.test_place.destroy()
        self.test_place.protocol("WM_DELETE_WINDOW", on_closing)
        
        num_label = []
        num_image = []
        image_item = []
        num_pred  = []
        for i in range(3):
            num_label.append(tk.Label(self.test_place, text=str(i+1), font=16))
            num_label[i].grid(row=i, column=0, padx=20, sticky='nsew')

            num_image.append(tk.Canvas(self.test_place, width=700, height=200))
            image_item.append(num_image[i].create_image(0, 0, anchor='nw'))
            num_image[i].grid(row=i, column=1, pady=10, columnspan=3)

            num_pred.append(tk.Label(self.test_place, text="nan", font=32))
            num_pred[i].grid(row=i, column=4, sticky='nsew', columnspan=2)
        
            if i in enable_window:
                command_thread = threading.Thread(target=self.testDetect, 
                                                  args=(i, num_image[i], image_item[i], num_pred[i]))
                command_thread.start()

    def startOverlay(self):
        if self.overlay_visible.get():
            # disable overlay
            self.overlay.place_forget()  
        else:
            # show overlay
            self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)  
            self.start_button.lift()
        self.overlay_visible.set(not self.overlay_visible.get())
    
    def startKeypressMessage(self):
        self.keypress_message = tk.Toplevel(self.root)
        self.keypress_message.title("提示")
        self.keypress_message.geometry("320x180")
        
        label = tk.Label(self.keypress_message, text="按下任意鍵", font=32)
        label.grid(row=0, column=0, sticky='nsew')
        self.keypress_message.grid_columnconfigure(0, weight=1)
        self.keypress_message.grid_rowconfigure(0, weight=1)

    def startDetect(self, th, process):
        time.sleep(1)
        while(not self.exit_flag):
            screenshot = self.handler.background_screenshot(self.combobox[th].get())
            
            img = Image.fromarray(screenshot)
            img = img.resize((1920, 1080))
            img = img.crop((610,700,1314,892))
            arrow_list = detectArrow(self.model, img, code=True)
            if arrow_list != 0:
                msg = keyPressMessageGenerater(arrow_list)

                self.keypress_lock.acquire()
                if self.exit_flag:
                    self.keypress_lock.release()
                    break

                self.handler.set_foreground(self.combobox[th].get())
                process.stdin.write(msg)
                process.stdin.flush()

                line = process.stdout.readline()
                if "failed" in line:
                    break
                self.keypress_lock.release()
                time.sleep(15)

            time.sleep(0.6)

    def keypressFunction(self):
        enable_window = []
        for i in range(3):
            if self.enable_button_state[i].get():
                enable_window.append(i)

        program_path = 'Interception/keyPress.exe'
        process = subprocess.Popen([program_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        
        line = process.stdout.readline() #console application
        self.keypress_message.destroy()
        if "failed" in line:
            process.terminate()
            process.wait()
            return 0
        
        for i in enable_window:
            command_thread = threading.Thread(target=self.startDetect, 
                                                args=(i, process))
            command_thread.start()

        while(True):
            if self.exit_flag:
                process.terminate()
                process.wait()
                break
            time.sleep(2)

    '''
    def keypressFunction(self):
        program_path = 'Interception/keyPress.exe'
        process = subprocess.Popen([program_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        
        if self.exit_flag:
            process.terminate()
            process.wait()
            return 0

        line = process.stdout.readline()
        print(line)

        self.keypress_message.destroy()

        process.stdin.write(f"1 2 3 4 5 0\n")
        process.stdin.flush()

        line = process.stdout.readline()
        print(line)  
    '''
    def start(self):
        self.startOverlay()
        if self.start_button_state.get(): # false for not start
            self.exit_flag = True
            self.start_button.config(text="開始", bg="lightgreen")
            self.start_button_state.set(False)

        else:
            self.exit_flag = False
            self.start_button.config(text="中斷", bg="lightpink")
            self.start_button_state.set(True)

            self.startKeypressMessage()
            self.command_thread = threading.Thread(target=self.keypressFunction)
            self.command_thread.start()
    