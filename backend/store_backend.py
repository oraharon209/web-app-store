from flask import Flask, request, jsonify
from pymongo import MongoClient
from kafka import KafkaConsumer
import threading
import json
import os

# Creating a Flask instance
app = Flask(__name__)

# Loading env vars into code
MONGO_IP = os.getenv('MONGO_IP')
MONGO_PORT = 27017
mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')
KAFKA_IP = os.getenv('KAFKA_IP')
kafka_password = os.getenv('KAFKA_PASSWORD')


# Use the MongoDB instance running on port 27017

mongo_client = MongoClient(f'mongodb://{mongo_username}:{mongo_password}@{MONGO_IP}:{MONGO_PORT}/', 
                           serverSelectionTimeoutMS=5000, 
                           authSource='admin', 
                           authMechanism='SCRAM-SHA-1')
db = mongo_client['shop_db']
collection_user = db['users']
collection_items = db['items']


# Set Kafka SASL authentication configurations
sasl_mechanism = "PLAIN"
security_protocol = "SASL_PLAINTEXT"
username = "user1"

# Kafka consumer configuration
consumer = KafkaConsumer(
    'purchase_topic',
    bootstrap_servers=f'{KAFKA_IP}:9092',
    security_protocol=security_protocol,
    sasl_mechanism=sasl_mechanism,
    sasl_plain_username=username,
    sasl_plain_password=kafka_password,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)


def consume_messages():
    for message in consumer:
        data = message.value
        user_id = data.get('userID')
        item_id = data.get('id')
        if user_id and item_id:
            # Update the purchases list in MongoDB
            collection_user.update_one({'userID': user_id}, {'$push': {'purchases': item_id}})
        else:
            print("Invalid purchase data:", data)


def get_purchases(user_id):
    if not user_id:
        return jsonify({'status': 'error', 'message': 'No userID provided'}), 400

    user = collection_user.find_one({'userID': user_id}, {'_id': 0, 'purchases': 1})
    if user:
        purchase_ids = user.get('purchases', [])
        if purchase_ids:
            items = list(collection_items.find({'id': {'$in': purchase_ids}}, {'_id': 0}))
            print(items)
            return jsonify(items)
        return jsonify([])
    return jsonify({'status': 'error', 'message': 'User not found'}), 404


@app.route('/items', methods=['GET'])
def get_items():
    items = list(collection_items.find({}, {'_id': 0}))
    return jsonify(items)


@app.route('/users', methods=['GET'])
def get_users():
    users = list(collection_user.find({}, {'_id': 0}))
    return jsonify(users)


@app.route('/get_user_by_id', methods=['GET'])
def get_user_by_id():
    user_id = request.args.get('userID')
    if not user_id:
        return jsonify({'status': 'error', 'message': 'No userID provided'}), 400
    user = collection_user.find_one({'userID': user_id}, {'_id': 0, 'purchases': 1})
    if user:
        purchase_ids = user.get('purchases', [])
        if purchase_ids:
            items = list(collection_items.find({'id': {'$in': purchase_ids}}, {'_id': 0}))
            return jsonify(items)
        return jsonify([])
    return jsonify({'status': 'error', 'message': 'User not found'}), 404

threading.Thread(target=consume_messages, daemon=True).start()

if __name__ == '__main__':
    # Start Kafka consumer in a separate thread
    app.run(host='0.0.0.0', port=5000)
