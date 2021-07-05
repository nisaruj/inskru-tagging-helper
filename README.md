# insKru tagging helper

Tag recommendation service created exclusively for insKru article writers.

[Demo](http://inskru-tag-helper.herokuapp.com/) on Heroku

## Installation

```
pip install -r requirements.txt
```

Run `python app.py` to start the development server. The web server is accessible at `localhost:5000` by default.

## API

Send a `POST` request with a JSON body whose schema is described below. Note that the `content` can be in HTML format. Containing URLs is also acceptable.

### Request

```json
POST /api/getTags
{
    "title": string,
    "content": string
}
```

### Response

The response is divided into two fields: `general` and `keywords`.

`general` contains general tags (i.e. subjects and major tag, such as `เกมและกิจกรรม`). The result should be an array of objects, sorted by `score` in descending order. Each object contains `tag` and `score` ranged 0 to 1 which is the probability that a tag relating to the article.

`keywords` is an array of string contains important keywords that are extracted from the article.

Example Response

```json
{
    "general": [
        {"tag": "เคมี", "score": 0.8844894709378359}, 
        {"tag": "วิทยาศาสตร์", "score": 0.7160098506678959}, 
        {"tag": "เกมและกิจกรรม", "score": 0.6136530011547631}, 
        {"tag": "ตัวช่วยครู", "score": 0.2200215928122598}, 
        {"tag": "ทบทวนบทเรียน", "score": 0.2018304010983465}
    ], 
    "keywords": ["ใบกิจกรรม", "เชิงคำนวณ", "หลอดทดลอง", "บอร์ดเกม", "ดัดแปลง", "เลื่อน", "เม็ด", "กิจกรรม", "หลอด"]
}
```


Made with ❤️ & ☕ by Nisaruj Rattanaaram