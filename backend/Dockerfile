FROM python:3.8.19-alpine3.20
WORKDIR /backend
COPY . .
ARG MONGO_IP='localhost'
ARG KAFKA_IP='localhost'
ENV MONGO_IP=$MONGO_IP
ENV KAFKA_IP=$KAFKA_IP
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "-m", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
