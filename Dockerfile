FROM        python:3

EXPOSE 5000

RUN         mkdir /data
COPY        app /data/app
COPY        tests /data/tests
COPY        setup.py /data
RUN         pip install -U pip
RUN         pip install /data
WORKDIR    /data/
ENV         FLASK_APP=app

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]