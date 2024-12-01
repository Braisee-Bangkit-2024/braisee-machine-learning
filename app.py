from flask import Flask, request, jsonify
import cv2
import numpy as np
import tensorflow as tf
import os

app = Flask(__name__)

# Load TFLite model
MODEL_PATH = "model.tflite"
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

# Class mapping
CLASS_MAPPING = {
    0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j',
    10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's',
    19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z', 26: 'empty'
}

# Preprocessing function
def preprocess_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY_INV)
    binary_image = cv2.resize(binary_image, (28, 28))  # Resize to model input size
    normalized_image = binary_image / 255.0
    return np.expand_dims(normalized_image, axis=(0, -1))

# Inference function
def predict_braille(image):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], image.astype(np.float32))
    interpreter.invoke()

    predictions = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = np.argmax(predictions)
    confidence = np.max(predictions)

    return predicted_class, confidence

# Route to process image
@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    image = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Preprocess the image
    processed_image = preprocess_image(image)

    # Predict using the model
    predicted_class, confidence = predict_braille(processed_image)

    # Map class to character
    if confidence > 0.5:  # Threshold for confidence
        character = CLASS_MAPPING.get(predicted_class, "unknown")
        return jsonify({"character": character, "confidence": float(confidence)})
    else:
        return jsonify({"error": "Low confidence in prediction"}), 400

if __name__ == '__main__':
    # Run locally for testing
    app.run(host='0.0.0.0', port=8080)
