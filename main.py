# Imports
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware 
import tensorflow as tf
from PIL import Image
import numpy as np
import io

from utils import preprocess_image, get_color_map

# FastAPI instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://segmend-moon-terrain.streamlit.app/"],  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load the pre-trained model for segmentation
model_path = 'model/LunarModel.h5'
model = tf.keras.models.load_model(model_path, compile=False)

# Endpoint 1 - read root
@app.get('/')
async def read_root():
    return {'App': "Running"}

# Endpoint 2 - preprocess image
@app.post('/preprocess/')
async def preprocess_image_endpoint(file: UploadFile = File(...)):
    try:
        # Read the image file into a BytesIO object
        image_bytes = await file.read()
        image_file = io.BytesIO(image_bytes)

        # Preprocess the image
        image_array = preprocess_image(image_file)
        print(image_array.shape)

        # Convert the preprocessed image to a PIL Image
        preprocessed_pil_image = Image.fromarray((image_array * 255).astype(np.uint8))

        # Save the preprocessed image to a BytesIO object
        preprocessed_img_byte_arr = io.BytesIO()
        preprocessed_pil_image.save(preprocessed_img_byte_arr, format='PNG')
        preprocessed_img_byte_arr.seek(0)

        return StreamingResponse(preprocessed_img_byte_arr, media_type='image/png')

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Endpoint 3 - segment image
@app.post('/segment/')
async def segment_lunar_terrain(file: UploadFile = File(...)):
    try:
        # Read the preprocessed image file into a BytesIO object
        image_bytes = await file.read()
        image_file = io.BytesIO(image_bytes)

        # Load the image as a numpy array
        preprocessed_image = Image.open(image_file)
        image_array = np.array(preprocessed_image) / 255.0  # Ensure the image is normalized

        # Perform segmentation using the loaded lunar model
        pred_mask = model.predict(np.expand_dims(image_array, axis=0))
        pred_mask = np.argmax(pred_mask, axis=-1)
        pred_mask = pred_mask[0]

        # Get color map and apply to pred_mask
        color_map = get_color_map()
        pred_mask = color_map[pred_mask]

        # Convert the predicted mask to a PIL Image
        segmented_pil_image = Image.fromarray(pred_mask)

        # Save the segmented image to a BytesIO object
        segmented_img_byte_arr = io.BytesIO()
        segmented_pil_image.save(segmented_img_byte_arr, format='PNG')
        segmented_img_byte_arr.seek(0)

        return StreamingResponse(segmented_img_byte_arr, media_type='image/png')

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)