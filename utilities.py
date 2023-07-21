## import library
import pandas as pd
import requests
from bs4 import BeautifulSoup

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')

## Helper function
def transform_date_news(date):
    date_str = str(date)

    # Convert to datetime
    date_dt = pd.to_datetime(date_str, format='%Y%m%d%H%M%S')
    date_only_str = date_dt.strftime('%Y-%m-%d')
    return date_only_str

def transform_date_price(date):
    date_str = str(date)

    # Convert to datetime
    date_str = date_str.replace('.', '')
    date_dt = pd.to_datetime(date_str, format='%b %d, %Y')
    date_only_str = date_dt.strftime('%Y-%m-%d')
    return date_only_str

def extract_text(url):
    # Set a User-Agent for the request header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

    # Send a GET request to the URL with the User-Agent header
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the element that contains the article text
    # depends on the structure of the webpage

    # Find the article element
    article = soup.find('article')

    # Find the main element
    main = soup.find('main')

    # Check if either the article or main element exists
    if article:
        # Get the text content from either the article or main element
        if main:
            text_content = article.text if len(article.text) > len(main.text) else main.text
        else:
            text_content = article.text
    elif main:
        text_content = main.text

    else:
        all_div = soup.find('body')
        text_content = all_div.text

    return text_content


def preprocess_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Remove mentions and hashtags
    text = re.sub(r'@\w+|#\w+', '', text)

    # Remove punctuation and convert to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()

    # Remove newline characters
    text = re.sub('\n', ' ', text)

    # Remove extra whitespace
    text = re.sub('\s+', ' ', text).strip()

    return text

def stem_fun(txt_in):
    from nltk.stem import PorterStemmer
    stem_tmp = PorterStemmer()
    tmp = [stem_tmp.stem(word) for word in txt_in.split()]
    tmp = ' '.join(tmp)
    # tmp = list()
    # for word in txt_in.split():
    #     tmp.append(stem_tmp.stem(word))
    return tmp

def lemma_fun(txt_in):

    def get_wordnet_pos(word):
        """Map POS tag to first character lemmatize() accepts"""
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

        return tag_dict.get(tag, wordnet.NOUN)

    lemmatizer = WordNetLemmatizer()

    tmp = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in word_tokenize(txt_in)]
    tmp = ' '.join(tmp)
    return tmp

def rem_sw(var_in):
    from nltk.corpus import stopwords
    sw = stopwords.words("english")
    tmp = var_in.split()
    # tmp_ar = list()
    # for word_t in tmp:
    #     if word_t not in sw:
    #         tmp_ar.append(word_t)
    tmp_ar = [word_t for word_t in tmp if word_t not in sw]
    tmp_o = ' '.join(tmp_ar)
    return tmp_o

def rem_num(text_in):
    import re
    tmp = re.sub("[^A-Za-z']+", " ",text_in).lower().strip().replace("  ", " ")
    return tmp


def get_clean_text(url):
    try:
        raw = extract_text(url)
        process = preprocess_text(raw)
        clean = rem_num(rem_sw(process))
        res = lemma_fun(clean)
        return res
    except:
        return None




