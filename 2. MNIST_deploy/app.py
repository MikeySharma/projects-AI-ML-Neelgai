from flask import Flask, render_template, request, redirect, url_for
from PIL import Image

from utils.classify import classify_image
from utils.load_model import load_model

app = Flask(__name__)

# Loading SVC model
svc = load_model()    


# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for image upload and prediction
@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        image = Image.open(file)
        prediction = classify_image(image,svc)
        image.save('static/uploaded_image.png') 
        return redirect(url_for('result', prediction=prediction))

# Route for displaying the result
@app.route('/result')
def result():
    prediction = request.args.get('prediction')
    return render_template('result.html', prediction=prediction, image_url='static/uploaded_image.png')

if __name__ == '__main__':
    app.run(debug=True)