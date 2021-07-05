import pickle
from .preprocess import DataPreparer

IDEA_CAT = [
    "การงานอาชีพ",
    "กิจกรรมเสริม",
    "คณิตศาสตร์",
    "คอมพิวเตอร์",
    "ชีววิทยา",
    "ตัวช่วยครู",
    "ทบทวนบทเรียน",
    "ฟิสิกส์",
    "ภาษาต่างประเทศ",
    "ภาษาอังกฤษ",
    "ภาษาไทย",
    "วิทยาการคำนวณ",
    "วิทยาศาสตร์",
    "ศิลปะดนตรีและนาฏศิลป์",
    "สังคมศึกษา",
    "สุขศึกษาและพลศึกษา",
    "เกมและกิจกรรม",
    "เคมี",
    "เทคโนโลยีการสอน",
    "แนะแนว",
]


def decode_output(pred, threshold=0.2):
    result = []
    for idx, prob in enumerate(pred):
        if prob > threshold:
            result.append((IDEA_CAT[idx], prob))
    return sorted(result, key=lambda t: t[1], reverse=True)


class ITagRecommender:
    def infer(self, content) -> tuple:
        pass


class LRTagRecommender(ITagRecommender):
    def __init__(self):
        with open("tag_helper/models/model_bigram.pkl", "rb") as fp:
            self.classifier = pickle.load(fp)

    def rank_term(self, tfidf, terms, max_keyword):
        scores = []
        for i in range(len(tfidf)):
            scores.append((tfidf[i], terms[i]))
        return sorted(scores, reverse=True)[:max_keyword]

    def extract_keywords(self, tfidf, terms, content, max_keyword=10):
        ranked_terms = self.rank_term(tfidf, terms, max_keyword)

        bigram_terms = []
        unigram_terms = []
        for _, term in ranked_terms:
            if ' ' in term:
                keyword = term.replace(' ', '')
                if keyword in content:
                    bigram_terms.append(keyword)
            else:
                unigram_terms.append(term)

        candidates = []
        single_words_used = set()
        for i in range(len(unigram_terms)):
            for j in range(len(unigram_terms)):
                if i != j:
                    keyword = unigram_terms[i] + unigram_terms[j]
                    if keyword in content:
                        candidates.append(keyword)
                        single_words_used.update((unigram_terms[i], unigram_terms[j]))
        
        keywords = bigram_terms + candidates + list(set(unigram_terms) - single_words_used)
        return keywords

    def infer(self, content):
        data_prep = DataPreparer()
        tfidf, X = data_prep.preprocess(content)
        keywords = self.extract_keywords(tfidf, data_prep.get_tfidf_terms(), content["content"])
        y_pred = self.classifier.predict_proba(X)[0]
        ranked_tags = decode_output(y_pred)
        return ranked_tags, keywords
