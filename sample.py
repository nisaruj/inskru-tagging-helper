# coding=utf8
from tag_helper.tag_recommender import LRTagRecommender
import json

# Require this func to make the model pickler works
def identity_fun(text):
    return text

with open('sample.json') as fp:
    sample = json.loads(fp.read())["content"]

if __name__ == "__main__":
    model = LRTagRecommender()
    print(model.infer({"content": sample}))
