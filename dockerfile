FROM python:3.10.9
COPY . /app
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get install ffmpeg -y
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --upgrade pip setuptools
RUN pip install -U openai-whisper
RUN pip install bilibili-api-python==16.1.1
RUN pip install websocket-client
RUN pip install pymysql
# RUN pip3 install pika
#RUN pip3 install baidu-aip -i https://pypi.tuna.tsinghua.edu.cn/simple
#RUN pip3 install moviepy -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install chardet
WORKDIR /app
VOLUME /tmp
CMD ["python", "main.py"]