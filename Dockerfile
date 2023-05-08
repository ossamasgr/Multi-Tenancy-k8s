FROM python:3-alpine

WORKDIR /app

COPY . /app
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN apk add --no-cache openssl

RUN apk update && apk add curl
RUN curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | sh


EXPOSE 80 2222

CMD ["python", "app.py"]
