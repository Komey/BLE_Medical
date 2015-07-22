FROM index.alauda.cn/lmh5257/django-on-docker

MAINTAINER Komey <lmh5257@live.cn>

ADD . /home/docker/code/ 


RUN pip install -r /home/docker/code/app/requirements.txt && chmod +x /home/docker/code/*.sh



EXPOSE 80
CMD ["/home/docker/code/run.sh"]
