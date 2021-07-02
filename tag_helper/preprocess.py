from bs4 import BeautifulSoup
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus.common import thai_stopwords
import numpy as np
import re
import string
import pickle

stop_words = thai_stopwords()


class DataPreparer:
    def __init__(self):
        with open("tag_helper/models/tfidf_vec.pkl", "rb") as fp:
            self.tfidf_vec = pickle.load(fp)

    def remove_tags(html):
        return BeautifulSoup(html, "lxml").text

    def deEmojify(text):
        regrex_pattern = re.compile(
            pattern="["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+",
            flags=re.UNICODE,
        )
        return regrex_pattern.sub(r"", text)

    def remove_url(text):
        return re.sub(r"[a-z]*[:.]+\S+", "", text)

    def clean_content(text):
        text = DataPreparer.remove_url(text)
        text = DataPreparer.remove_tags(text)
        text = DataPreparer.deEmojify(text)
        text = text.replace("\xa0", " ")
        return text

    def tokenize(content):
        return word_tokenize(content)

    def word_removal(word):
        word = word.strip()
        word = word.lower()
        word = word.translate(str.maketrans("", "", string.punctuation))
        if (
            word.isdigit()
            or (word in stop_words)
            or (word in ["blank", "href", "target"])
        ):
            return ""
        else:
            return word

    def perform_removal(article):
        doc = list(map(DataPreparer.word_removal, article))
        doc = list(filter(lambda word: word != "", doc))
        return doc

    def tfidf_transform(self, tok):
        return self.tfidf_vec.transform(tok)

    def preprocess(self, data):
        content = data["content"]
        content = DataPreparer.clean_content(content)
        tok = DataPreparer.tokenize(content)
        tok = DataPreparer.perform_removal(tok)
        tfidf = self.tfidf_transform([tok])
        tfidf = np.array(tfidf.todense())
        return tfidf
