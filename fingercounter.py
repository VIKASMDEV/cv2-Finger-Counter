import cv2
import time
import os
import handtrackingmodule as htm
wCam, hCam = 1600, 900

pTime = 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
folderPath = "fingerImage"
myList = os.listdir(folderPath)
#print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    #print(f'({folderPath}/{imPath})')
    overlayList.append(image)
#print(len(overlayList))

detector = htm.handDetector(detectionCon=0.75)  # handtracking
tipIds = [4, 8, 12, 16, 20]
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    #print(lmList)

    if len(lmList) != 0:  # checking if fingers are opened or closed
        fingers = []
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:  # lmlist[no][y postion]
            fingers.append(1)
        else:
            fingers.append(0)
        for Id in range(1, 5):
         if lmList[tipIds[Id]][2] < lmList[tipIds[Id]-2][2]:  # lmlist[no][y postion]
            fingers.append(1)
         else:
            fingers.append(0)
        #print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)


        # Resize overlayList[0] to (740, 720) to match the slice dimensions
        resized_overlay = cv2.resize(overlayList[totalFingers-1], (200, 200))

        # Now, you can assign the resized overlay to the slice in img
        img[0:200, 0:200] = resized_overlay
        resized_overlay = overlayList[totalFingers-1]

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img,f'fps: {int(fps)}', (40,250),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

