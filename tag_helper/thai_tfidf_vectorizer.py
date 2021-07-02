from sklearn.feature_extraction.text import TfidfVectorizer

class ThaiTdidfVectorizer(TfidfVectorizer):
  def __init__(self):
      super().__init__(analyzer = 'word',
                                   tokenizer=ThaiTdidfVectorizer.identity_fun,
                                   preprocessor=ThaiTdidfVectorizer.identity_fun,
                                   token_pattern=None)
  def identity_fun(text):
      return text