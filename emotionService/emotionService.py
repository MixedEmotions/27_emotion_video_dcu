
# coding: utf-8

# In[ ]:



from __future__ import division
import logging
import os
import xml.etree.ElementTree as ET

from senpy.plugins import EmotionPlugin, SenpyPlugin
from senpy.models import Results, EmotionSet, Entry, Emotion, Error

logger = logging.getLogger(__name__)

import numpy as np
import math, itertools
from collections import defaultdict

import gzip
from datetime import datetime 

import ffmpeg



class emotionService(EmotionPlugin):
    
    def __init__(self, info, *args, **kwargs):
        super(emotionService, self).__init__(info, *args, **kwargs)
        self.name = info['name']
        self.id = info['module']
        self._info = info
        local_path = os.path.dirname(os.path.abspath(__file__))        
        
        self._centroid_mappings = {
            "V": "http://www.gsi.dit.upm.es/ontologies/onyx/vocabularies/anew/ns#valence",
            "A": "http://www.gsi.dit.upm.es/ontologies/onyx/vocabularies/anew/ns#arousal",
            "D": "http://www.gsi.dit.upm.es/ontologies/onyx/vocabularies/anew/ns#dominance"          
            }  
        

    def activate(self, *args, **kwargs):
        
        st = datetime.now()        
        logger.info("{} {}".format(datetime.now() - st, "active"))
        logger.info("%s plugin is ready to go!" % self.name)
        
    def deactivate(self, *args, **kwargs):
        try:
            logger.info("%s plugin is being deactivated..." % self.name)
        except Exception:
            print("Exception in logger while reporting deactivation of %s" % self.name)
            
            
    # CUSTOM FUNCTION
    
    def _extract_features(self, filename):
        
        feature_set = { dimension:float(5.0) for dimension in ['V','A','D'] }            
        return feature_set

    def analyse(self, **params):
        
        logger.debug("emotionService with params {}".format(params))
        
        
##------## PUT YOUR CODE HERE------------------------------- \  

        filename = params.get("filename", None)
#         filename = '/var/www/mixedemotions/tmp/wikoe20151114_wiruebli_sd_avc.mp4'
        filename = '/home/vlaand/data/wikoe20151114_wiruebli_sd_avc.mp4'
    
        if not os.path.isfile(filename):
            raise Error("Error: File does not exist")
    
#         input_file = ffmpeg.file_input(filename)
    
        
        feature_set = self._extract_features(filename = filename)
        
        print(feature_set)
            
        response = Results()
        entry = Entry()    
        
        emotionSet = EmotionSet()
        emotionSet.id = "Emotions"
        
        emotion1 = Emotion() 
        
        for dimension in ['V','A','D']:
            value = 5.0
            emotion1[ self._centroid_mappings[dimension] ] = feature_set[dimension]
            
##------## PUT YOUR CODE HERE------------------------------- \

        emotionSet.onyx__hasEmotion.append(emotion1)
    
        entry.emotions = [emotionSet,]
        
        response.entries.append(entry)
        
        return response

