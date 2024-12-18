
from PIL import Image
from paddleocr import PaddleOCR
import pytesseract
from io import BytesIO
import os


pytesseract.pytesseract.tesseract_cmd = r'C://Program Files//Tesseract-OCR//tesseract.exe'


os.environ["TESSDATA_PREFIX"] =  "C://Program Files//Tesseract-OCR//tessdata"
custom_config = r'-c preserve_interword_spaces=1'

# Initialize PaddleOCR with the specified language and other configurations
ocr = PaddleOCR(use_angle_cls=True, lang='en')

def paddle_ocr(image_bytes):
    # Perform OCR on the image
    result = ocr.ocr(image_bytes, cls=True)

    # Extract and concatenate recognized text
    text = ' '.join([word[1][0] for line in result for word in line])
    
    return text

def tesseract_ocr(image_bytes):
    img = Image.open(BytesIO(image_bytes))
    img = img.convert('L') 
    text = pytesseract.image_to_string(img)
    return text