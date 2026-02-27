from flask import Flask, jsonify, send_from_directory, request
from word_search_generator import generate_word_search

app = Flask(__name__, static_folder='../frontend')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/wordsearch/<subject>')
def get_word_search(subject):
    num_words = request.args.get('num_words', default=10, type=int)
    return jsonify(generate_word_search(subject, num_words))

if __name__ == '__main__':
    app.run(debug=True)
