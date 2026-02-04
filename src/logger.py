import cv2
import numpy as np
import pytesseract
from ultralytics import YOLO
from PIL import Image
import re

# Set Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load YOLO ONCE
model = YOLO("runs/detect/train/weights/best.pt")

# Map class IDs to field names (update according to your model)
LABELS = {
    0: "game",
    1: "odds",
    2: "wager",
    3: "payout"
}


def runDetection(image, conf=0.4):
    """
    image: PIL.Image OR image path (str)
    returns: list of dicts with box + OCR text (cleaned)
    """
    # --- Load image ---
    if isinstance(image, str):
        img = cv2.imread(image)
        if img is None:
            raise ValueError("Image path invalid")
    elif isinstance(image, Image.Image):
        img = pilToCv(image)
    else:
        raise TypeError("image must be PIL.Image or file path")

    # --- Run YOLO ---
    results = model(img, conf=conf, iou=0.5)
    extracted = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf_score = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Crop region for OCR
            crop = img[y1:y2, x1:x2]

            # Convert to grayscale + threshold for OCR
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            gray = cv2.threshold(
                gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )[1]

            # Run OCR
            text = pytesseract.image_to_string(gray, config="--psm 6")

            # Clean text based on field type
            field_name = LABELS.get(cls, "unknown")
            if field_name in ("odds", "wager", "payout"):
                text = clean_numeric_field(text)
            else:
                text = clean_text_field(text)

            extracted.append({
                "class_id": cls,
                "field": field_name,
                "confidence": conf_score,
                "bbox": (x1, y1, x2, y2),
                "text": text
            })


    return extracted 


def pilToCv(img):
    # Force RGB
    if img.mode != "RGB":
        img = img.convert("RGB")
    # Convert to OpenCV BGR
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def clean_text_field(text):
    """
    Removes newlines and extra spaces, keeps words intact
    """
    text = text.replace("\x0c", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_numeric_field(text):
    """
    Keeps +, -, $, digits, decimals
    Removes newlines and spaces
    Handles symbols separated by spaces from numbers
    """
    text = text.replace("\x0c", "").replace("\n", "")

    # Match optional +, -, $ (possibly separated by spaces) followed by number
    # e.g. " +120", " -120", "$ 10.00"
    matches = re.findall(r"[+\-$]?\s*\d+(?:\.\d+)?", text)

    # Remove any internal spaces between symbol and number
    cleaned = "".join(m.replace(" ", "") for m in matches)
    return cleaned

