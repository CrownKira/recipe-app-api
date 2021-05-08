FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# permanent dependencies
RUN apk add --update --no-cache postgresql-client jpeg-dev
# temporary build dependencies
# used just for installing pip packages
# will be wiped after docker build
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# store any files that need to be shared with other container in vol 
# media/ : used for media files uploaded by the user
# -p : make all the subdirectories if they dont exist
RUN mkdir -p /vol/web/media
# static/ : used for js, css files, etc 
# ie. not changing during the execution of the application
RUN mkdir -p /vol/web/static
RUN adduser -D user
# sets the ownership of all the directory in vol directory to 
# the custom user 
# -R : recursive
RUN chown -R user:user /vol/
# the user can do everything with the directory
# the rest can read and execute from the directory
RUN chmod -R 755 /vol/web
USER user