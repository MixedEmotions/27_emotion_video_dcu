FROM gsiupm/senpy:0.8.8-python2.7

ENV PYTHON_VERSION 2.7
ENV NUM_CORES 4

COPY logo-dcu.png /usr/local/lib/python$PYTHON_VERSION/site-packages/senpy/static/img/gsi.png
RUN perl -i -pe s^http://www.gsi.dit.upm.es^https://nuig.insight-centre.org/unlp/^g /usr/local/lib/python$PYTHON_VERSION/site-packages/senpy/templates/index.html
RUN perl -i -pe 's^https://nuig.insight-centre.org/unlp/" target="_blank"><img id="mixedemotions-logo^http://mixedemotions-project.eu/" target="_blank"><img id="mixedemotions-logo^g' /usr/local/lib/python$PYTHON_VERSION/site-packages/senpy/templates/index.html

RUN cd /

RUN apt-get -y update
RUN apt-get -y install python$PYTHON_VERSION-dev wget unzip \
                       build-essential cmake git pkg-config libatlas-base-dev gfortran \
                       libjasper-dev libgtk2.0-dev libavcodec-dev libavformat-dev \
                       libswscale-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libv4l-dev
    
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install numpy matplotlib

RUN wget https://github.com/Itseez/opencv/archive/3.1.0.zip && \
    unzip 3.1.0.zip && \
    rm 3.1.0.zip && \  
    mv opencv-3.1.0 /opencv && \    
    wget https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip && \
    unzip 3.1.0.zip && \
    rm 3.1.0.zip && \    
    mv opencv_contrib-3.1.0 /opencv_contrib
#RUN cd /
#RUN wget https://github.com/Itseez/opencv/archive/3.1.0.zip -O opencv3.zip && \
#    unzip -q opencv3.zip && mv /opencv-3.1.0 /opencv
#RUN wget https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip -O opencv_contrib3.zip && \
#    unzip -q opencv_contrib3.zip && mv /opencv_contrib-3.1.0 /opencv_contrib
    
RUN mkdir /opencv/build
WORKDIR /opencv/build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D BUILD_PYTHON_SUPPORT=ON \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=OFF \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib/modules \
	-D BUILD_EXAMPLES=ON \
	-D BUILD_NEW_PYTHON_SUPPORT=ON \
	-D WITH_IPP=OFF \
	-D WITH_V4L=ON ..
RUN make -j$NUM_CORES
RUN make install
RUN ldconfig
RUN pip install scikit-learn
RUN pip install scikit-image
RUN pip install imutils
