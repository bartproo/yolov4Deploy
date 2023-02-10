import base64
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import json

# Initialize Flask application
app = Flask(__name__)

# Load the YOLO class names
with open('data/coco.names', 'r') as f:
    classes = f.read().splitlines()

# Load the YOLO model
net = cv2.dnn.readNetFromDarknet('data/yolov4.cfg', 'data/yolov4.weights')
model = cv2.dnn_DetectionModel(net)

# Set input parameters for the model
model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)


# Function to convert Numpy objects to serializable objects
def convert_to_serializable(obj):
    if isinstance(obj, np.int32):
        return int(obj)
    if isinstance(obj, np.float32):
        return float(obj)


# Route to render the main HTML template
@app.route("/")
def index():
    return render_template("index.html")


# Route to handle image uploads
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the image in base64 format
        image_base64 = request.form.get('image')

        # Decode the base64 string to binary data
        image_binary = base64.b64decode(image_base64)

        # Convert the binary data to a OpenCV image
        img = cv2.imdecode(np.frombuffer(image_binary, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

        # Convert the image from RGBA to BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)

        # Run object detection on the image
        class_ids, scores, boxes = model.detect(img, confThreshold=0.6, nmsThreshold=0.4)

        # Prepare the results for serialization
        result = []
        for i, box in enumerate(boxes):
            result.append({
                'class_id': class_ids[i],
                'class_name': classes[class_ids[i]],
                'confidence': scores[i],
                'x_min': box[0],
                'y_min': box[1],
                'width': box[2],
                'height': box[3]
            })

        # Serialize the results
        json_result = json.dumps(result, default=convert_to_serializable)

        # Return the results as a JSON response
        return jsonify(json.loads(json_result))

    # exception handling code
    except Exception as e:
        return jsonify({"error": str(e)})


# Route to test api
@app.route('/upload', methods=['POST'])
def upload():
    # Return the results as a JSON response
    return "hi"

# Main method to run the application
if __name__ == "__main__":
    app.run(debug=False)
