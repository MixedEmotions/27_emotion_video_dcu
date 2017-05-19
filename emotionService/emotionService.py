
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
import requests, shutil



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
        
        self._storage_path = '/home/vlaand/IpythonNotebooks/27_emotion_video_dcu/tmp'
        self._storage_path = 'tmp'
        

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
        
    def _download_file(self, saveFolder = 'tmp', url = "http://mixedemotions.insight-centre.org/tmp/little-girl.mp4"):
        
        logger.info("{} {}".format(datetime.now(), "downloading "+url))
        st = datetime.now()        
        global dump       
        downloadedFile = requests.get(url, stream=True)
        dump = downloadedFile.raw

        path, filename  = os.path.dirname(url), os.path.basename(url)    
        #print(path, filename)

        with open(os.path.join(saveFolder, filename), 'wb') as file:
            shutil.copyfileobj(dump, file)

        del dump
        del downloadedFile
        
        logger.info("{} {}".format(datetime.now() - st, "downloaded "+url))

        return os.path.join(saveFolder,filename)
    
    
    
    
        
    def analyse(self, **params):
        
        logger.debug("emotionService with params {}".format(params))    
        
        
        
        
        ## FILE MANIPULATIONS ------------------------------- \  
        
        filename = params.get("filename", None)
        #filename = 'little-girl.mp4' # TEMPORARY FIX
        
        #filename = '/var/www/mixedemotions/tmp/wikoe20151114_wiruebli_sd_avc.mp4''
#         url = "http://mixedemotions.insight-centre.org/tmp/little-girl.mp4"
        
        #if not os.path.isfile(filename):
            #raise Error("File does not exist")
            #print("File does not exist")     
        
#         filename = self._download_file(
#                 saveFolder = 'tmp',
#                 url = "http://mixedemotions.insight-centre.org/tmp/little-girl.mp4")
        
        filename = os.path.join(self._storage_path, filename)
    
        if not os.path.isfile(filename):
            raise Error("File does not exist") 
        else:
            print("file found")
            
        #input_file = ffmpeg.file_input(filename)    
            
            
        
        ## EXTRACTING FEATURES ------------------------------- \  
        
        feature_set = self._extract_features(filename = filename)
        
        response = Results()
        entry = Entry()   
        entry['filename'] = filename
        
        emotionSet = EmotionSet()
        emotionSet.id = "Emotions"
        
        emotion1 = Emotion() 
        
        for dimension in ['V','A','D']:
            value = 5.0
            emotion1[ self._centroid_mappings[dimension] ] = feature_set[dimension]            

        emotionSet.onyx__hasEmotion.append(emotion1)
    
        entry.emotions = [emotionSet,]
        
        response.entries.append(entry)
        
        return response

