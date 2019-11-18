import json


data = [
    {
        'title': "hadoop",
        'url': "https://www.naver.com",
        'detail' : 'A textbook is a comprehensive compilation of content in a branch of study. Textbooks are produced to meet the needs of educators, usually at educational institutions. Schoolbooks are textbooks and other books used in schools.[1][2] Today, many textbooks are published in both print format and digital formats.',
    },
    {
        'title': "naver",
        'url': "https://www.naver.com",
        'detail' : 'A textbook is a comprehensive compilation of content in a branch of study. Textbooks are produced to meet the needs of educators, usually at educational institutions. Schoolbooks are textbooks and other books used in schools.[1][2] Today, many textbooks are published in both print format and digital formats.',
    },
    {
        'title': "javascript",
        'url': "https://www.naver.com",
        'detail' : 'A textbook is a comprehensive compilation of content in a branch of study. Textbooks are produced to meet the needs of educators, usually at educational institutions. Schoolbooks are textbooks and other books used in schools.[1][2] Today, many textbooks are published in both print format and digital formats.',
    }
]


print(json.dumps(data))