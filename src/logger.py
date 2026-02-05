import cv2
import pytesseract
import re
from ultralytics import YOLO
import imgPaste

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

model = YOLO("runs/detect/train/weights/best.pt")

OCR_CONFIGS = {
    "wager": "--psm 6 -c tessedit_char_whitelist=$0123456789.",
    "payout": "--psm 6 -c tessedit_char_whitelist=$0123456789.",
    "odds": "--psm 6 -c tessedit_char_whitelist=+-0123456789"
}

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

def extract_features(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")

    results = model(img, conf=0.4)
    output = {}

    for r in results:
        boxes = sorted(r.boxes, key=lambda b: b.xyxy[0][1])  # top → bottom

        for box in boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            crop = img[y1:y2, x1:x2]

            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            gray = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY,
                11, 2
            )

            config = OCR_CONFIGS.get(label, "--psm 6")
            text = pytesseract.image_to_string(gray, config=config).strip()
            
            value = None
            if label == "odds":
                value = extract_odds(text)
            elif label in ("wager", "payout"):
                value = clean_money(text)
            else:
                value = text

            if value:
                output.setdefault(label, []).append(value)

    return output

print(extract_features("betslip.jpg"))
