from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import shutil
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tempfile import NamedTemporaryFile

# Initialize FastAPI app
app = FastAPI()

# Label dictionary
label_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,
              'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16,
              'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24,
              'z': 25, 'empty': 26}

# Load the model
model_path = "braille1.h5"  # Update with your model path
model = load_model(model_path)

def process_and_crop_image(image_path, output_dir, target_size=(32, 32)):
    os.makedirs(output_dir, exist_ok=True)
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((20, 10), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bounding_boxes = []
    max_width = 0
    max_height = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if 10 < w < 100 and 10 < h < 100:
            bounding_boxes.append((x, y, x + w, y + h))
            max_width = max(max_width, w)
            max_height = max(max_height, h)

    bounding_boxes.sort(key=lambda box: (box[1], box[0]))
    bars = []
    current_bar = []
    last_y = bounding_boxes[0][1]
    bar_threshold = 20

    for box in bounding_boxes:
        x1, y1, x2, y2 = box
        if abs(y1 - last_y) < bar_threshold:
            current_bar.append(box)
        else:
            bars.append(sorted(current_bar, key=lambda b: b[0]))
            current_bar = [box]
        last_y = y1
    bars.append(sorted(current_bar, key=lambda b: b[0]))

    cropped_images = []

    for bar_idx, bar in enumerate(bars, 1):
        for col_idx, box in enumerate(bar, 1):
            x1, y1, x2, y2 = box
            new_x2 = x1 + max_width
            new_y2 = y1 + max_height
            cropped_image = image[y1:new_y2, x1:new_x2]
            resized_image = cv2.resize(cropped_image, target_size)
            cropped_images.append(resized_image)
            filename = f'{output_dir}/braille_letter_bar_{bar_idx:03d}_col_{col_idx:03d}.jpg'
            cv2.imwrite(filename, resized_image)

    return cropped_images

def load_and_process_image(image_path, target_size=(28, 28)):
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_image(model, image_path, label_dict):
    img_array = load_and_process_image(image_path)
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction)
    reverse_label_dict = {v: k for k, v in label_dict.items()}
    return reverse_label_dict[predicted_class]

def organize_predictions(predictions):
    organized = {}
    for image_file, predicted_label in predictions.items():
        try:
            parts = image_file.split('_')
            row = int(parts[3].replace("bar", ""))
            col = int(parts[5].replace("col", "").split('.')[0])
            if row not in organized:
                organized[row] = []
            organized[row].append((col, predicted_label))
        except (IndexError, ValueError):
            print(f"Skipping file with invalid format: {image_file}")

    sorted_text = []
    for row in sorted(organized.keys()):
        organized[row].sort(key=lambda x: x[0])
        sorted_text.append("".join([label for _, label in organized[row]]))

    return sorted_text

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Save uploaded image to temporary file
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.write(await file.read())
        temp_file.close()

        # Directory for cropped images
        output_dir = "/tmp/cropped_images"
        os.makedirs(output_dir, exist_ok=True)

        # Process and crop the uploaded image
        process_and_crop_image(temp_file.name, output_dir)

        # Predict labels for cropped images
        predictions = {}
        for image_file in sorted(os.listdir(output_dir)):
            if image_file.endswith(('.jpg', '.png')):
                image_path = os.path.join(output_dir, image_file)
                predicted_label = predict_image(model, image_path, label_dict)
                predictions[image_file] = predicted_label

        # Organize predictions into rows of text
        sorted_text = organize_predictions(predictions)

        # Cleanup temporary files
        os.remove(temp_file.name)
        shutil.rmtree(output_dir)

        return JSONResponse(content={"predicted_text": sorted_text})

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
