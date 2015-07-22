FROM index.alauda.cn/lmh5257/django-on-docker

MAINTAINER Komey <lmh5257@live.cn>

ADD . /home/docker/code/ 


RUN pip install -r /home/docker/code/Medical/requirements.txt && /usr/bin/supervisord


VOLUME ["/home/docker/code/app"]
EXPOSE 80
CMD ["exec /usr/sbin/sshd -D"]
