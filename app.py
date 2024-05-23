from flask import Flask, request, render_template, flash, redirect, url_for
from custom_vision import classify_tomato_disease
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Use a secure secret key for production

OPENAI_ENDPOINT = os.getenv('OPENAI_ENDPOINT', 'https://TomatoDiseaseClassifier.openai.azure.com/openai/deployments/gpt-35-turbo-16k/chat/completions?api-version=2023-03-15-preview')
OPENAI_KEY = os.getenv('OPENAI_KEY', '34fd03f1f03c41cb8ee3fdcf6ccd03f1')

def generate_response(question):
    headers = {
        'Content-Type': 'application/json',
        'api-key': OPENAI_KEY
    }
    data = {
        'messages': [
            {'role': 'system', 'content': 'You are an expert in tomato plant diseases. Provide detailed information about the diseases, symptoms, causes, and control measures.'},
            {'role': 'user', 'content': question}
        ],
        'temperature': 0.7,
    }
    response = requests.post(OPENAI_ENDPOINT, json=data, headers=headers)
    if response.status_code == 200:
        raw_response = response.json().get('choices', [{}])[0].get('message', {}).get('content', 'No response available')
        return raw_response
    else:
        return f'Error occurred: {response.status_code}, {response.text}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('file')
    url = request.form.get('url')
    
    if not file and not url:
        flash('Please upload an image or enter an image URL.', 'error')
        return redirect(url_for('index'))

    if file and file.filename == '':
        flash('Please select a valid image file.', 'error')
        return redirect(url_for('index'))
    
    diagnosis = classify_tomato_disease(image_file=file, image_url=url)
    if not diagnosis:
        flash('Error occurred while processing the image. Please try again.', 'error')
        return redirect(url_for('index'))
    
    return render_template('index.html', diagnosis=diagnosis)

@app.route('/generate', methods=['POST'])
def generate():
    question = request.form.get('question')
    tomato_disease_keywords = ['tomato', 'disease', 'blight', 'leaf curl', 'septoria leaf spot', 'verticillium wilt']
    
    if any(keyword in question.lower() for keyword in tomato_disease_keywords):
        response = generate_response(question)
        return render_template('index.html', generated_response=response, question=question)
    else:
        flash('Please ask a question related to tomato diseases.', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
