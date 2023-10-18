import os
import pytesseract
from PIL import Image
from flask import Flask, request, render_template, jsonify
import re
import cv2
import numpy as np
from werkzeug.utils import secure_filename


app = Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def preprocess_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to enhance text
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Save the preprocessed image for reference
    preprocessed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preprocessed_image.png')
    cv2.imwrite(preprocessed_image_path, thresh)
    
    return preprocessed_image_path

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/extract', methods=['POST'])
def extract_name_from_aadhar():
    # Ensure the request contains an image file
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image = request.files['image']
    
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Save the uploaded image to the upload folder
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename))
        image.save(image_path)
        
        # Preprocess the image to enhance OCR accuracy
        preprocessed_image_path = preprocess_image(image_path)
        
        # Perform OCR on the preprocessed image
        text = pytesseract.image_to_string(Image.open(preprocessed_image_path))
        lines = text.split('\n')

        # Remove any empty lines from the list
        lines = [line.strip() for line in lines if line.strip()]

        # Print the list of lines
        for line in lines:
            print(line)
        
        pattern = r'\d+\.\d+'

        matches = re.findall(pattern, text)

        extracted_values = [float(match) for match in matches]

      
        print(extracted_values)
        if extracted_values:
            print(extracted_values)
            return jsonify({'text': extracted_values})
        else:
            return jsonify({'error': 'Na ho payega'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500    
    
if __name__ == '__main__':
    app.run(debug=True)