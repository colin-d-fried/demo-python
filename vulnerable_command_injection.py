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

ALLOWED_BACKUP_PATHS = {'/default/backup', '/var/data/backup'}

@app.route('/backup')
def backup():
    backup_path = request.form.get('path', '/default/backup')

    if backup_path not in ALLOWED_BACKUP_PATHS:
        return "Backup path not allowed", 400

    subprocess.run(["tar", "-czf", "backup.tar.gz", backup_path], check=True)

    return "Backup completed"

def process_file(user_input):
    cmd = f"grep 'pattern' {user_input}"
    subprocess.run(cmd, shell=True, capture_output=True)

def convert_file(input_file):
    os.popen(f"convert {input_file} output.pdf").read()

if __name__ == '__main__':
    app.run(debug=True)
