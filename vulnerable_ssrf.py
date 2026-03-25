import ipaddress
import socket
from urllib.parse import urlparse

import requests
from flask import Flask, request, abort
import urllib.request

ALLOWED_HOSTS = {
    "api.example.com",
    "cdn.example.com",
    "images.example.com",
    "hooks.example.com",
    "metadata.example.com",
}

ALLOWED_SCHEMES = ("http", "https")


def _validate_url(url, allowed_hosts=None):
    """Validate that a URL uses an allowed scheme and host, and does not
    resolve to a private/internal IP address.

    Returns the parsed URL on success; calls ``abort(400)`` on failure.
    """
    if allowed_hosts is None:
        allowed_hosts = ALLOWED_HOSTS

    if not url:
        abort(400, description="Missing URL parameter")

    try:
        parsed = urlparse(url)
    except Exception:
        abort(400, description="Invalid URL")

    if parsed.scheme not in ALLOWED_SCHEMES:
        abort(400, description="URL scheme not allowed")

    if parsed.hostname not in allowed_hosts:
        abort(400, description="URL host not allowed")

    # Prevent DNS-rebinding: resolve the hostname and reject private IPs
    try:
        resolved_ip = socket.getaddrinfo(parsed.hostname, None)[0][4][0]
        if ipaddress.ip_address(resolved_ip).is_private:
            abort(400, description="URL resolves to a private address")
    except socket.gaierror:
        abort(400, description="Could not resolve URL host")

    return parsed


app = Flask(__name__)


@app.route('/fetch')
def fetch_url():
    url = request.args.get('url')
    _validate_url(url)

    response = requests.get(url)
    return response.text


@app.route('/proxy')
def proxy_request():
    target_url = request.args.get('target')
    _validate_url(target_url)

    data = urllib.request.urlopen(target_url).read()
    return data


@app.route('/webhook', methods=['POST'])
def webhook():
    callback_url = request.json.get('callback_url')
    _validate_url(callback_url, allowed_hosts={"hooks.example.com", "api.example.com"})

    response = requests.post(callback_url, json={'status': 'success'})
    return f"Webhook sent: {response.status_code}"


@app.route('/image')
def load_image():
    image_url = request.args.get('url')
    _validate_url(image_url, allowed_hosts={"images.example.com", "cdn.example.com"})

    img_data = requests.get(image_url).content
    return img_data


def fetch_remote_resource(resource_url):
    _validate_url(resource_url)
    with urllib.request.urlopen(resource_url) as response:
        return response.read()


@app.route('/metadata')
def fetch_metadata():
    metadata_url = request.args.get('metadata_url')
    _validate_url(metadata_url, allowed_hosts={"api.example.com", "metadata.example.com"})

    metadata = requests.get(metadata_url, timeout=5).json()
    return metadata


def download_file(file_url):
    _validate_url(file_url)
    response = requests.get(file_url, stream=True)
    with open('downloaded_file', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


if __name__ == '__main__':
    app.run(debug=True)
