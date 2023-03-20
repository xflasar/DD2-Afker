# TODO:
# -Add exit method
# -Add a warning if there is an mini-boss in game
# -Add a warning and focus the window application if a Tower is damaged

import pyautogui
import pywinauto
from pywinauto.controls.hwndwrapper import HwndWrapper
import time
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Method for sending keystroke
def send_keystroke(app):
    app.send_keystrokes('G', with_spaces=False)

# Method for getting the applications
def get_applications():
    apps = pywinauto.Desktop(backend="win32").windows()
    return [app for app in apps if 'Dungeon Defenders 2' in app.window_text()]

def main():
    applications = get_applications()
    
    while True:
        for app in applications:
            # Get screenshot of application
            screenshot = pyautogui.screenshot(region=(app.rectangle().left, app.rectangle().top, app.rectangle().width(), app.rectangle().height()))

            # Convert screenshot to string
            text = pytesseract.image_to_string(screenshot)

            # Convert Screenshot to data
            data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
            text = data['text']

            if 'READY!' in text:
                send_keystroke(app)
                print(f'Successfully sent READY keystroke to {app.window_text()}')
            elif 'ON!' in text:
                send_keystroke(app)
                print(f'Successfully sent MOVE ON keystroke to {app.window_text()}')
            elif "Replay" in text:
                # Get the index of the word "Replay" in the text
                index = text.index("Replay")
                
                # Get the coordinates of the word from the data
                x = data['left'][index] + app.rectangle().left
                y = data['top'][index] + app.rectangle().top
                
                # Bring the application window into focus
                try: 
                    HwndWrapper(app).wrapper_object().set_focus()
                except Exception as e:
                    print(f"Error setting focus: {e}")
                
                # Move the mouse to the desired location and click
                pyautogui.moveTo(x, y)
                pyautogui.click()
                
                # Unfocus the application window (non-functional)!!
                pywinauto.keyboard.SendKeys('%')

                # Wait for user to press Enter to continue
                input("Once the deffences are set up press Enter!")

if __name__ == '__main__':
    print("DD2 Wave Auto-Afker Running!")
    main()