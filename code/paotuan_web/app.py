from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# 游戏数据，仅作示例
dungeon = {
    'rooms': [
        {'id': 1, 'name': 'Room 1', 'description': 'This is room 1'},
        {'id': 2, 'name': 'Room 2', 'description': 'This is room 2'},
        {'id': 3, 'name': 'Room 3', 'description': 'This is room 3'},
    ],
    'player': {'name': 'Player', 'health': 100, 'attack': 10, 'defense': 5}
}


@app.route('/')
def index():
    return render_template('index.html', player=dungeon['player'], rooms=dungeon['rooms'])


@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    return jsonify(dungeon['rooms'])


@app.route('/api/player', methods=['GET'])
def get_player():
    return jsonify(dungeon['player'])


@app.route('/api/player/move', methods=['POST'])
def move_player():
    room_id = request.json.get('room_id')
    # 处理玩家移动逻辑，仅作示例
    for room in dungeon['rooms']:
        if room['id'] == room_id:
            return jsonify({'message': f'Player moved to {room["name"]}'})
    return jsonify({'message': 'Room not found'})


if __name__ == '__main__':
    app.run()
