from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Serves frontend

@app.route('/api/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    tag = request.json.get('tag')
    attributes = request.json.get('attributes')
    
    if not url or not tag or not attributes:
        return jsonify({"error": "Missing required parameters"}), 400

    scrape_target = requests.get(url)
    soup = BeautifulSoup(scrape_target.content, 'html.parser')
    scrape_tag = soup.find_all(tag, attrs={"class": attributes})
    
    results = []
    for element in scrape_tag:
        text = element.text
        results.append({"data": text})
    
    return jsonify(results)

@app.route('/api/scrape/csv', methods=['POST'])
def scrape_csv():
    url = request.json.get('url')
    tag = request.json.get('tag')
    attributes = request.json.get('attributes')
    
    if not url or not tag or not attributes:
        return jsonify({"error": "Missing required parameters"}), 400

    scrape_target = requests.get(url)
    soup = BeautifulSoup(scrape_target.content, 'html.parser')
    scrape_tag = soup.find_all(tag, attrs={"class": attributes})
    
    results = []
    for element in scrape_tag:
        text = element.text
        results.append({"data": text})
    
    df = pd.DataFrame(results)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return app.response_class(output, mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=scraped_data.csv"})

if __name__ == '__main__':
    app.run(debug=True)
