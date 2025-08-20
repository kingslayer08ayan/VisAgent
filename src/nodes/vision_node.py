from typing import Dict, Optional
from PIL import Image
from transformers import pipeline
import pytesseract
from io import BytesIO
from src.utils.logging import get_logger

logger = get_logger("Vision")

class Vision:
    def __init__(self):
        # BLIP captioning is light enough for 3050
        self.pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

    def caption(self, image_bytes: bytes) -> str:
        try:
            img = Image.open(BytesIO(image_bytes)).convert("RGB")
            out = self.pipe(img)
            if isinstance(out, list) and len(out) and "generated_text" in out[0]:
                return out[0]["generated_text"]
        except Exception as e:
            logger.warning(f"Caption failed: {e}")
        # OCR fallback
        try:
            img = Image.open(BytesIO(image_bytes))
            return pytesseract.image_to_string(img)
        except Exception as e:
            logger.warning(f"OCR failed: {e}")
            return ""

def vision_node(state: Dict, vision: Vision):
    b = state.get("image_bytes")
    if not b:
        return state
    cap = vision.caption(b)
    state["vision_caption"] = cap
    return state
