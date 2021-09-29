print("""\n\n
                                                                                                                                                                                     
     / /                                                             //   ) )                                 //    ) )                                                              
    / /        ( )  ___      ___       __      ___      ___         //___/ / //  ___    __  ___  ___         //    / /  ___    __  ___  ___      ___    __  ___ ( )  ___       __    
   / /        / / //   ) ) //___) ) //   ) ) ((   ) ) //___) )     / ____ / // //   ) )  / /   //___) )     //    / / //___) )  / /   //___) ) //   ) )  / /   / / //   ) ) //   ) ) 
  / /        / / //       //       //   / /   \ \    //           //       // //   / /  / /   //           //    / / //        / /   //       //        / /   / / //   / / //   / /  
 / /____/ / / / ((____   ((____   //   / / //   ) ) ((____       //       // ((___( (  / /   ((____       //____/ / ((____    / /   ((____   ((____    / /   / / ((___/ / //   / /   
\n\n""")


print("Importing Modules ...\n\n")
import cv2
import imutils
import numpy as np
import pytesseract
from time import sleep

#download tesseract from https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20210506.exe

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

imgae_f_us = input("please write the name of picture with it's type file in here.\n")

try:
    img = cv2.imread(imgae_f_us,cv2.IMREAD_COLOR)
    img = cv2.resize(img, (600,400) )
except:
    print("\nThe File that you gave us is incorrect or not available, Please Try Again\n")
    sleep(5)
    exit()


print("Processing image please be patient.")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
gray = cv2.bilateralFilter(gray, 13, 15, 15) 

edged = cv2.Canny(gray, 30, 200) 
contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None


for c in contours:
    
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)
 
    if len(approx) == 4:
        screenCnt = approx
        break

if screenCnt is None:
    detected = 0
    print ("No contour detected")
else:
     detected = 1

if detected == 1:
    cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)


mask = np.zeros(gray.shape,np.uint8)
try:
    new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
except:
    print("\n\nPlease give us a 'jpeg' 'jpg' not a 'png', we can't process it.")
    sleep(5)
    exit()
new_image = cv2.bitwise_and(img,img,mask=mask)

(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
Cropped = gray[topx:bottomx+1, topy:bottomy+1]


text = pytesseract.image_to_string(Cropped, config='--psm 11')
print("\nDetected license plate Number is:",text)
img = cv2.resize(img,(500,300))
Cropped = cv2.resize(Cropped,(400,200))
print("\n\nPress '0' to exit\n")
cv2.imshow('car',img)
cv2.imshow('Cropped',Cropped)

cv2.waitKey(0)
cv2.destroyAllWindows()


#Created By AlPHA