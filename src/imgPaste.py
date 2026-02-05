from PIL import ImageGrab
import numpy as np
import cv2


def get_img_from_clipboard():
    """
    Docstring for get_img_from_clipboard
    
    This function uses the pillow library to grab the 
    image from the clipboard and convert it from PIL to openCV BGR.
    """
    img = ImageGrab.grabclipboard()
    
    if img in None:
        raise ValueError("Clipboard does not contain an image")
    
    # Convert PIL → OpenCV (BGR)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img