from flask import Flask, request, render_template
from custom_vision import classify_tomato_disease

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files and 'url' not in request.form:
        return 'No file or URL part'
    
    file = request.files.get('file')
    url = request.form.get('url')
    
    if file and file.filename != '':
        diagnosis = classify_tomato_disease(image_file=file)
    elif url and url != '':
        diagnosis = classify_tomato_disease(image_url=url)
    else:
        return 'No selected file or URL'
    
    return render_template('index.html', diagnosis=diagnosis)

if __name__ == '__main__':
    app.run(debug=True)

