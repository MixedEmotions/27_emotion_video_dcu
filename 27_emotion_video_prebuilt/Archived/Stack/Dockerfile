FROM gsiupm/senpy:0.8.8-python2.7

COPY logo-dcu.png /usr/local/lib/python3.5/site-packages/senpy/static/img/gsi.png
RUN perl -i -pe s^http://www.gsi.dit.upm.es^https://nuig.insight-centre.org/unlp/^g /usr/local/lib/python3.5/site-packages/senpy/templates/index.html
RUN perl -i -pe 's^https://nuig.insight-centre.org/unlp/" target="_blank"><img id="mixedemotions-logo^http://mixedemotions-project.eu/" target="_blank"><img id="mixedemotions-logo^g' /usr/local/lib/python3.5/site-packages/senpy/templates/index.html


RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app 

# Various Python and C/build deps
RUN apt-get update && apt-get install -y \ 
    wget \
    build-essential \ 
    cmake \ 
    git \
    unzip \ 
    pkg-config \
    python-dev \ 
    python-opencv \ 
    libopencv-dev \ 
    libav-tools  \ 
    libjpeg-dev \ 
    libpng-dev \ 
    libtiff-dev \ 
    libjasper-dev \ 
    libgtk2.0-dev \ 
    python-numpy \ 
    python-pycurl \ 
    libatlas-base-dev \
    gfortran \
    webp \ 
    python-opencv \ 
    qt5-default \
    libvtk6-dev \ 
    zlib1g-dev 

# Install Open CV - Warning, this takes absolutely forever
RUN mkdir -p ~/opencv cd ~/opencv && \
    wget https://github.com/opencv/opencv/archive/3.2.0.zip && \
    unzip 3.2.0.zip && \
    rm 3.2.0.zip && \
    mv opencv-3.2.0 OpenCV && \
    cd OpenCV && \
    mkdir build && \ 
    cd build && \
    cmake \
    -DWITH_QT=ON \ 
    -DWITH_OPENGL=ON \ 
    -DFORCE_VTK=ON \
    -DWITH_TBB=ON \
    -DWITH_GDAL=ON \
    -DWITH_XINE=ON \
    -DBUILD_EXAMPLES=ON .. && \
    make -j4 && \
    make install && \ 
    ldconfig

# COPY requirements.txt /usr/src/app/
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . /usr/src/app 