FROM python:3.8.1
ENV PYTHONUNBUFFERED 1
ENV TERM xterm

# Let the conatiner know that there is no tty
ENV DEBIAN_FRONTEND noninteractive

# Packets
RUN apt-get update -qqy && apt-get install -qqy software-properties-common nano cron tzdata locales vim lsof inetutils-ping unzip

# Set the locale
RUN locale-gen pt_BR.UTF-8  
ENV LANG pt_BR.UTF-8  
ENV LANGUAGE pt_BR:en  
RUN rm /etc/localtime && ln -s /usr/share/zoneinfo/Etc/GMT+3 /etc/localtime 

# Add colours to bashrc
RUN  sed -i -e "s/#force_color_prompt=yes/force_color_prompt=yes/g" /root/.bashrc

RUN pip install -U pip setuptools
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY ./ /usr/src/app

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pip install pygments
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/bash"]
