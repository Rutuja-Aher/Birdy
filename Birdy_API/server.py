from flask import Flask, jsonify
import json
app = Flask(__name__)

with open('../constants/birds.json', 'r') as file:
    birds_data = json.load(file)

@app.route('/bird/<int:bird_id>', methods=['GET'])
def get_bird_by_id(bird_id):
    bird = next((b for b in birds_data if b['id'] == bird_id), None)

    if bird:
        return jsonify(bird), 200
    else:
        return jsonify({'error': 'Bird not found'}), 404

if __name__ == '__main__':
    app.run(port=5000)
