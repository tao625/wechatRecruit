FROM python:3.6
MAINTAINER danding
COPY . /opt/wechatRecruit
WORKDIR /opt/wechatRecruit
RUN pip install -r requestment.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && python manage.py runserver 0.0.0.0:8020 &
EXPOSE 8020

