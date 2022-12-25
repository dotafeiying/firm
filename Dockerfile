FROM python:3.7

# 镜像作者
MAINTAINER Jie

# 更新依赖
RUN apt-get update

# 设置python环境变量
ENV PYTHONUNBUFFERED 1

# 在容器内创建项目文件夹
RUN mkdir -p /firm

# 设置容器内工作目录
WORKDIR /firm

# 将当前目录文件加入到容器工作目录中
ADD . /firm

# 更新pip版本
#RUN /usr/local/bin/python -m pip install --upgrade pip

# pip安装依赖
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/
RUN pip install gunicorn -i https://pypi.douban.com/simple/

# 设置环境变量
ENV SPIDER=/firm
