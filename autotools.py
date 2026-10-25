import time
import pyautogui


def auto_press_join(image="join_button.png", timeout=25, confidence=0.8):
    """Click the Join button once it appears. Pass resource_path("join_button.png")
    from main.py so it also works inside the built exe."""
    end = time.time() + timeout
    while time.time() < end:
        try:
            pos = pyautogui.locateCenterOnScreen(image, confidence=confidence)
        except pyautogui.ImageNotFoundException:
            pos = None
        if pos:
            pyautogui.click(pos)
            return True
        time.sleep(0.5)
    return False
