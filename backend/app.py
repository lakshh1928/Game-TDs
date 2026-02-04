from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Use Environment Variable for DB URI (Crucial for DevOps)
DB_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://root:password@db/tds_db')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

@app.route('/api/players', methods=['GET'])
def get_players():
    players = Player.query.all()
    return jsonify([p.name for p in players]), 200

@app.route('/api/players', methods=['POST'])
def add_player():
    data = request.json
    try:
        new_player = Player(name=data['name'])
        db.session.add(new_player)
        db.session.commit()
        return jsonify({"message": "Player added"}), 201
    except:
        return jsonify({"error": "Exists or DB error"}), 400

@app.route('/api/players/<name>', methods=['DELETE'])
def delete_player(name):
    player = Player.query.filter_by(name=name).first()
    if player:
        db.session.delete(player)
        db.session.commit()
        return jsonify({"message": "Removed"}), 200
    return jsonify({"message": "Not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
