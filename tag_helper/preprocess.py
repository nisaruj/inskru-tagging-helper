from bs4 import BeautifulSoup
import attacut
from pythainlp.corpus.common import thai_stopwords
import numpy as np
import re
import string
import pickle
from .keyword_rules import TAG_KEYWORDS, TAG_IGNORE_LIST


class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == "ThaiTdidfVectorizer":
            from tag_helper.thai_tfidf_vectorizer import ThaiTdidfVectorizer

            return ThaiTdidfVectorizer
        return super().find_class(module, name)


stop_words = thai_stopwords()


class DataPreparer:
    def __init__(self):
        self.tfidf_vec = CustomUnpickler(
            open("tag_helper/models/tfidf_vec.pkl", "rb")
        ).load()
        self.terms = self.tfidf_vec.get_feature_names()

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
        return attacut.tokenize(content)

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

    def contains_essential_keyword(idea_content):
        content = idea_content.lower()
        features = []
        for tag in TAG_KEYWORDS:
            if tag not in TAG_IGNORE_LIST:
                flag = tag in content
            else:
                flag = False
            for keyword in TAG_KEYWORDS[tag]:
                if keyword in content:
                    flag = True
                    break
            features.append(int(flag))
        return np.array(features)

    def rank_term(self, tfidf):
        scores = []
        print(tfidf)
        for i in range(len(tfidf)):
            scores.append((tfidf[i], self.terms[i]))
        return sorted(scores, reverse=True)[:10]

    def preprocess(self, data):
        raw_content = data["content"]
        content = DataPreparer.clean_content(raw_content)
        tok = DataPreparer.tokenize(content)
        tok = DataPreparer.perform_removal(tok)
        tfidf = self.tfidf_transform([tok])
        tfidf = np.array(tfidf.todense())
        tfidf_and_handcraft = np.append(
            tfidf.reshape(-1), DataPreparer.contains_essential_keyword(raw_content)
        ).reshape(1, -1)
        return tfidf_and_handcraft
