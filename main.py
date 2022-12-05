from config import *
import cv2
import pytesseract
import re
from nltk.corpus import stopwords
import requests
import pandas as pd


"""
Steps:
1. user uploads photo of ingredients ✓        
2. convert photo to text ✓
3. convert text to list ✓
4. call Cosmily API for EWG analysis ✓
5. return ingredients report to user

Error Handling:
- user input is a jpg, jpeg, or png file.
- Blurry Image
- Ingredients are not found in Cosmily database
- Image is not of ingredients or does not have any text in it

If extra time:
- scrape a website for a product's ingredients
- add dictionary instead of hardcoded phrasing
"""

class IngredientChecker():
    def __init__(self, file_path):
        self.ingredients = None
        self.convert_image_to_text(file_path)
        self.analyze()

    def preprocess(self, text):
        stop_words = set(stopwords.words('english'))
        ingredients = []

        # remove stop words, the word "ingredients", and leading spaces
        for item in text:
            item = item.lstrip()
            if "ingredients" not in item.lower() and item not in stop_words:
                ingredients.append(item)

        self.ingredients = ', '.join(ingredients)

    def convert_image_to_text(self, path):
        # open image and convert to rgb
        img = cv2.imread(path)
        b,g,r = cv2.split(img)
        img_rgb = cv2.merge([r,g,b])

        # convert image to string
        text = re.findall(r'[^.,:/\n]+', pytesseract.image_to_string(img_rgb))      # custom_config = r'--oem 3 --psm 6' --> add config param if words are too blurry
        self.preprocess(text)

    def analyze(self):
        # get analysis of ingredient list from cosmily database api
        api_url = 'https://api.cosmily.com/api/v1/analyze/ingredient_list'
        headers =  {"Content-Type":"application/json", "Authorization": AUTH_TOKEN}
        params = {"ingredients": self.ingredients}
        response = requests.post(api_url, params=params, headers=headers)
        self.analysis = response.json()['analysis']

    def report(self):
        description = f'This product contains {self.analysis["total_ingredients"]} ingredients.'
        print(description)

        # # TODO: EWG stats
        # self.analysis["ewg"]

        # print("DETRIMENTS")
        # # TODO: loop through and list negatives and harmful
        # self.analysis["negatives"]
        # self.analysis["harmful"]

        # print("BENEFITS")
        # # TODO: loop through and list positives and notables
        # self.analysis["positives"]
        # self.analysis["notable"]

        # # TODO: loop though each ingredient in ingredients_table and provide breakdown
        # print("\nWould you like to view the full ingredients data breakdown? (Y/N)")
        # show_breakdown = input

        # if show_breakdown.lower() == 'y':
        #     print(pd.DataFrame(self.analysis["ingredients_table"]))
        
        # # TODO: End report
            


def start():
    print('Please enter the image file path:')
    # TODO: test more images and remove default
    # image_path = input()
    image_path = './images/sensodyne.jpeg'
    checker = IngredientChecker(image_path)
    checker.report()
    checker = None


def main():
    done = 0
    print("Ready to check some ingredients?")
    while done < 1:
        start()
        print("Would you like to check another product? (Y/N)")
        user_input = input()
        if user_input.lower() != 'y':
            done += 1


if __name__ == '__main__':
    main()