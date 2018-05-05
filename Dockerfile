FROM python

WORKDIR code

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN rm requirements.txt