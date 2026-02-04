from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database Configuration (Point this to your MySQL container later)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@db/tds_db'
db = SQLAlchemy(app)

# Database Model
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

@app.route('/api/players', methods=['GET'])
def get_players():
    players = Player.query.all()
    return jsonify([p.name for p in players])

@app.route('/api/players', methods=['POST'])
def add_player():
    data = request.json
    new_player = Player(name=data['name'])
    db.session.add(new_player)
    db.session.commit()
    return jsonify({"message": "Player added"}), 201

@app.route('/api/players/<name>', methods=['DELETE'])
def delete_player(name):
    player = Player.query.filter_by(name=name).first()
    if player:
        db.session.delete(player)
        db.session.commit()
    return jsonify({"message": "Player removed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)