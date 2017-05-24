# 27_emotion_video_dcu

Usage:

> docker run -ti --restart=always -p 5000:5000 mixedemotions/27_emotion_video_dcu > $HOME/dockerlogs/27_emotion_video_dcu.log

Launch with a volume for downloaded files:

> cd /var/www/mixedemotions/tmp

> docker run -ti --restart=always -p 5000:5000 -v $PWD/tmp:/senpy-plugins/tmp mixedemotions/27_emotion_video_dcu > $HOME/dockerlogs/27_emotion_video_dcu.log


Build:

> git clone git@github.com:MixedEmotions/27_emotion_video_dcu.git

> cd 27_emotion_video_dcu

> docker pull vlaand/27_emotion_video_prebuilt

> make run


Rebuild core image:

> cd 27_emotion_video_prebuilt

> make run 


#Docker hub
https://hub.docker.com/r/mixedemotions/27_emotion_video_dcu/

https://hub.docker.com/r/vlaand/27_emotion_video_prebuilt/

