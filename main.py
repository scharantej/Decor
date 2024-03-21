
# Libraries
from flask import Flask, request, redirect, url_for, render_template
import numpy as np
from PIL import Image
import io
from io import BytesIO
from tensorflow.keras.models import load_model

# Load the AI interior design model
model = load_model('interior_design_model.h5')

# Create the Flask application
app = Flask(__name__)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Upload photo and process
@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    # Get the uploaded photo
    photo = request.files['photo']

    # Preprocess the photo
    image = Image.open(BytesIO(photo.read()))
    image = image.resize((224, 224))
    image = np.array(image) / 255.0

    # Predict the interior design suggestions
    suggestions = model.predict(np.expand_dims(image, axis=0))

    # Redirect to the results page
    return redirect(url_for('results', suggestions=suggestions))

# Results page
@app.route('/results')
def results():
    # Get the interior design suggestions
    suggestions = request.args.get('suggestions')
    suggestions = [int(suggestion) for suggestion in suggestions.split(',')]

    # Get the image names
    image_names = ['image1.jpg', 'image2.jpg', 'image3.jpg']

    # Render the results page
    return render_template('results.html', image_names=image_names, suggestions=suggestions)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
