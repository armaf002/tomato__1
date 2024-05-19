import requests
from io import BytesIO
from PIL import Image

PREDICTION_KEY = '16d8a257351c45a6bfb3ec48c78f7a24'
ENDPOINT_URL_IMAGE = 'https://tomatodiseaseclassifier-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/39ffcd65-40e5-486c-9ca3-5dbbf9f05d32/classify/iterations/Iteration3/image'
ENDPOINT_URL_URL = 'https://tomatodiseaseclassifier-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/39ffcd65-40e5-486c-9ca3-5dbbf9f05d32/classify/iterations/Iteration3/url'

def classify_tomato_disease(image_file=None, image_url=None):
    headers = {
        'Prediction-Key': PREDICTION_KEY
    }
    
    if image_file:
        headers['Content-Type'] = 'application/octet-stream'
        img_byte_arr = BytesIO()
        image = Image.open(image_file.stream)
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        response = requests.post(ENDPOINT_URL_IMAGE, headers=headers, data=img_byte_arr)
    
    elif image_url:
        headers['Content-Type'] = 'application/json'
        data = {"Url": image_url}
        response = requests.post(ENDPOINT_URL_URL, headers=headers, json=data)
    
    else:
        return 'No image file or URL provided'
    
    if response.status_code == 200:
        result = response.json()
        predictions = result['predictions']
        highest_prob = max(predictions, key=lambda x: x['probability'])
        return highest_prob['tagName']
    else:
        return f'Error: {response.status_code}, {response.text}'

