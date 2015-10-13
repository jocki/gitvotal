# Ubuntu
FROM ubuntu:14.04

ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN locale-gen en_US.UTF-8
RUN dpkg-reconfigure locales

RUN apt-get update --fix-missing
RUN apt-get upgrade -y

RUN apt-get install software-properties-common python-software-properties -y
RUN add-apt-repository ppa:nginx/stable -y
RUN add-apt-repository -y ppa:rwky/redis
RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install nginx wget -y
RUN apt-get install build-essential -y
RUN apt-get install libssl-dev openssl nano -y
RUN apt-get install supervisor -y
RUN apt-get install libsqlite3-dev -y
RUN apt-get install python-setuptools -y
RUN apt-get install python-dev -y
RUN apt-get install python-pip -y
RUN apt-get install tcl8.5 -y
RUN apt-get install libffi-dev -y
RUN apt-get install libssl-dev -y

# Python 3.4.2
WORKDIR /tmp/
RUN wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tar.xz
RUN tar -xvf Python-3.4.2.tar.xz
WORKDIR /tmp/Python-3.4.2/
RUN ls
RUN ./configure --with-ensurepip=install
RUN make -j `nproc`
RUN make install
RUN rm -rf /tmp/Python-3.4.2*

# Add user
RUN adduser --disabled-password --gecos "" gitvotal
USER gitvotal
RUN mkdir /home/gitvotal/log
USER root
RUN mkdir /var/gitvotal
RUN chown gitvotal /var/gitvotal

# Copy and extract apps
WORKDIR /home/gitvotal
ADD requirements.txt /home/gitvotal/
RUN pip3 install -r requirements.txt
ENV GITVOTAL_VERSION 0.1
ADD gitvotal-$GITVOTAL_VERSION.tar.gz /home/gitvotal
WORKDIR /home/gitvotal/gitvotal-$GITVOTAL_VERSION
RUN python3 setup.py install

# Configuration files
ADD uwsgi.ini /etc/gitvotal/
ADD uwsgi_params /etc/gitvotal/
ADD config.ini /etc/gitvotal/
ADD supervisor-app.conf /etc/supervisor/conf.d/
ADD nginx-app.conf /etc/nginx/sites-enabled/
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default

# Networking
EXPOSE 80

# Run
USER root
CMD ["supervisord", "-n"]