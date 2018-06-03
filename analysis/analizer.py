import json, re
from konlpy.tag import Twitter
from collections import Counter


# json 파일명, 추출할 데이터의 key 값을 주면 문자열을 리턴한다.
def json_to_str(filename, key):
    jsonfile = open(filename, 'r', encoding='utf-8')
    # 파일1개당 데이터 덩어리 1개 실제문자열
    json_string = jsonfile.read()
    # list로 담겨있고
    jsondata = json.loads(json_string)

    # print(type(json_string))
    # print(json_string)
    #
    # print(type(jsondata))
    # print(jsondata)

    data = ''
    for item in jsondata:
        value = item.get(key)
        if value is None:
            continue
        data += re.sub(r'[^\w]', '', value)  # 한글만 계속 붙여나간다.
    return data


# 명사를 추출해서 빈도수를 알려줌
def count_wordfreq(data):
    twitter = Twitter()  # 객체생성
    nouns = twitter.nouns(data)
    print(nouns)

    # 단어에서 횟수나옴
    count = Counter(nouns)
    # print(count)
    return count


datastring = json_to_str("D:/spring/fb/jtbcnews.json", "message_str")
# print(datastring)
count_wordfreq(datastring)
