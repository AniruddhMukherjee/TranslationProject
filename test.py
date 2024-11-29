from PIL import Image
import pytesseract

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Test with a sample image
image = Image.open("test_image.png")  # Replace with an actual image path
text = pytesseract.image_to_string(image)
print(text)
