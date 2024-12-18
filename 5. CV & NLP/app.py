from flask import Flask, request, render_template, jsonify
from utils.preprocess import *
from utils.classify import *
from utils.summarize import *
from utils.utils import * 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({"error": "Empty image filename"}), 400
    
    if image_file:
        image_bytes = image_file.read()
        image = Image.open(BytesIO(image_bytes))
        image.save('static/uploaded_image.png') 

        ocr_engine = request.form.get('ocr_engine')
        abstractive_summarization_model = request.form.get('abstractive_summarization')

        text = get_text_from_ocr(image_bytes, ocr_engine)
        abstractive_summarized_news = get_abstractive_summary(text, abstractive_summarization_model)


        # Preprocess the text and classify it
        classification_result = classify_news(text)

        # Summarize
        extractive_summarized_news = extractive_summarize(text)

        return render_template('result.html', text=text, classification_result=classification_result, extractive_summarized_news = extractive_summarized_news,abstractive_summarized_news = abstractive_summarized_news, image_url='static/uploaded_image.png')

if __name__ == '__main__':
    app.run(debug=True)