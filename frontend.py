import streamlit as st
import requests
from PIL import Image
import io

# Set up the Streamlit page
st.set_page_config(
    page_title="Segment Moon",
    page_icon="🌕",
    layout="wide"
)

# Background CSS for adding a background image
background_image_url = "https://www.sott.net/image/s27/554081/full/ARnG8wPtoSYVQJVtS9q7WR_2069_80.jpg"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown('<h1 style="color: lightgray;">🌙 Lunar Terrain Segmentation App</h1>', unsafe_allow_html=True)


# FastAPI backend endpoints
PREPROCESS_URL = "http://localhost:8000/preprocess/"
SEGMENT_URL = "http://localhost:8000/segment/"

# Initialize session state for storing images
if 'preprocessed_image' not in st.session_state:
    st.session_state['preprocessed_image'] = None
if 'segmented_image' not in st.session_state:
    st.session_state['segmented_image'] = None
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None

# Upload an image
uploaded_file = st.file_uploader("Upload an image of the moon's surface which must be at least 480x480 pixels:-", type=["jpg", "jpeg", "png", "bmp"])

# Clear session state when a new file is uploaded
if uploaded_file is not None:
    if st.session_state['uploaded_file'] != uploaded_file:
        # New file uploaded, clear previous state
        st.session_state['uploaded_file'] = uploaded_file
        st.session_state['preprocessed_image'] = None
        st.session_state['segmented_image'] = None

    # Step 1: Automatically preprocess the image upon upload
    if st.session_state['preprocessed_image'] is None:
        with st.spinner("Processing..."):
            try:
                # Send the uploaded file to the preprocess endpoint
                files = {'file': uploaded_file.getvalue()}
                response = requests.post(PREPROCESS_URL, files=files)
                response.raise_for_status()  # Check for request errors

                # Load the preprocessed image from the response
                preprocessed_image = Image.open(io.BytesIO(response.content))
                st.session_state['preprocessed_image'] = preprocessed_image  # Store in session state

            except requests.exceptions.RequestException as e:
                st.error(f"Error during preprocessing: {e}")

# Only display the preprocessed image and the segmentation button if the image is processed
if st.session_state['preprocessed_image'] is not None:
    col1, col2 = st.columns(2)

    with col1:
        # Display the preprocessed image
        st.image(st.session_state['preprocessed_image'], caption="Preprocessed Image", use_container_width=True)
        
        # Show the "Segment This Image" button
        segment_button = st.button("Segment This Image")

    # Display the segmentation results in the second column only when the button is clicked
    with col2:
        if segment_button:
            # Show the spinner only while the segmentation process is going on
            with st.spinner("Segmenting..."):
                try:
                    # Convert the preprocessed image to bytes for sending to the backend
                    img_byte_arr = io.BytesIO()
                    st.session_state['preprocessed_image'].save(img_byte_arr, format='PNG')
                    img_byte_arr.seek(0)

                    # Send the preprocessed image to the segmentation endpoint
                    files = {'file': img_byte_arr.getvalue()}
                    response = requests.post(SEGMENT_URL, files=files)
                    response.raise_for_status()  # Check for request errors

                    # Load the segmented image from the response
                    segmented_image = Image.open(io.BytesIO(response.content))
                    st.session_state['segmented_image'] = segmented_image  # Store in session state

                except requests.exceptions.RequestException as e:
                    st.error(f"Error during segmentation: {e}")
        
        # If segmentation is done, display the segmented image on the right side
        if st.session_state['segmented_image'] is not None:
            st.image(st.session_state['segmented_image'], caption="Segmented Image", use_container_width=True)

# Add the footer at the end of the script
footer = """
<div style='position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; text-align: center; padding: 10px;'>
    <p style='color: black; margin: 0;'>This project is developed by <b>Spartificial</b> as part of the <b>Machine Learning for Astronomy</b> Training Program</p>
</div>
"""

# Inject the footer using markdown
st.markdown(footer, unsafe_allow_html=True)