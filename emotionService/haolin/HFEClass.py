#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 18:18:41 2017

@author: haolin
"""
from skimage import feature
import numpy as np

class HistFeatureExtractor(object):
    def __init__(self, method='LBP', num_points=8, radius=1, ki=4, kj=4):        
        self.method = method
        self.num_points = num_points
        self.radius = radius
        self.ki = ki
        self.kj = kj         
    
    def ExtFea(self, image):
        if self.method == 'LBP':                        
            (height, width) = image.shape
            wi = height/self.ki
            wj = width/self.kj
            num_fea = 59
            
            features = []
            # loop through each block
            for i_start in range(0, height, wi):            
                i_end = i_start + wi
                if i_end >= height-1:
                    i_end = height
                for j_start in range(0, width, wj):
                    j_end = j_start + wj
                    if j_end >= width-1:
                        j_end = width
                    # extract lbp feature
                    face_part = image[i_start:i_end, j_start:j_end]
                    lbp = feature.local_binary_pattern(face_part, self.num_points, self.radius, method="nri_uniform")
        
                    # calculate the histogram
                    (hist, _) = np.histogram(lbp.ravel(), bins=np.arange(0,60))
                    
                	# normalize the histogram
                    hist = hist.astype("float")
                    hist /= (hist.sum() + 1e-7)
                    features.append(hist)
        
            features = np.reshape(features, (1, num_fea*self.ki*self.kj))        
        return features
        
        