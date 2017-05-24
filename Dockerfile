FROM vlaand/27_emotion_video_prebuilt:latest

COPY logo-dcu.png /usr/local/lib/python2.7/site-packages/senpy/static/img/gsi.png
RUN perl -i -pe s^http://www.gsi.dit.upm.es^https://nuig.insight-centre.org/unlp/^g /usr/local/lib/python2.7/site-packages/senpy/templates/index.html
RUN perl -i -pe 's^https://nuig.insight-centre.org/unlp/" target="_blank"><img id="mixedemotions-logo^http://mixedemotions-project.eu/" target="_blank"><img id="mixedemotions-logo^g' /usr/local/lib/python2.7/site-packages/senpy/templates/index.html

COPY . /senpy-plugins/
RUN python -m senpy --only-install -f /senpy-plugins
