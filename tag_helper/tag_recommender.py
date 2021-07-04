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
        with open("tag_helper/models/model.pkl", "rb") as fp:
            self.classifier = pickle.load(fp)

    def infer(self, content):
        X = DataPreparer().preprocess(content)
        y_pred = self.classifier.predict_proba(X)[0]
        ranked_tags = decode_output(y_pred)
        return ranked_tags
