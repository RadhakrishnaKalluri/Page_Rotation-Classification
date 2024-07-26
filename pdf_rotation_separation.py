'A  Python function for page rotation and Classification '

import fitz
from PIL import Image
import numpy as np
import pytesseract
import cv2
import matplotlib.pyplot as plt

show_plots = 0 # 0='ON',1='OFF'

def detect_page_rotation_and_classify(pdf_path):
    doc = fitz.open(pdf_path)
    rotations = {}
    classifications = {}
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image = np.array(img)
        
        # To convert to grayscale image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Threshold to create a binary image
        binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        edges = cv2.Canny(binary, 50, 150, apertureSize=3) # Detect edges using Canny
        
        # Detect lines using Hough Transform
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        
        # Calculate angles from detected lines
        angles = []
        if lines is not None:
            for rho, theta in lines[:, 0]:
                angle = np.degrees(theta) - 90
                if angle < -45:
                    angle = -(90 + angle)
                else:
                    angle = -angle
                angles.append(angle)
        
        # Calculate the median angle
        if angles:
            angle = np.median(angles)
        else:
            angle = 0
        
        if show_plots == 1:
            fig, axs = plt.subplots(1, 3, figsize=(15, 5))
            fig.suptitle(f'Page {page_num + 1}')
            
            axs[0].imshow(image)
            axs[0].set_title('Original Image')
            axs[0].axis('off')
            
            axs[1].imshow(binary, cmap='gray')
            axs[1].set_title('Binary Image')
            axs[1].axis('off')
            
            axs[2].imshow(edges, cmap='gray')
            if lines is not None:
                for rho, theta in lines[:, 0]:
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    x1 = int(x0 + 1000 * (-b))
                    y1 = int(y0 + 1000 * (a))
                    x2 = int(x0 - 1000 * (-b))
                    y2 = int(y0 - 1000 * (a))
                    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            axs[2].imshow(image)
            axs[2].set_title('Detected Lines')
            axs[2].axis('off')  
            plt.show()
        
        # TO store the rotation angle
        rotations[page_num + 1] = angle
        
        # page classification by text extraction
        text = page.get_text()
        #print(text)
        if text.strip():
            classifications[page_num + 1] = 'Machine-readable PDF'
        else:
            # Use OCR to detect text
            ocr_text = pytesseract.image_to_string(img)
            if ocr_text.strip():
                classifications[page_num + 1] = 'Image-based PDF which may be OCR'
            else:
                classifications[page_num + 1] = 'Image-based PDF which may not be OCR'
                
    return rotations, classifications 

#_____________________________________________________________________________

pdf_path = r"input.pdf"
rotations, classifications = detect_page_rotation_and_classify(pdf_path)
print("Rotations:", rotations)
print('\n',100*'_','\n')
print("Classifications:", classifications)


