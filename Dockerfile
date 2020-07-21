FROM python:3.8.1,
ENV PYTHONUNBUFFERED 1,

RUN pip install -U pip setuptools,

RUN mkdir -p /usr/src/app,
WORKDIR /usr/src/app,
COPY ./ /usr/src/app,

RUN pip install --upgrade pip,
RUN pip install pipenv,
RUN pipenv lock --requirements > requirements.txt,
RUN pip install -r requirements.txt,

EXPOSE 80,
CMD sh /usr/src/app/run_web.sh