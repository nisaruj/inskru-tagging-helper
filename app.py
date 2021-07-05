from flask import Flask, render_template, request
from tag_helper.tag_recommender import LRTagRecommender
import json

app = Flask(__name__)
model = LRTagRecommender()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/getTags", methods=["POST"])
def get_tags():
    req = request.json
    title = req["title"]
    content = title + ' ' + req["content"]
    result, keyword = model.infer({"content": content})
    payload = {
        "general": list(map(lambda tag: {"tag": tag[0], "score": tag[1]}, result)),
        "keywords": keyword
    }
    return json.dumps(payload, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
