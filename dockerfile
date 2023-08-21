FROM python:3.10.9
COPY . /app
WORKDIR /app
VOLUME /tmp
RUN pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install bilibili-api-python -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install websocket-client -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install pymysql -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["python", "main.py"]