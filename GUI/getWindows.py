import win32gui
import win32ui
import win32con
import win32api
import pyautogui
import pygetwindow as gw
import numpy as np
from keyInput import KeyPress

class WindowsHandler():
    def __init__(self):
        self.window_titles = gw.getAllTitles()

    def getAllTitles(self):
        self.window_titles = gw.getAllTitles()

    def showAllTitles(self):
        print("Show all window titles")
        for title in self.window_titles:
            if title != "" and title != None:
                print(title)

    '''
    def targetWindow(self, title):
        target_window = gw.getWindowsWithTitle(title)[0]
        window_x, window_y, window_width, window_height = target_window.left, target_window.top, target_window.width, target_window.height
        screenshot = pyautogui.screenshot(region=(window_x, window_y, window_width, window_height))
        return screenshot
    '''

    def background_screenshot(self, title):
        hwnd = win32gui.FindWindow(None, title)
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w, h = right - left, bot - top

        #hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)
        #win32api.SendMessage(hwndChild, win32con.WM_CHAR, ord('k'), 0)
        #KeyPress()
        #temp = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x4B, 0)
        #print(temp)
        #hwndEdit = win32gui.FindWindowEx(hwnd, hwndChild, "Edit", title)
        #win32api.PostMessage( hwndEdit, win32con.WM_CHAR, ord('k'), 0)
        win32api.PostMessage(hwnd, win32con.WM_CHAR, 0x4B, 0)
        print('k')
        
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img = np.reshape(img, (h, w, 4), order='C')[:,:,:3][:,:,::-1] #need to check
        #print(img.shape)

        

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        return img
    #print("input w")
    #pyautogui.press('w')
    #pyautogui.hotkey('ctrl', 'c')
    #time.sleep(2)
