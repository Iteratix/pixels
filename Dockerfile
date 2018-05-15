FROM pypy:2

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf
RUN apt-get update && apt-get install -y python-setuptools \
build-essential \
git \
jq \
libffi-dev \
libssl-dev \
python-socketio \
python-flask \
python-serial
# python3-dev \
# python3-pip

ADD ./requirements.txt /opt/lib/pixels/requirements.txt
RUN pip install -r /opt/lib/pixels/requirements.txt

WORKDIR /opt/pixels/
