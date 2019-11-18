import json


data = [
    {
        'title': "hadoop",
        'url': "https://www.naver.com",
        'detail' : 'this is a test',
    },
    {
        'title': "naver",
        'url': "https://www.naver.com",
        'detail' : 'this is a test',
    },
    {
        'title': "javascript",
        'url': "https://www.naver.com",
        'detail' : 'this is a test',
    }
]


print(json.dumps(data))