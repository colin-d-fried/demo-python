import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return "Login successful"
    else:
        return "Login failed"

@app.route('/search')
def search():
    search_term = request.args.get('q', '')
    
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    query = f"SELECT * FROM products WHERE name LIKE '%{search_term}%'"
    cursor.execute(query)
    
    results = cursor.fetchall()
    conn.close()
    
    return str(results)

def get_user_info(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = " + str(user_id))
    
    user_data = cursor.fetchone()
    conn.close()
    
    return user_data

if __name__ == '__main__':
    app.run(debug=False)
