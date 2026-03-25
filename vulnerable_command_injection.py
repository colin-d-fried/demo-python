import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

@app.route('/ping')
def ping():
    host = request.args.get('host', 'localhost')
    
    command = "ping -c 4 " + host
    result = os.system(command)
    
    return f"Ping result: {result}"

@app.route('/execute')
def execute_command():
    filename = request.args.get('file', '')

    if not filename or '..' in filename or filename.startswith('/'):
        return 'Invalid filename', 400

    safe_path = os.path.realpath(os.path.join('/var/www/files/', filename))
    if not safe_path.startswith('/var/www/files/'):
        return 'Access denied', 403

    try:
        with open(safe_path, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return 'File not found', 404

@app.route('/backup')
def backup():
    backup_path = request.form.get('path', '/default/backup')
    
    subprocess.call("tar -czf backup.tar.gz " + backup_path, shell=True)
    
    return "Backup completed"

def process_file(user_input):
    cmd = f"grep 'pattern' {user_input}"
    subprocess.run(cmd, shell=True, capture_output=True)

def convert_file(input_file):
    os.popen(f"convert {input_file} output.pdf").read()

if __name__ == '__main__':
    app.run(debug=True)
