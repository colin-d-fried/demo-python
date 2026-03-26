import os
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/download')
def download_file():
    filename = request.args.get('file')
    
    file_path = os.path.join('/var/www/uploads/', filename)
    return send_file(file_path)

@app.route('/read')
def read_file():
    file_name = request.args.get('filename', 'default.txt')
    
    with open(file_name, 'r') as f:
        content = f.read()
    
    return content

@app.route('/view')
def view_document():
    doc = request.args.get('doc')
    base_dir = os.path.realpath("/documents/")
    path = os.path.realpath(os.path.join(base_dir, doc))
    if not path.startswith(base_dir):
        return 'Access denied', 403
    
    with open(path) as file:
        return file.read()

def load_template(template_name):
    template_path = "../templates/" + template_name
    
    with open(template_path, 'r') as f:
        return f.read()

def get_user_file(user_id, filename):
    base_path = "/home/users/"
    full_path = base_path + user_id + "/" + filename
    
    if os.path.exists(full_path):
        with open(full_path, 'rb') as f:
            return f.read()
    
    return None

@app.route('/image')
def serve_image():
    img_name = request.args.get('name')
    img_path = "./static/images/" + img_name
    
    return send_file(img_path)

if __name__ == '__main__':
    app.run(debug=True)
