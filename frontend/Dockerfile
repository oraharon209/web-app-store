FROM python:3.8.19-alpine
WORKDIR /frontend
COPY . .
ARG API_SERVER_IP='localhost'
ARG KAFKA_IP='localhost'
ENV API_SERVER_IP=$API_SERVER_IP
ENV KAFKA_IP=$KAFKA_IP
RUN pip install --no-cache-dir -r requirements.txt
CMD python3 store_frontend.py
