# 🚗 Vehicle Damage Detection App


### Project Overview

This project develops an automated vehicle damage detection system based on deep learning, designed to classify the condition of a vehicle’s front and rear into six predefined categories. The solution integrates a trained deep learning model with a Streamlit application, enabling fast, accurate, and user-friendly damage assessment. By automating the inspection process, the system helps VROOM Cars improve the efficiency, consistency, and reliability of vehicle evaluations while providing a scalable foundation for future enhancements.


### Business Problem

* Manual vehicle damage inspection is time-consuming, labor-intensive, and prone to human error, leading to inconsistent assessments.
* VROOM Cars requires a faster, more reliable, and standardized vehicle damage evaluation process.


### Deliverables

* A trained deep learning model for car damage detection along with the complete source code.
* A model that achieves a minimum classification accuracy of **75%**.
* A Streamlit web application that allows users to upload or drag and drop a car image.
* Real-time prediction of the uploaded image into one of the following six categories:

  * Front Normal
  * Front Breakage
  * Front Crushed
  * Rear Normal
  * Rear Breakage
  * Rear Crushed
  

* An intuitive and user-friendly interface for efficient vehicle damage assessment.


![app_screenshot](app_screenshot3.png)

---

### Model Details

- **Model:** ResNet50 (Transfer Learning)
- **Training Images:** Approximately 2,300
- **Number of Classes:** 6

### Damage Classes

- Front Normal
- Front Crushed
- Front Breakage
- Rear Normal
- Rear Crushed
- Rear Breakage

### Model Performance

- **Validation Accuracy:** ~80%

---
### Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---
### Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser.

---
### Technologies Used

* **Python** – Core programming language for model development and application.
* **PyTorch** – Deep learning framework used for training and inference.
* **Torchvision** – Provides pre-trained models (ResNet50) and image preprocessing utilities.
* **ResNet50** – Pre-trained convolutional neural network used for transfer learning.
* **Streamlit** – Framework for building the interactive web application.
* **Pillow (PIL)** – Image processing library for loading and handling uploaded images.

---
### Project Workflow

1. Upload a car image.
2. The image is preprocessed.
3. The trained ResNet50 model predicts the damage category.
4. The predicted damage type is displayed on the screen.

---
### Notes

- Upload clear, high-quality images.
- Best results are obtained with third-quarter front or rear views.
- Performance may decrease for side views, top views, or heavily occluded vehicles.