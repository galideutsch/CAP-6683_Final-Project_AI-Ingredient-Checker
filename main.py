from config import *
import cv2
import pytesseract
import re
from nltk.corpus import stopwords
import requests
import pandas as pd


class IngredientScanner():
    def __init__(self, file_path):
        self.ingredients = None
        self.convert_image_to_text(file_path)
        self.analyze()

    def preprocess(self, text):
        stop_words = set(stopwords.words('english'))
        ingredients_list = []

        # remove stop words, the word "ingredients", and leading spaces
        for item in text:
            item = item.lstrip()
            if "ingredients" not in item.lower() and item not in stop_words:
                ingredients_list.append(item)

        self.ingredients = ', '.join(ingredients_list)

    def convert_image_to_text(self, path):
        # open image and convert to rgb
        img = cv2.imread(path)
        b,g,r = cv2.split(img)
        img_rgb = cv2.merge([r,g,b])

        # convert image to string
        text = re.findall(r'[^.,:/\n]+', pytesseract.image_to_string(img_rgb))   
        self.preprocess(text)

    def analyze(self):
        # get analysis of ingredient list from cosmily database api
        api_url = 'https://api.cosmily.com/api/v1/analyze/ingredient_list'
        headers =  {"Content-Type":"application/json", "Authorization": AUTH_TOKEN}
        params = {"ingredients": self.ingredients}
        response = requests.post(api_url, params=params, headers=headers)
        self.analysis = response.json()['analysis']

    def report(self):
        print(self.analysis['description'])
        print(f"{self.analysis['text'].split('. ')[1]}.")

        print("\nSAFETY OF INGREDIENTS")
        ingredients_dictlist = []
        ing_df = pd.DataFrame(columns=['Name','Alias','Decision'])

        ings = []
        ali = []
        decis = []
        for ing in self.analysis['ingredients_table']:
            ingredients_dictlist.append(ing)
            ings.append(ing['title'])
            ali.append(ing['alias'])
            
            try:
                ing['ewg']['decision']
            except:
                decis.append('N/A')
            else:
                decis.append(ing['ewg']['decision'])


        ing_df['Name'] = ings
        ing_df['Alias'] = ali
        ing_df['Decision'] = decis
        
        print(ing_df)


        print("\nBENEFICIAL ASPECTS")
        pos_df = pd.DataFrame(columns=['Benefit','Ingredient','Description'])

        pos = []
        desc = []
        ings = []
        for positive in self.analysis['positive']:
            pos.append(self.analysis['positive'][positive]['title'])
            desc.append(self.analysis['positive'][positive]['description'])
            ings.append(self.analysis['positive'][positive]['list'][0]['title'])

        pos_df['Benefit'] = pos
        pos_df['Ingredient'] = ings
        pos_df['Description'] = desc

        print(pos_df)

        print("\nHAZARDOUS ASPECTS")
        harm_df = pd.DataFrame(columns=['Hazard','Ingredient','Description'])
        name = []
        desc = []
        ings = []
        for h in self.analysis['harmful']:
            if len(self.analysis['harmful'][h]['list']) > 0:
                for i in self.analysis['harmful'][h]['list']:
                    name.append(self.analysis['harmful'][h]['title'])
                    desc.append(self.analysis['hgarmful'][h]['description'])
                    ings.append(i['title'])

        harm_df['Hazard'] = name
        harm_df['Ingredient'] = ings
        harm_df['Description'] = desc

        print(harm_df)
            

def main():
    image_path = './images/sensodyne.png'
    scanner = IngredientScanner(image_path)
    scanner.report()


if __name__ == '__main__':
    main()