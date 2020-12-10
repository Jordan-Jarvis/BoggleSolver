import FindDigits as cw
import multiprocessing as mp
import os
import cv2 
import joblib
import numpy as np
from time import sleep
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
import tensorflow.keras as keras
import boggle1 as bg
from GUI import *

def ShowFinalImage(queue1, queue2):
    while True:
        if queue2.empty() == False:
            cropped = queue2.get()
            cv2.imshow('Final Image',cropped)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        if queue1.empty():
            sleep(0.05)
            continue
        img = queue1.get()
        cv2.imshow("Cropped (warp affine)" + str(os.getppid()), img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#queue is cropped and black and white 

def AttemptBoggleSolve(InputQueue, ProcessedDigits, FinalImage, DigitsQueue):
    while True:
        gray = InputQueue.get()
        img, cropped, digits = cw.extract_boggle(gray)
        ProcessedDigits.put(img)
        digits = np.array(digits)
        if DigitsQueue.qsize() < 10:
            DigitsQueue.put((digits,cropped))
        

def NeuralNetworkThread(DigitsQueue, processQueue):
    trainedModel = keras.models.load_model('TrainedBoggle')
    yRepresentations = ('a0','a1','a2','a3','b0','b1','b2','b3','c0','c1','c2','c3','d0','d1','d2','d3','e0','e1','e2','e3','f0','f1','f2','f3','g0','g1','g2','g3','h0','h1','h2','h3','i0','i1','i2','i3','j0','j1','j2','j3','k0','k1','k2','k3','l0','l1','l2','l3','m0','m1','m2','m3','n0','n1','n2','n3','o0','o1','o2','o3','p0','p1','p2','p3','q0','q1','q2','q3','r0','r1','r2','r3','s0','s1','s2','s3','t0','t1','t2','t3','u0','u1','u2','u3','v0','v1','v2','v3','w0','w1','w2','w3','x0','x1','x2','x3','y0','y1','y2','y3','z0','z1','z2','z3','00','11')

    while True:
        if DigitsQueue.empty() == False:
            digits = DigitsQueue.get()
            cropped = digits[1]
            digits = digits[0]
        else:
            sleep(0.05)
            continue
        y_test_pred = trainedModel.predict_classes(digits, verbose=0)
        PredictedVals = []
        for index in y_test_pred:
            PredictedVals.append(yRepresentations[index][0])
        if '0' in PredictedVals:
            continue
        if '1' in PredictedVals:
            continue
        tempVal = 0
        tempVal2 = 0

        PredictedVals = [x.upper() for x in PredictedVals] 
        for i in range(len(PredictedVals)):
            if PredictedVals[i] == 'Q':
                PredictedVals[i] = "Qu"
        listBox(bg.SolveBoard(PredictedVals))

