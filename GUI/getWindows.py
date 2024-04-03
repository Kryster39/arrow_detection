import win32gui
import win32ui
import win32con
import win32com.client
import pygetwindow as gw
import numpy as np

class WindowsHandler():
    def __init__(self, keyword):
        self.keyword = keyword
        self.window_title_hwnd = {}

    def getAllTitles(self):
        titles = gw.getAllTitles()
        self.window_title_hwnd = {}
        for title in titles:
            for kw in self.keyword:
                if kw in title:
                    prev_title = ""
                    orgi_title = title
                    while(title in self.window_title_hwnd.keys()):
                        prev_title = title
                        title = title+"#"
                    if prev_title == "":
                        hwnd = win32gui.FindWindowEx(0, 0, None, orgi_title)
                    else:
                        hwnd = win32gui.FindWindowEx(0, self.window_title_hwnd[prev_title], None, orgi_title)
                    self.window_title_hwnd[title] = hwnd
                    break
            
    def showAllTitles(self):
        print("Show all window titles")
        for title in self.window_title_hwnd.keys():
            if title != "" and title != None:
                print(title)

    def findWindow(self, title):
        num = 0
        print(title)
        while(title[-1]=='#'):
            num += 1
            title = title[:-1]
        
        hwnd = 0
        for i in range(num):
            hwnd = win32gui.FindWindowEx(0, hwnd, None, title)
            print(hwnd)
            if hwnd == 0:
                break
        return hwnd

    def background_screenshot(self, title):
        hwnd = self.window_title_hwnd[title]
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w, h = right - left, bot - top
        
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img = np.reshape(img, (h, w, 4), order='C')[:,:,:3][:,:,::-1]

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        return img

    def set_foreground(self, title):
        hwnd = self.window_title_hwnd[title]
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
        