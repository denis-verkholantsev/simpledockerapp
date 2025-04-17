from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from tenacity import retry, stop_after_attempt, wait_fixed

import os


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


@retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
def init_db():
    db.create_all()


@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    if not data.get('name'):
        return jsonify({'error': 'missing-argument'}), 400
    
    if not isinstance(data['name'], str):
        return jsonify({'error': 'wrong-type'}), 400

    if len(data['name']) > 100:
        return jsonify({"error": 'max-length-exceeded'}), 400
    
    item = Item(name=data['name'])
    db.session.add(item)
    db.session.commit()
    return jsonify({"id": item.id, "name": item.name}), 200


@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name} for item in items]), 200


@app.route('/items', methods=['DELETE'])
def delete_items():
    id = request.args.get('id', type=int)
    if not id:
        return jsonify({'error': 'missing-argument'}), 400
    
    try:
        item = db.session.get(Item, id)
        if not item:
            return jsonify({'error': 'not-found'}), 404

        db.session.delete(item)
        db.session.commit()
        return jsonify({'result': 'ok'}), 200
    except:
        db.session.rollback()
        return jsonify({'error': 'internal-error'}), 500


if __name__ == '__main__':
    with app.app_context():
        try:
            init_db()
        except Exception as e:
            print(f'Failed to connect to the database: {e}')

    app.run(host='0.0.0.0', port=5000)
