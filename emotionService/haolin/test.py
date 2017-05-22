#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 16:44:55 2017

@author: haolin
"""

from ESClass import DCU_EmotionService

predictor = DCU_EmotionService()
# use video
json_res = predictor.analysis_video('Navigate The World Of Emotions.mp4', vis=False)

# use webcam
#json_res = predictor.analysis_video(0, vis=True)


