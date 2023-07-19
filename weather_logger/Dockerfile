FROM python:3.9

RUN apt update
RUN apt install -y cron
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN mkdir /app
WORKDIR /app
COPY . /
RUN pip install -U pip
RUN pip install -Ur requirements.txt

RUN echo '*/5 * * * * root' $(which python) '/app/__main__.py >> /var/log/cron/weather.log' >> /etc/cron.d/cron
RUN chmod 644 /etc/cron.d/*

CMD cron && tail -f /dev/null
