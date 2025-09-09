from PIL import Image
import pytesseract

# Ensure pytesseract is properly configured to find Tesseract executable
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # Windows path; change accordingly for your OS

def parse_image(image_path):
    # Open the image file
    image = Image.open(image_path)
    
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(image)
    return text
