FROM vckyouuu/geezprojects:buster

RUN git clone -b Tonic-Userbot https://github.com/Tonic990/Tonic-Userbot  /root/userbot/
    && chmod 777 /root/userbot \
    && mkdir /root/userbot/bin/

WORKDIR /root/userbot/

CMD [ "bash", "start" ]
