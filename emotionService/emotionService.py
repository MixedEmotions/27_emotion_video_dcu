
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

import requests, shutil
import subprocess
import sys


from haolin.ESClass import DCU_EmotionService
import json


class emotionService(EmotionPlugin):
    
    def __init__(self, info, *args, **kwargs):
        super(emotionService, self).__init__(info, *args, **kwargs)
        self.name = info['name']
        self.id = info['module']
        self._info = info
        local_path = os.path.dirname(os.path.abspath(__file__))
        
        self._dimensions = ['V','A']
        
        self._centroid_mappings = {
            "V": "http://www.gsi.dit.upm.es/ontologies/onyx/vocabularies/anew/ns#valence",
            "A": "http://www.gsi.dit.upm.es/ontologies/onyx/vocabularies/anew/ns#arousal",
            "D": "http://www.gsi.dit.upm.es/ontologies/onyx/vocabularies/anew/ns#dominance"          
            }  
        
        self._storage_path = '/senpy-plugins/tmp'
        

    def activate(self, *args, **kwargs):
        
        st = datetime.now()   
        self._predictor = DCU_EmotionService()
        logger.info("{} {}".format(datetime.now() - st, "predictor loaded"))
        
        st = datetime.now()        
        logger.info("{} {}".format(datetime.now() - st, "active"))
        logger.info("%s plugin is ready to go!" % self.name)
        
    def deactivate(self, *args, **kwargs):
        try:
            logger.info("%s plugin is being deactivated..." % self.name)
        except Exception:
            print("Exception in logger while reporting deactivation of %s" % self.name)
            
            
    # CUSTOM FUNCTION
    
    def _download_file(self, saveFolder = '/senpy-plugins/tmp', url = "http://mixedemotions.insight-centre.org/tmp/little-girl.mp4"):
        
        logger.info("{} {}".format(datetime.now(), "downloading "+url))
        st = datetime.now()        
        global dump       
        downloadedFile = requests.get(url, stream=True)
        dump = downloadedFile.raw

        path, filename  = os.path.dirname(url), os.path.basename(url)    
        with open(os.path.join(saveFolder, filename), 'wb') as file:
            shutil.copyfileobj(dump, file)

        del dump
        del downloadedFile
        
        logger.info("{} {}".format(datetime.now() - st, "downloaded "+url))

        return os.path.join(saveFolder,filename)
    
    def _download_file_v1(self, saveFolder = '/senpy-plugins/tmp', url = "http://mixedemotions.insight-centre.org/tmp/little-girl.mp4"):
        
        st = datetime.now()
        logger.info("{} {}".format(datetime.now(), "downloading "+url))        
        
        path, filename  = os.path.dirname(url), os.path.basename(url)        
        outfilename = os.path.join(saveFolder,filename)
        
        subprocess.call(['wget', '-O', outfilename, url])
        logger.info("{} {}".format(datetime.now() - st, "downloaded "+url))
        
        return outfilename
    
    def _remove_file(self, filename):
        st = datetime.now()
        logger.info("{} {}".format(datetime.now(), "deleting "+ filename))  
        
        subprocess.call(['rm', '-f', filename])
        logger.info("{} {}".format(datetime.now() - st, "deleted "+filename))
    
    
    def _convert_longformat_to_shortformat(self, json_long):         
        
        json_long = json.loads(json_long)        
        json_short = { 
            'V': np.mean([json_long[frame]['0']['emotion']['pad:pleasure'] for frame in json_long]) , 
            'A': np.mean([json_long[frame]['0']['emotion']['pad:arousal' ] for frame in json_long]) 
            }
        return json_short
    
    def _extract_features(self, filename, convert=True):        
          
        # predictor = DCU_EmotionService()
        json_res = self._predictor.analysis_video(filename, vis=False)
        
        if convert:
            json_res = self._convert_longformat_to_shortformat(json_res)
        
        return json_res
    
        
    def analyse(self, **params):
        
        logger.debug("emotionService with params {}".format(params))         
                
        ## FILE MANIPULATIONS ------------------------------- \ 
        
        filename = params.get("i", None)
        downloaded = params.get("d", None)
        
        if downloaded:            
            filename = os.path.join(self._storage_path,filename)
        else:
            filename = self._download_file_v1(saveFolder = self._storage_path, url = filename)
        
        logger.info("{} {}".format(datetime.now(), filename))
        
        if not os.path.isfile(filename):
            raise Error("File %s does not exist" % filename) 
        
        ## EXTRACTING FEATURES ------------------------------- \ 
        
        feature_set = self._extract_features(filename, convert=True)
        # self._remove_file(filename)
        
        ## GENERATING OUTPUT --------------------------------- \        
                
        response = Results()
        entry = Entry()   
        entry['filename'] = filename
        
        emotionSet = EmotionSet()
        emotionSet.id = "Emotions"
        
        emotion1 = Emotion() 
        
        for dimension in self._dimensions:
            emotion1[ self._centroid_mappings[dimension] ] = 5*(1+feature_set[dimension])           

        emotionSet.onyx__hasEmotion.append(emotion1)
    
        entry.emotions = [emotionSet,]        
        response.entries.append(entry)
        
        return response

