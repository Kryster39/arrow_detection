import win32gui
import win32ui
import win32con
import win32api
import pydirectinput
from pynput.keyboard import Key, Controller
import pygetwindow as gw
import numpy as np
import time
from keyInput import KeyPress
from keyInput3 import keydownup
import keyboard

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
        print(title)
        hwnd = win32gui.FindWindow(None, title)
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w, h = right - left, bot - top

        #hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        #time.sleep(3)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)
        keydownup(0x4B)
        #keypress('space')
        #time.sleep(1)
        #keypress('k')
        #kb=Controller()
        #kb.press(Key.space)
        #time.sleep(0.5)
        #kb.release(Key.space)
        #win32api.keybd_event(ord('k'), 0, 0, 0)
        #time.sleep(0.5)
        #win32api.keybd_event(ord('k'), 0, win32con.KEYEVENTF_KEYUP, 0)
        #pydirectinput.moveTo(40,40)
        #time.sleep(1)
        #pydirectinput.click()
        #time.sleep(1)
        #pydirectinput.keyDown('space')
        #time.sleep(0.5)
        #pydirectinput.keyUp('space')
        #time.sleep(0.5)
        #pydirectinput.keyDown('left')
        #time.sleep(1)
        #pydirectinput.keyUp('left')
        #win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, 0x4B, 0)
        #time.sleep(0.5)
        #win32api.SendMessage(hwnd, win32con.WM_KEYUP, 0x4B, 0)
        #KeyPress(0x41)
        #temp = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x4B, 0)
        #print(temp)
        #hwndEdit = win32gui.FindWindowEx(hwnd, hwndChild, "Edit", title)
        #win32api.PostMessage( hwndChild, win32con.WM_CHAR, ord('K'), 0)
        '''
        while True:
            ip = input()
            if ip == 'z':
                break
        '''
        '''
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
        '''
    #print("input w")
    #pyautogui.press('w')
    #pyautogui.hotkey('ctrl', 'c')
    #time.sleep(2)
def get_inner_windows(whndl):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            hwnds[win32gui.GetClassName(hwnd)] = hwnd
        return True
    hwnds = {}
    win32gui.EnumChildWindows(whndl, callback, hwnds)
    return hwnds