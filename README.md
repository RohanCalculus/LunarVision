# 🌙 Segment Lunar Terrain using Computer Vision
Give input image of Moon Terrain which is at least 480x480 pixels and get the segmented mask as output.
* Note that, the segmentation mask will only include those rocks which might be dangerous for rover!

<img src="media/moon - Made with Clipchamp.gif" alt="Web App GIF" width=90%>

## ⚙️ How to Set Up This Project in Your System
1. Clone this repository using the web URL given below or download the ZIP file.
   ```bash
   git clone https://github.com/SpartificialUdemy/project_3.git
   ```

2. Create the virtual environment in your system:
   - **Windows**
   ```bash
   python -m venv venv
   ```
   - **Linux or Mac**
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**
   ```bash
   venv\Scripts\activate
   ```
   - **Linux or Mac**
   ```bash
   source venv/bin/activate
   ```

4. Install the requirements:
   - **Windows**
   ```bash
   python -m pip install -r requirements.txt
   ```
   - **Linux or Mac**
   ```bash
   pip install -r requirements.txt
   ```

5. Run the backend powered by FastAPI using Uvicorn:
   ```bash
   uvicorn main:app 
   ```

6. Run the frontend powered by Streamlit:
   ```bash
   streamlit run frontend.py
   ```

## 🔧 Tools used in This Project
1. **FastAPI** - To build the API endpoints
2. **Streamlit** - To build and host the frontend of the web application
3. **Keras** - To build the dataset pipeline, model, perform training and evaluation
4. **UNET**:- Architecture selected for performing Image Segmentation
5. **Transfer Learning** - Using SOTA backbone for UNET to get better results in no time 
6. **Matplotlib** - To visualize the cost vs iterations and in the web application to visualize the regression line
7. **Pandas** - To read CSV files, create the dataframe, and save dataframes back to CSV
8. **PIL** - For displaying image as output in FastAPI response and on Streamlit web app

## 💖 Acknowledgments
- Special thanks to the authors of the libraries used in this project.
  
## 📧 Contact
For questions or support, please reach out to [Instructors at Spartificial](https://mail.google.com/mail/?view=cm&fs=1&to=instructors@spartificial.com).
