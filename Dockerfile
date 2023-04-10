FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive 
RUN apt update
RUN apt-get install python3 -y
RUN python3 --version
RUN apt-get install python3-pip -y
RUN apt-get install vim -y
RUN apt-get -y install systemd
RUN apt-get install wget -y
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
RUN apt-get install -y ./wkhtmltox_0.12.6-1.focal_amd64.deb
RUN apt-get install -y fonts-wqy-microhei ttf-wqy-microhei fonts-wqy-zenhei ttf-wqy-zenhei
RUN fc-cache -f -v

RUN pip3 install --upgrade pip

RUN mkdir /home/mssp-service/

WORKDIR /home/mssp-service/

COPY requirements.txt .  
RUN pip3 install -r requirements.txt
