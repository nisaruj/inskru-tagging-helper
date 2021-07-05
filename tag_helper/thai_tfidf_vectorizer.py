from sklearn.feature_extraction.text import TfidfVectorizer

class ThaiTdidfVectorizer(TfidfVectorizer):
  def __init__(self):
      super().__init__(analyzer = 'word',
                                   tokenizer=ThaiTdidfVectorizer.identity_fun,
                                   preprocessor=ThaiTdidfVectorizer.identity_fun,
                                   token_pattern=None, ngram_range=(1, 2), max_features=50000)
  def identity_fun(text):
      return text