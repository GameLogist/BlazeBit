FROM python:3.7-slim

RUN apt-get update -y && \
    apt-get install -y nginx
   
# RUN apk add --no-cache gcc musl-dev linux-headers
COPY ./requirements.txt /app/requirements.txt
ENV FLASK_APP run.py
WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app

# ENTRYPOINT [ "python" ]

# CMD [ "run.py" ]