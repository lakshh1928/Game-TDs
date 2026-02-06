from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import socket

app = Flask(__name__)
CORS(app)

DB_USER = os.getenv('MYSQL_USER')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_NAME = os.getenv('MYSQL_DATABASE')
DB_HOST = os.getenv('MYSQL_HOST')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

@app.route('/')
def home():
    container_id = socket.gethostname()
    return f"<h1>Hello from the TDS Game API!</h1><p>Served by Container: <b>{container_id}</b></p>"

@app.route('/api/players', methods=['GET'])
def get_players():
    players = Player.query.all()
    return jsonify([p.name for p in players]), 200

@app.route('/api/players', methods=['POST'])
def add_player():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "Name required"}), 400
    try:
        new_player = Player(name=data['name'])
        db.session.add(new_player)
        db.session.commit()
        return jsonify({"message": "Player added"}), 201
    except:
        return jsonify({"error": "Player already exists"}), 400

@app.route('/api/players/<name>', methods=['DELETE'])
def delete_player(name):
    player = Player.query.filter_by(name=name).first()
    if player:
        db.session.delete(player)
        db.session.commit()
        return jsonify({"message": "Removed"}), 200
    return jsonify({"message": "Not found"}), 404

@app.route('/health')
def health_check():
    try:
        db.session.execute('SELECT 1')
        return jsonify({"status": "Success", "container": socket.gethostname()}), 200
    except Exception as e:
        return jsonify({"status": "Error", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
