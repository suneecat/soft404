
import time
import sys
import re
import io
import os
import torch
import requests
import numpy as np
import csv
from bs4 import BeautifulSoup
from PIL import Image
from urllib.parse import urljoin
from requests.exceptions import ConnectionError
from urllib3.exceptions import NewConnectionError
from nltk.corpus import wordnet
from transformers import BertTokenizer, BertForSequenceClassification
from goose3 import Goose
#removed by psl
#model = torch.load("bert_model1")
#changed, added,  by psl
#import nltk
model = torch.load("/home/psl/CCrawl/BERT_and_catbin_models/bert_model", map_location=torch.device('cpu'))

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=False)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
device

#nltk.download('wordnet')
#uncomment the above if u havent download it even once

def is_meaningful(name):
    # Check if the image name contains a meaningful word
    for word in name.split('_'):  # Split image name by underscores
        if wordnet.synsets(word):
            return True
    return False

def sanitize_csv_text(text):
    # Remove common CSV delimiters (comma, semicolon, tab, pipe, colon, and space)
    sanitized_text = re.sub(r'[,\t;|: ]', ' ', text)
    # Replace multiple spaces with a single space
    sanitized_text = re.sub(r'\s+', ' ', sanitized_text)
    # Split the text into words and take the first 100 words
    words = sanitized_text.split()[:100]
    # Join the first 100 words back into a single string
    sanitized_text = ' '.join(words)
    return sanitized_text


def get_website_details(url):
  
    try:
        response = requests.get(url, timeout=30)
        content = response.content.decode('utf-8', 'ignore')
        soup = BeautifulSoup(content, "html.parser")
        paragraphs = soup.find_all("p")
        
  
        g = Goose()
        article = g.extract(raw_html=content) 
               
     
        context=sanitize_csv_text(article.cleaned_text[:200])


        extracted_text = []
        for paragraph in paragraphs:
            text = paragraph.get_text()
            extracted_text.append(text)
        content_t = " ".join(extracted_text)
     
        content_t=sanitize_csv_text(content_t)

        
        title = soup.find("title")
        title_text = title.text
        title_text=sanitize_csv_text(title_text)
        
        images = soup.find_all("img")
        k=0
        image_names = []
        for i, image in enumerate(images):
           if i < 5:  # Limit to top 5 images
               image_url = image["src"]
               image_name = os.path.basename(image_url)
               if len(image_name) > 25:
                   image_name = image_name[:25]  # Truncate name to 25 characters
               image_names.append(image_name)
           else:
               break
        meaningful_image_names = []
        for i, image in enumerate(images):
            if i < 5:  # Limit to top 5 images
                image_url = image["src"]
                image_name = os.path.basename(image_url)

                if is_meaningful(image_name):
                    if len(image_name) > 25:
                        image_name = image_name[:25]  # Truncate name to 25 characters
                    meaningful_image_names.append(image_name)
            else:
                break
        
        details = {
            "Url": url,
            "Title":title_text,
            "Text":context,
            "Article":content_t,
            "Image_Name":meaningful_image_names,
            "response_status_code": response.status_code
        }

        return details

    except Exception as e:
        print(f"Error processing website {url}: {str(e)}")
        return None

def make_prediction(details):
    # Prepare the input for the BERT model  '[CLS]'  + dft['Title'] + '[SEP]' + dft['Text'] + dft['Image_Name']
    if details["response_status_code"] != 200:
        #return details["response_status_code"]
        prediction=int(details["response_status_code"])
        return prediction
    text=details['Text']
    text = ' '.join(text.split()[:350])
    input_text = '[CLS]'  + details['Title'] + '[SEP]' + text +'[SEP]'+details['Article']+'[SEP]'+' '.join(details['Image_Name'])
    input_text = ' '.join(input_text.split()[:450])
    # print(input_text) # uncomment to check input to model 
    # Take the first 75 words   QWE
    inputs = tokenizer.encode_plus(
        input_text,
        None,
        add_special_tokens=True,
        max_length=128,  # Adjust this based on your model's input length
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )

    # Perform the prediction
    with torch.no_grad():
        inputs = {k: v.to(device) for k, v in inputs.items()}
        output = model(**inputs)
        logits = output.logits
        logits = logits.detach().cpu().numpy()
        prediction = np.argmax(logits, axis=1).flatten().item()

    return prediction

def get_file_data(filename):
    with open(filename, 'r') as f:
        data = [line.rstrip('\n') for line in f]	   
        return data

def write_header(outputfile):
   with open(outputfile, "w", newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(["Url", "prediction", "Actual", "prediction_ok?"])

def write_details_to_csv(outputfile, url, prediction, actual, ok):
        with open(outputfile, "a", newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([url, prediction, actual, ok])

def main():
    outputfile = "bert_soft404_chk.csv"
    write_header(outputfile)
    count=0
    http_list = get_file_data("http_sites.dat")
    for http in http_list:
        details = get_website_details(http)
        if details is not None:
            prediction = make_prediction(details)
            if (prediction==1):
                result="404-error"
            elif(prediction==0):
                result="200 Okay"
        else:
            result="HTTPS_status_code_"+str(prediction)

        write_details_to_csv(outputfile, http, result, None, None)
        count=count+1
        if count == 1000:
            break

        


if __name__ == "__main__":
    main()
