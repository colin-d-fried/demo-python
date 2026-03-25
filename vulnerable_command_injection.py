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
    
    os.system(f"cat {filename}")
    
    return "Command executed"

@app.route('/backup')
def backup():
    backup_path = request.form.get('path', '/default/backup')
    
    subprocess.call("tar -czf backup.tar.gz " + backup_path, shell=True)
    
    return "Backup completed"

def process_file(user_input):
    cmd = f"grep 'pattern' {user_input}"
    subprocess.run(cmd, shell=True, capture_output=True)

def convert_file(input_file):
    safe_path = os.path.realpath(input_file)
    if not os.path.isfile(safe_path):
        return None
    result = subprocess.run(["convert", safe_path, "output.pdf"], capture_output=True)
    return result.stdout

if __name__ == '__main__':
    app.run(debug=True)
