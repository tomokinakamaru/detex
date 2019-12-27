FROM python:3.7

RUN mkdir /src

COPY . /src

RUN cd /src && pip install .

WORKDIR /workdir

ENTRYPOINT [ "detex" ]
