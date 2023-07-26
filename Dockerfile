FROM joyzoursky/python-chromedriver:3.8

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
