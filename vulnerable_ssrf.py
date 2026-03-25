import requests
from flask import Flask, request
from markupsafe import escape
import urllib.request

app = Flask(__name__)

@app.route('/fetch')
def fetch_url():
    url = request.args.get('url')
    
    response = requests.get(url)
    
    return str(escape(response.text))

@app.route('/proxy')
def proxy_request():
    target_url = request.args.get('target')
    
    data = urllib.request.urlopen(target_url).read()
    
    return data

@app.route('/webhook', methods=['POST'])
def webhook():
    callback_url = request.json.get('callback_url')
    
    response = requests.post(callback_url, json={'status': 'success'})
    
    return f"Webhook sent: {response.status_code}"

@app.route('/image')
def load_image():
    image_url = request.args.get('url')
    
    img_data = requests.get(image_url).content
    
    return img_data

def fetch_remote_resource(resource_url):
    with urllib.request.urlopen(resource_url) as response:
        return response.read()

@app.route('/metadata')
def fetch_metadata():
    metadata_url = request.args.get('metadata_url')
    
    metadata = requests.get(metadata_url, timeout=5).json()
    
    return metadata

def download_file(file_url):
    response = requests.get(file_url, stream=True)
    with open('downloaded_file', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

if __name__ == '__main__':
    app.run(debug=True)
