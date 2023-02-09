import fitz
import cv2
import numpy as np

# PDF file path
pdf_path = "SP-A3-1-10.1R.pdf"

# Open the PDF file
pdf_doc = fitz.open(pdf_path)

# Get the first page of the PDF
page = pdf_doc[-1]

# Render the page to a pixmap
pix = page.get_pixmap()

# Convert the pixmap to a numpy array
img = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)

# Draw a rectangle on the image
cv2.rectangle(img, (161, 373), (241, 373), (255, 0, 0), 2)
cv2.rectangle(img, (161, 40), (241, 40), (255, 0, 0), 2)
n = 35
k = 9
size = 193
cv2.rectangle(img, (161, 40+size), (241, 40+size), (255, 0, 0), 2)


print(pix.h)
print(pix.w)

# Show the image with the rectangle using OpenCV
cv2.imshow("Preview", img)
cv2.waitKey(0)
cv2.destroyAllWindows()