import cv2
import time
import os

def takePic():
	cap = cv2.VideoCapture(0)
	if cap.isOpened():
		_, frame = cap.read()
	cap.release()
	return frame

def savePic(pic, counter):
	cv2.imwrite(str(counter)+'.jpg', pic)
	print('Written {0}.jpg!'.format(counter))

def updateCounter():
	counter = 0
	for file in os.listdir('D:/Work/carpark/pic'):
		if file.endswith('.jpg'):
			number = int(file.strip('.jpg'))
			if number > counter:
				counter = number
	return counter

counter = updateCounter() + 1
os.chdir('D:/work/carpark/pic')
while True:
	pic = takePic()
	savePic(pic, counter)
	counter += 1
	time.sleep(300)
