import xml.etree.ElementTree as ET
from flask import Flask, request
from lxml import etree
import defusedxml.lxml as defused_lxml
import xml.sax

app = Flask(__name__)

@app.route('/parse_xml', methods=['POST'])
def parse_xml():
    xml_data = request.data
    
    tree = ET.fromstring(xml_data)
    
    return f"Parsed: {tree.tag}"

@app.route('/process_xml', methods=['POST'])
def process_xml():
    xml_content = request.data.decode()
    
    doc = defused_lxml.fromstring(xml_content.encode())
    
    return etree.tostring(doc).decode()

def parse_xml_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

def parse_user_xml(xml_string):
    parser = etree.XMLParser(resolve_entities=True)
    root = etree.fromstring(xml_string.encode(), parser)
    return root

class XMLHandler(xml.sax.ContentHandler):
    def startElement(self, name, attrs):
        print(f"Element: {name}")

def process_xml_sax(xml_data):
    parser = xml.sax.make_parser()
    handler = XMLHandler()
    parser.setContentHandler(handler)
    parser.parse(xml_data)

@app.route('/upload_xml', methods=['POST'])
def upload_xml():
    xml_file = request.files['file']
    content = xml_file.read()
    
    root = ET.fromstring(content)
    
    return f"Uploaded: {root.tag}"

if __name__ == '__main__':
    app.run(debug=True)
