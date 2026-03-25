from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/admin/users')
def get_all_users():
    users = [
        {'id': 1, 'username': 'admin', 'email': 'admin@example.com'},
        {'id': 2, 'username': 'user1', 'email': 'user1@example.com'}
    ]
    return jsonify(users)

@app.route('/admin/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return jsonify({'message': f'User {user_id} deleted'})

@app.route('/api/sensitive_data')
def get_sensitive_data():
    data = {
        'ssn': '123-45-6789',
        'credit_card': '4532-1234-5678-9010',
        'salary': 150000
    }
    return jsonify(data)

@app.route('/config')
def get_config():
    config = {
        'database_url': 'postgresql://admin:password@localhost/db',
        'api_keys': ['key1', 'key2', 'key3'],
        'secret_key': 'my-secret-key'
    }
    return jsonify(config)

@app.route('/admin/settings', methods=['POST'])
def update_settings():
    new_settings = request.json
    return jsonify({'message': 'Settings updated', 'settings': new_settings})

@app.route('/user/<int:user_id>/financial')
def get_financial_info(user_id):
    financial_data = {
        'account_balance': 50000,
        'transactions': ['payment1', 'payment2']
    }
    return jsonify(financial_data)

@app.route('/debug/logs')
def get_debug_logs():
    logs = [
        'User admin logged in from 192.168.1.1',
        'Password reset for user@example.com',
        'API key abc123 used'
    ]
    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True)
