#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 19:17:10 2017

@author: haolin
"""
import cv2
import os
from imutils import face_utils

class FaceDetector(object):    
    def __init__(self, method='cv'): 
        
        # @vlaand
        self.local_path = os.path.dirname(os.path.abspath(__file__))
        self._file_paths = {
            'CascadeClassifier':os.path.join(self.local_path,'haarcascade_frontalface_default.xml')
            }
        # @vlaand
        
        self.method = method
        if self.method == 'dlib'        :
            import dlib      
            self.detector = dlib.get_frontal_face_detector()
        elif self.method == 'cv':
            self.face_cascade = cv2.CascadeClassifier(self._file_paths['CascadeClassifier'])            
            
    def detect_face(self, image):
        face_rect = [0,0,0,0]
        if self.method == 'cv':                        
            dets = self.face_cascade.detectMultiScale(image, 1.3, 5)
            if len(dets) > 0:
                face_rect = list(dets[0])
        elif self.method == 'dlib':
            dets = self.detector(image, 1)    
            if len(dets) > 0:
                face_rect = list(face_utils.rect_to_bb(dets[0]))
        return face_rect