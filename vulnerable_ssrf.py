import ipaddress
import socket
from urllib.parse import urlparse, urlunparse

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

    Returns a reconstructed URL built from the parsed components so the
    original tainted input is never passed to HTTP clients.
    Calls ``abort(400)`` on validation failure.
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

    # Resolve the hostname and reject private/internal IPs across ALL records
    # to prevent DNS-rebinding and multi-record bypass attacks.
    try:
        addr_infos = socket.getaddrinfo(parsed.hostname, None)
    except socket.gaierror:
        abort(400, description="Could not resolve URL host")

    if not addr_infos:
        abort(400, description="Could not resolve URL host")

    for addr_info in addr_infos:
        resolved_ip = addr_info[4][0]
        if ipaddress.ip_address(resolved_ip).is_private:
            abort(400, description="URL resolves to a private address")

    # Pin the first resolved public IP in the URL so the HTTP client cannot
    # re-resolve the hostname to a different (potentially private) address.
    pinned_ip = addr_infos[0][4][0]
    pinned_netloc = (
        f"{pinned_ip}:{parsed.port}" if parsed.port
        else pinned_ip
    )
    safe_url = urlunparse(parsed._replace(netloc=pinned_netloc))
    return safe_url, parsed.hostname


app = Flask(__name__)


@app.route('/fetch')
def fetch_url():
    url = request.args.get('url')
    safe_url, original_host = _validate_url(url)

    response = requests.get(safe_url, headers={"Host": original_host})
    return response.text


@app.route('/proxy')
def proxy_request():
    target_url = request.args.get('target')
    safe_url, original_host = _validate_url(target_url)

    req = urllib.request.Request(safe_url, headers={"Host": original_host})
    data = urllib.request.urlopen(req).read()
    return data


@app.route('/webhook', methods=['POST'])
def webhook():
    callback_url = request.json.get('callback_url')
    safe_url, original_host = _validate_url(
        callback_url, allowed_hosts={"hooks.example.com", "api.example.com"}
    )

    response = requests.post(
        safe_url, json={'status': 'success'}, headers={"Host": original_host}
    )
    return f"Webhook sent: {response.status_code}"


@app.route('/image')
def load_image():
    image_url = request.args.get('url')
    safe_url, original_host = _validate_url(
        image_url, allowed_hosts={"images.example.com", "cdn.example.com"}
    )

    img_data = requests.get(safe_url, headers={"Host": original_host}).content
    return img_data


def fetch_remote_resource(resource_url):
    safe_url, original_host = _validate_url(resource_url)
    req = urllib.request.Request(safe_url, headers={"Host": original_host})
    with urllib.request.urlopen(req) as response:
        return response.read()


@app.route('/metadata')
def fetch_metadata():
    metadata_url = request.args.get('metadata_url')
    safe_url, original_host = _validate_url(
        metadata_url, allowed_hosts={"api.example.com", "metadata.example.com"}
    )

    metadata = requests.get(
        safe_url, timeout=5, headers={"Host": original_host}
    ).json()
    return metadata


def download_file(file_url):
    safe_url, original_host = _validate_url(file_url)
    response = requests.get(
        safe_url, stream=True, headers={"Host": original_host}
    )
    with open('downloaded_file', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


if __name__ == '__main__':
    app.run(debug=True)
