<h1>Ingredient Scanner</h1>

<h2>Setup</h2>

<b>To run this project, install the necessary libraries:</b>

pip install pytesseract

pip install opencv-python

pip install nltk

pip install pandas

<b>How to change image for analysis</b>

To analyze a different product image, upload your image to the ./images path and update the "image_path" variable to your image's file name. Images should be .png or .jpg/jpeg files.

<h2>About</h2>

This project utilizes image processing techniques along with ingredient analysis from the Cosmily API to provide an in-depth analysis of a product's ingredients.

Developed by Gali Deutsch and Nicholas Bogdanovic.

<h2>Technologies</h2> 

* pytesseract and OpenCV for OCR
* Cosmily API to retrieve EWG data and analysis: https://docs.cosmily.com/
* Pandas
* NLTK

<h2>To Do</h2>

Given more time the following changes/additions would be made:

1. Add user interface to upload images / use camera to take live images

2. Expand user interface to display ingredient(s) / ingredient characteristics
