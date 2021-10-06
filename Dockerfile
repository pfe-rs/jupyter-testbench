FROM alpine:latest

RUN apk update 
RUN apk add python3 py3-pip curl

EXPOSE 80/tcp

HEALTHCHECK CMD ["/usr/bin/curl", "-f", "http://localhost:80/"]

RUN mkdir -p /web
COPY . /web/
WORKDIR /web

RUN pip install -r /web/requirements.txt

ENTRYPOINT ["/usr/bin/gunicorn", "--bind", "0.0.0.0:80", "wsgi:app"]
