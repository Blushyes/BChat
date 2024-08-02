FROM python:3.10.9
COPY . /app
# 下载并安装ffmpeg，为分析@视频
# RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
# RUN sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
# RUN apt-get update
# RUN apt-get install ffmpeg -y
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
WORKDIR /app
VOLUME /tmp
CMD ["python", "main.py"]