#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 16:29:55 2017

@author: haolin
"""

import numpy as np

import sys

import cv2
import json
from collections import defaultdict

from sklearn import svm
from sklearn.externals import joblib
from sklearn import preprocessing
from scipy.signal import medfilt

from haolin.HFEClass import HistFeatureExtractor
from haolin.FDClass import FaceDetector

import os

class DCU_EmotionService(object):
    def __init__(self, feature_type='LBP', face_det_type='cv'):        
        
        # @vlaand
        self.local_path = os.path.dirname(os.path.abspath(__file__))
        self._file_paths = {
            'arousal_model': os.path.join(self.local_path,'arousal_model.pkl') ,
            'valence_model': os.path.join(self.local_path,'valence_model.pkl'),
            'fea_scaler': os.path.join(self.local_path,'feature_scaler.pkl')
            }        
        # @vlaand
        
        self.hist_fea_ext = HistFeatureExtractor(method = feature_type)
        self.face_detector = FaceDetector(method = face_det_type)
        self.FACE_SIZE = (76,76)
        self.ki=4
        self.kj=4        
        self.num_fea = 59                
        # load arousal model
        self.arousal_model = joblib.load(self._file_paths['arousal_model'])
        # load valence model
        self.valence_model = joblib.load(self._file_paths['valence_model'])
        # load feature scaler
        self.fea_scaler = joblib.load(self._file_paths['fea_scaler'])
    
    def defDictOfDict(self):
        return defaultdict(dict)
    
    # To Do: add post processing method
    def post_processing_predication():
        return 
                    
    def analysis_video(self, path_to_video_file, vis=False):                    
        cap = cv2.VideoCapture(path_to_video_file)
        total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))    
        face = np.zeros(self.FACE_SIZE).astype('uint8')    
        allFrameData = defaultdict(self.defDictOfDict)
        frameID = 0
        
        # Extract features from given video
        print 'Extracting features .......'
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()   
            if not ret:
                break
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            
            [x,y,w,h] = self.face_detector.detect_face(gray)    
            
            if sum([x,y,w,h]) == 0:
                lbp_fea = np.zeros((1, self.num_fea * self.ki * self.kj))
            else:    
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, self.FACE_SIZE)
                    
                lbp_fea = self.hist_fea_ext.ExtFea(face)
                lbp_fea = self.fea_scaler.transform(lbp_fea)
                
            # Predict arousal, valence value use pre-trained model
            arousal_res = self.arousal_model.predict(lbp_fea)
            valence_res = self.valence_model.predict(lbp_fea)
            # print frameID, arousal_res, valence_res
            allFrameData[frameID][0]['emotion'] = {"pad:arousal":arousal_res[0], "pad:pleasure":valence_res[0]}            
                            
            frameID = frameID + 1                                                    
            
            if vis:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "arousal {0:.2f}, valence {0:.2f}".format(arousal_res[0], valence_res[0]), 
                                              (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
        cap.release()
        
        if vis:
            cv2.destroyAllWindows()
        
        return json.dumps(allFrameData)
        
    