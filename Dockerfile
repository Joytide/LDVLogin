FROM python:3.9
 
ENV DEBIAN_FRONTEND noninteractive
ENV GECKODRIVER_VER v0.32.0
ENV FIREFOX_VER 108.0
 # Lastest as of 01/2023


RUN set -x \
   && apt update \
   && apt upgrade -y \
   && apt install -y firefox-esr cron
RUN pip install loguru selenium
# Works with loguru==0.6.0 selenium==4.7.2 with latest as of 01/2023

# Add latest FireFox
RUN set -x \
   && apt install -y \
       libx11-xcb1 \
       libdbus-glib-1-2 \
   && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
   && tar -jxf firefox-* \
   && mv firefox /opt/ \
   && chmod 755 /opt/firefox \
   && chmod 755 /opt/firefox/firefox

# Add geckodriver
RUN set -x \
   && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/


COPY . /app
WORKDIR /app
RUN crontab cronjob
CMD ["cron", "-f"]