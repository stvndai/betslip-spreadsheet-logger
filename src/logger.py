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

OCR_CONFIGS = {
    "wager": "--psm 6 -c tessedit_char_whitelist=$0123456789.",
    "payout": "--psm 6 -c tessedit_char_whitelist=$0123456789.",
    "odds": "--psm 6 -c tessedit_char_whitelist=+-0123456789"
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
            
            # Identify field name
            field_name = LABELS.get(cls, "unknown")

            # Crop region for OCR
            crop = img[y1:y2, x1:x2]

            # Convert to grayscale
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

            # --- FIX 1: Use Adaptive Thresholding (Matches extract_features) ---
            gray = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY,
                11, 2
            )

            # --- FIX 2: Use Specific OCR Configs (Matches extract_features) ---
            # Default to --psm 6 if the field isn't in OCR_CONFIGS
            config = OCR_CONFIGS.get(field_name, "--psm 6")
            
            # Run OCR with the config
            text = pytesseract.image_to_string(gray, config=config)

            # Clean text based on field type
            if field_name == "odds":
                text = extract_odds(text)
            elif field_name in ("wager", "payout"):
                text = clean_money(text)
            else:
                text = clean_text_field(text) # Assuming you want basic cleaning here

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


def clean_money(text):
    text = text.replace(",", "").replace(" ", "")
    match = re.search(r"\$?\d+(\.\d{2})?", text)
    return match.group() if match else None

def extract_odds(text):
    text = (
        text.replace("–", "-")
            .replace("—", "-")
            .replace(" ", "")
    )
    match = re.search(r"[+-]\d{2,4}", text)
    return match.group() if match else None

