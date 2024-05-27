from flask import Flask, request, jsonify, render_template, redirect
from kafka import KafkaProducer
import requests
import json
import os

# Creating a Flask instance
app = Flask(__name__)

# Loading env vars into code
KAFKA_IP = os.getenv('KAFKA_IP')
API_SERVER_IP = os.getenv('API_SERVER_IP')
API_SERVER_URL = f'http://{API_SERVER_IP}:5000'
kafka_password = os.getenv('KAFKA_PASSWORD')

# Set Kafka SASL authentication configurations
sasl_mechanism = "PLAIN"
security_protocol = "SASL_PLAINTEXT"
username = "user1"

# Kafka production configuration
producer = KafkaProducer(
    bootstrap_servers=f'{KAFKA_IP}:9092',
    security_protocol=security_protocol,
    sasl_mechanism=sasl_mechanism,
    sasl_plain_username=username,
    sasl_plain_password=kafka_password,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


@app.route('/buy', methods=['POST'])
def buy_item():
    user_id = request.form.get('userID')
    item_id = request.form.get('id')
    if user_id and item_id:
        purchase_data = {'userID': user_id, 'id': item_id}
        producer.send('purchase_topic', value=purchase_data)
        return redirect('/')
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request parameters'}), 400


@app.route('/get_purchases', methods=['POST'])
def get_items():
    users_response = requests.get(f'{API_SERVER_URL}/users')
    items_response = requests.get(f'{API_SERVER_URL}/items')
    users = users_response.json()
    items = items_response.json()
    user_id = request.form.get('userID')
    user_response = requests.get(f'{API_SERVER_URL}/get_user_by_id', params={'userID': user_id})
    user_items = user_response.json()
    return render_template('index.html', user_purchases=user_items, users=users, items=items)


@app.route('/', methods=['GET', 'POST'])
def main():
    users_response = requests.get(f'{API_SERVER_URL}/users')
    items_response = requests.get(f'{API_SERVER_URL}/items')
    users = users_response.json()
    items = items_response.json()
    return render_template('index.html', users=users, items=items)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
