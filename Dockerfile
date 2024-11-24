FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow

RUN apt-get update && apt-get install -y python3-pip python3 && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /

CMD ["python3", "main.py"]
