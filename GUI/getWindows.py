import pyautogui
import pygetwindow as gw
import time

class WindowsHandler():
    def getAllTitles(self):
        self.window_titles = gw.getAllTitles()

    def showAllTitles(self):
        print("Show all window titles")
        for title in self.window_titles:
            if title != "" and title != None:
                print(title)

    def targetWindow(self, title):
        target_window = gw.getWindowsWithTitle(title)[0]
        target_window.activate()

    #print("input w")
    #pyautogui.press('w')
    #pyautogui.hotkey('ctrl', 'c')
    #time.sleep(2)
window_titles = gw.getAllTitles()
tr = 0
for i,title in enumerate(window_titles):
    if "txt" in title:
        tr = i
        print(i, title)

#i = int(input())
#print(window_titles[i])

target_window = gw.getWindowsWithTitle(window_titles[tr])[0]
time.sleep(2)
target_window.activate()
time.sleep(2)
pyautogui.press('w')
#pyautogui.write(text_to_type)

time.sleep(2)
