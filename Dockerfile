FROM phusion/baseimage

WORKDIR /app

RUN apt-get clean && apt-get update && apt-get install -y apt-utils python3 python3-dev python3-pip build-essential \
    python3-nose libpq-dev

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt
# Now we add /app
COPY . /app
ENV LC_ALL=C.UTF-8