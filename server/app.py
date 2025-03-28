from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def messages():
    try:
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return make_response(jsonify([message.to_dict() for message in messages]), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.json  # Use JSON payload
    new_message = Message(
        body=data.get('body'),
        username=data.get('username')
    )
    db.session.add(new_message)
    db.session.commit()
    return make_response(jsonify(new_message.to_dict()), 201)

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    data = request.json  # Use JSON payload
    message = Message.query.filter_by(id=id).first()
    if message:
        message.body = data.get('body')
        db.session.commit()
        return make_response(jsonify(message.to_dict()), 200)
    return make_response(jsonify({'error': 'Message not found'}), 404)

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    try:
        message = Message.query.filter_by(id=id).first()
        if message:
            db.session.delete(message)
            db.session.commit()
            return make_response(jsonify({'message': f'Message {id} deleted successfully'}), 200)
        return make_response(jsonify({'error': 'Message not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(port=5555)
