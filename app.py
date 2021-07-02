from flask import Flask, render_template, request
from tag_helper.tag_recommender import LRTagRecommender
import json

# Require this func to make the model pickler works
def identity_fun(text):
    return text


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/getTags", methods=["POST"])
def get_tags():
    req = request.json
    content = req["content"]
    title = req["title"]
    result = model.infer({"content": content})
    result = list(map(lambda tag: {"tag": tag[0], "score": tag[1]}, result))
    return json.dumps(result, ensure_ascii=False)


if __name__ == "__main__":
    model = LRTagRecommender()
    app.run(host="0.0.0.0", debug=True)