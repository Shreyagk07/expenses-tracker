import cv2
import pytesseract
from tkinter import Tk, filedialog
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def upload_and_convert():
    
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    img = cv2.imread(file_path)
    text = pytesseract.image_to_string(img)
    print("Extracted Text:")
    print(text)

upload_and_convert()


import cv2
import pytesseract

# Set the path for Tesseract (adjust this to your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Open the camera
cap = cv2.VideoCapture(0)

# Wait for a key press
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow('Press space to capture', frame)

    # Wait for the space key to be pressed
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()

# Convert captured image to text
text = pytesseract.image_to_string(frame)

print("Extracted Text:")
print(text)
