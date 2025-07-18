import pyautogui
from tkinter import messagebox

def execute_command(command):
    if command == "thumbs up":
        pyautogui.press('volumeup')
        messagebox.showinfo("Gesture Command", "Volume Increased")
    elif command == "thumbs down":
        pyautogui.press('volumedown')
        messagebox.showinfo("Gesture Command", "Volume Decreased")
    elif command == "scroll down":
        pyautogui.scroll(-100)
        messagebox.showinfo("Gesture Command", "Scrolled Down")
    elif command == "scroll up":
        pyautogui.scroll(100)
        messagebox.showinfo("Gesture Command", "Scrolled Up")
    elif command == "open browser":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('chrome')
        pyautogui.press('enter')
        messagebox.showinfo("Voice Command", "Browser Opened")
    elif command == "mute":
        pyautogui.press('volumemute')
        messagebox.showinfo("Voice Command", "Volume Muted")
    elif command == "play pause":
        pyautogui.press('playpause')
        messagebox.showinfo("Voice Command", "Play/Pause Media")
    elif command == "next track":
        pyautogui.press('nexttrack')
        messagebox.showinfo("Voice Command", "Next Track")
    elif command == "previous track":
        pyautogui.press('prevtrack')
        messagebox.showinfo("Voice Command", "Previous Track")
    elif command == "take screenshot":
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        messagebox.showinfo("Voice Command", "Screenshot Saved")
    elif command == "lock screen":
        pyautogui.hotkey('win', 'l')
        messagebox.showinfo("Voice Command", "Screen Locked")
    elif command == "shutdown":
        pyautogui.hotkey('alt', 'f4')
        pyautogui.press('enter')
        messagebox.showinfo("Voice Command", "Shutting Down...")
    elif command == "open notepad":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('notepad')
        pyautogui.press('enter')
        messagebox.showinfo("Voice Command", "Notepad Opened")
    elif command == "close window":
        pyautogui.hotkey('alt', 'f4')
        messagebox.showinfo("Voice Command", "Window Closed")
    elif command == "minimise window":
        pyautogui.hotkey('win', 'down')
        messagebox.showinfo("Voice Command", "Window Minimized")
    elif command == "maximize window":
        pyautogui.hotkey('win', 'up')
        messagebox.showinfo("Voice Command", "Window Maximized")
    elif command == "open calculator":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('calc')
        pyautogui.press('enter')
        messagebox.showinfo("Voice Command", "Calculator Opened")
    elif command == "open task manager":
        pyautogui.hotkey('ctrl', 'shift', 'esc')
        messagebox.showinfo("Voice Command", "Task Manager Opened")
    elif command == "open file explorer":
        pyautogui.hotkey('win', 'e')
        messagebox.showinfo("Voice Command", "File Explorer Opened")
    elif command == "open settings":
        pyautogui.hotkey('win', 'i')
        messagebox.showinfo("Voice Command", "Settings Opened")
    elif command == "switch window":
        pyautogui.hotkey('alt', 'tab')
        messagebox.showinfo("Voice Command", "Switched Window")
    elif command == "open command prompt":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('cmd')
        pyautogui.press('enter')
        messagebox.showinfo("Voice Command", "Command Prompt Opened")
    elif command == "open control panel":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('control')
        pyautogui.press('enter')
        messagebox.showinfo("Voice Command", "Control Panel Opened")
    elif command == "refresh desktop":
        pyautogui.hotkey('f5')
        messagebox.showinfo("Voice Command", "Desktop Refreshed")
    elif command == "open downloads folder":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('%USERPROFILE%\\Downloads')
        pyautogui.press('enter')
        messagebox.showinfo("Voice Command", "Downloads Folder Opened")
    elif command == "open documents folder":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('%USERPROFILE%\\Documents')
        pyautogui.press('enter')
        messagebox.showinfo("Voice Command", "Documents Folder Opened")
    elif command == "open pictures folder":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('%USERPROFILE%\\Pictures')
        pyautogui.press('enter')
        messagebox.showinfo("Voice Command", "Pictures Folder Opened")
    else:
        messagebox.showinfo("Unknown Command", f"Command not recognized: {command}")