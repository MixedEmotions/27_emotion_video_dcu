
# coding: utf-8

# In[ ]:



from __future__ import division
import logging
import os
import xml.etree.ElementTree as ET

from senpy.plugins import SenpyPlugin, EmotionPlugin
from senpy.models import Results, Entry

logger = logging.getLogger(__name__)

import numpy as np
import math, itertools
from collections import defaultdict

import gzip
from datetime import datetime 



class machineTranslation(EmotionPlugin):
    
    def __init__(self, info, *args, **kwargs):
        super(machineTranslation, self).__init__(info, *args, **kwargs)
        self.name = info['name']
        self.id = info['module']
        self._info = info
        local_path=os.path.dirname(os.path.abspath(__file__))
   
        

    def activate(self, *args, **kwargs):
        
        st = datetime.now()        
        logger.info("{} {}".format(datetime.now() - st, "active"))
        logger.info("%s plugin is ready to go!" % self.name)
        
    def deactivate(self, *args, **kwargs):
        try:
            logger.info("%s plugin is being deactivated..." % self.name)
        except Exception:
            print("Exception in logger while reporting deactivation of %s" % self.name)

    def analyse(self, **params):
        
        logger.debug("machine translation with params {}".format(params))
                
        text_input = params.get("input", None)
        self.__source = params.get("sourcelanguage", 'en')
        self.__target = params.get("targetlanguage", 'es')
        
##------## PUT YOUR CODE HERE------------------------------- \  
        
        def _your_method(text):
            return text.lower()
        
        text_output = _your_method(text_input)
        
##------## PUT YOUR CODE HERE------------------------------- \  
            
        response = Results()
        entry = Entry()        
        
        entry.nif__isString = text_input  
        entry['nif:predLang'] = self.__source
    
        translation = {}        
        translation['nif:isString'] = text_output
        translation['nif:predLang'] = self.__target
        translation['nif:wasTranslatedFrom'] = entry.id     
        
        entry['nif:translation'] = [translation]
        
        response.entries.append(entry)
            
        return response


# In[ ]:

"""
@micarc:

I managed to docker-ize the translation models we have with the moses 
translation toolkit. Since I followed the path of "learning-by-doing" 
and ignoring all documentations I am quite sure some parts of a good 
implementation are missing. Therefore, suggestions to improve this 
docker images are more than welcome

instructions:

1) install docker
2) save the attached docker file into a foder
3) run command: docker build -t docker/whalesay .     (in the same 
folder as the attached and docker file, don't forget the fullstop)
4) run command: docker run -td docker/whalesay
5) run command: docker exec "container-name" /translate.perl 
source_language_code target_language_code "text to be translated"

language codes = 
en|bg|cs|da|de|el|es|et|fi|fr|ga|hr|hu|it|lt|lv|mt|nl|pl|pt|ro|sk|sl|sr|sv

"""

"""
docker build -t 18_machine_translation_nuig .
docker exec docker/whalesay /translate.perl 

"""


# In[ ]:

"""
FROM docker/whalesay:latest
RUN apt-get update && apt-get install -q -y unzip make g++ wget git git-core mercurial bzip2 autotools-dev automake libtool zlib1g-dev libbz2-dev libboost-all-dev libxmlrpc-core-c3-dev libxmlrpc-c++8-dev build-essential pkg-config python-dev cmake libcmph-dev libcmph-tools libcmph0 libgoogle-perftools-dev liblzma-dev
RUN git clone https://github.com/moses-smt/mosesdecoder.git
RUN mkdir -p /home/mosesdecoder
WORKDIR mosesdecoder/
RUN ./bjam --prefix=/home/mosesdecoder --install-scripts --with-cmph=/usr/include/cmph --with-xmlrpc-c -j8
RUN rm -rf mosesdecoder/
WORKDIR /
RUN wget http://server1.nlp.insight-centre.org/docker/translate.perl
RUN chmod +x translate.perl
"""


# In[1]:

## THIS IS A TEST CELL

# def _backwards_conversion(original):    
#         """Find the closest category"""        
#         dimensions = list(centroids.values())[0]        
#         def distance(e1, e2):
#             return sum((e1[k] - e2.get(k, 0)) for k in dimensions)
#         distances = { state:distance(centroids[state], original) for state in centroids }
#         mindistance = max(distances.values())
#         print(distances)
#         dummyfix = sorted(distances.values(),reverse=True)
#         for state in distances:
#             if distances[state] == dummyfix[0] or distances[state] == dummyfix[1]:
#                 mindistance = distances[state]
#                 emotion = state                
#                 print(state)
#             else:
#                 print(state, 'no')                
#         result = Emotion(onyx__hasEmotionCategory=emotion, onyx__hasEmotionIntensity=emotion)
#         return result
    
# feature_text = {
#     "A":5.9574053436517715,
#     "D":6.3352929055690765,
#     "V":2.9072564840316772
# }

# centroids= {
#     "anger": {
#         "A": 6.95, 
#         "D": 5.1, 
#         "V": 2.7}, 
#     "disgust": {
#         "A": 5.3, 
#         "D": 8.05, 
#         "V": 2.7}, 
#     "fear": {
#         "A": 6.5, 
#         "D": 3.6, 
#         "V": 3.2}, 
#     "joy": {
#         "A": 7.22, 
#         "D": 6.28, 
#         "V": 8.6}, 
#     "sadness": {
#         "A": 5.21, 
#         "D": 2.82, 
#         "V": 2.21}
# }  

# from senpy.models import Emotion

# emotion = Emotion() 
# for dimension in ["V","A","D"]:
#     emotion[dimension] = float((feature_text[dimension])) 
    
# _backwards_conversion(emotion)

