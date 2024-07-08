import os
import sys
import numpy as np
from flask import Flask, request, render_template, redirect, send_from_directory
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing import image  # Correct import for image processing
from tensorflow.keras.models import load_model  # Correct import for loading the model

# Ensure UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
# Initialize the Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Path for uploaded files in static folder

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the pre-trained model
model = load_model('model/model1.keras')

# Define the class labels
class_labels = ['No Fracture', 'Fracture']


# Function to prepare the image
def prepare_image(file_path):
    img = image.load_img(file_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0
    return img


# Define the route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                # Debugging: Print the file path
                print(f"File saved to: {file_path}", file=sys.stderr)

                img = prepare_image(file_path)
                prediction = model.predict(img)
                predicted_class = class_labels[int(prediction[0][0] > 0.5)]

                # Debugging: Print the filename and prediction
                print(f"Filename for template: {filename}", file=sys.stderr)
                print(f"Prediction: {predicted_class}", file=sys.stderr)

                return render_template('index.html', img_path=filename, prediction=predicted_class)
            except Exception as e:
                print(f"Error: {str(e)}", file=sys.stderr)
                return redirect(request.url)

    return render_template('index.html')


# Route to serve files from the 'static/uploads' directory
@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)