FROM python:3.7-alpine as base
WORKDIR /work
ENV FLASK_APP ./reddit_twitter_data_api_with_sqlite/app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# EXPOSE 5000
# COPY . .
# CMD ["flask", "run"]

###########START NEW IMAGE : DEBUGGER ###################
FROM base as debug
RUN pip install ptvsd

WORKDIR /work/
CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess -m flask run -h 0.0.0 -p 5000

###########START NEW IMAGE: PRODUCTION ###################
FROM base as prod

CMD flask run -h 0.0.0 -p 5000

