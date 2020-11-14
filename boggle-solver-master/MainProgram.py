import numpy as np
import cv2
import operator
#from matplotlib import pyplot as plt
import joblib
from dlxsudoku import Sudoku
import FindDigits as cw
import multiprocessing as mp
import os
import ThreadWorker as tw
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import tensorflow as tf
import tensorflow.keras as keras
def main():
	skipped = 0
	boardType = 'boggle'	
	number_of_processes = 5
	InputQueue = mp.Queue()
	FinalImages = mp.Queue()
	ProcessedDigits= mp.Queue()
	DigitsQueue = mp.Queue()
	processQueue = mp.Queue()
	processes = []
	for i in range(number_of_processes):
		boggleSolve = mp.Process(target=tw.AttemptBoggleSolve, args=(InputQueue,ProcessedDigits,FinalImages,DigitsQueue))
		processes.append(boggleSolve)
		boggleSolve.start()

	p = mp.Process(target=tw.ShowFinalImage, args=(ProcessedDigits, FinalImages))
	p.start()
	nn = mp.Process(target = tw.NeuralNetworkThread, args=(DigitsQueue, processQueue))
	nn.start()

	boardFound = 1
	cap = cv2.VideoCapture(0)
	ret, frame = cap.read()
	centerX = frame.shape[1]/2
	centerY = frame.shape[0]/2
	x1 = int(centerX - 170)
	y1 = int(centerY - 170)
	x2 = int(centerX + 170)
	y2 = int(centerY + 170)
	startPoint = (x1,y1)
	endPoint = (x2,y2)
	font = cv2.FONT_HERSHEY_SIMPLEX
	org = (50, 50) 
	fontScale = 1
	color = (255, 0, 0) 
	thickness = 2
	result = np.zeros(81)
	img = frame
	cropped = frame
	result_old = np.zeros(81)
	result_really_old = result_old
	while(True):
		ret, frame = cap.read()
		if not np.sum(frame) == 0:
			break
	while(True):
		ret, frame = cap.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		frame = cv2.rectangle(frame, startPoint, endPoint, (255,0,0), 10)
		frame = cv2.putText(frame, 'Align ' + boardType + ' board with square', org, font,  
		fontScale, color, thickness, cv2.LINE_AA) 
		gray = gray[y1:y2, x1:x2]
		cv2.imshow('Original',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
		if (InputQueue.qsize() < 10):
			InputQueue.put(gray)
		else:
			print("Queue is full. Skipped", skipped, "frames.")
			skipped += 1
	p.terminate()
	for pr in processes:
		pr.terminate()

	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
