FROM python:3.11.4-alpine

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /social_network

COPY ./requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8080

COPY . .

WORKDIR /social_network/social_network
