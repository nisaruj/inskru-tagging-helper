# insKru tagging helper

Tag recommendation service created exclusively for insKru article writers.

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

The result should be an array of objects, sorted by `score` in descending order. Each object contains `tag` and `score` ranged 0 to 1 which is the probability that a tag relates to the article.

Example Response

```json
[
    {
        "tag": "วิทยาศาสตร์", 
        "score": 0.2875840585310179
    }, 
    {
        "tag": "เกมและกิจกรรม", 
        "score": 0.20208380161743394
    }
]
```