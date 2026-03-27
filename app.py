from flask import Flask, render_template, request, jsonify
from agent import get_schemes

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-schemes', methods=['POST'])
def fetch_schemes():
    data = request.json
    
    language = data.get('language', 'english')
    state = data.get('state', '')
    category = data.get('category', '')
    age = data.get('age', '')
    problem = data.get('problem', '')
    
    result = get_schemes(language, state, category, age, problem)
    
    return jsonify({'response': result})

if __name__ == '__main__':
    app.run(debug=True)