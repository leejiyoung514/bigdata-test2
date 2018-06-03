import requests
from datetime import datetime, timedelta
import json

BASE_URL_CS_API="https://graph.facebook.com/v3.0"
ACCESS_TOKEN="EAACEdEose0cBAPrv2z5wGkWXOXTBWJ1jHRr3soX4AxZBKhYmZBLn95WkVMwmOWfFY6peN84BaYo0gBTazgax9fYYZALND6GeZC14gCmNkT7fwKGW7xXLS2x25cHZBszZBKROluP6NvVjsiZCO75EBmI4Oo1mnGBuxalOOMIM1FOgZAPUkZCKNUZAUVtfDXEdCTOhMNGCOsrB0xiwZDZD"
LIMIT_REQUEST=20
pagename="chosun"
from_date="2018-05-14"
to_date="2018-05-23"

#json통신 모듈 만들기 -url을 통해 요청하고 json 형태의 정보를 받아옴
def get_json_result(url):
    try:
        response=requests.get(url)

        if response.status_code==200:
            json_result=response.json()

        return json_result

    except Exception as e:
        return '%s: Error for request [%s]' %(datetime.now(), url)

#chosun id 값 알아오기
def fb_name_to_id(pagename):

    base = BASE_URL_CS_API
    node = "/%s" % pagename
    params = "/?access_token=%s" % ACCESS_TOKEN
    url = base + node + params

    json_result=get_json_result(url)
    return (json_result["id"])
    #print(json_result)

result=fb_name_to_id("chosun")
print(result)

#특정기간 내의 chosun포스트를 가져오는 함수
def fb_get_post_list(pagename, from_date, to_date):
    page_id=fb_name_to_id(pagename)
    base=BASE_URL_CS_API
    node='/%s/posts' % page_id
    fields='/?fields=id,message,link,name,type,shares,'+\
        'created_time,comments.limit(0).summary(true),'+\
        'reactions.limit(0).summary(true)'
    duration='&since=%s&untill=%s' % (from_date, to_date)
    parameters='&limit=%s&access_token=%s' %(LIMIT_REQUEST, ACCESS_TOKEN)
    url=base+node+fields+duration+parameters

    postList=[]
    isNext=True
    while isNext:
        tmpPostList=get_json_result(url)
        for post in tmpPostList["data"]:
            postVo=preprocess_post(post)
            postList.append(postVo)

        paging=tmpPostList.get("paging").get("next")
        if paging !=None:
            url=paging
        else:
            isNext=False
        # save results to file
        with open("d:/spring/fb/" + pagename + ".json", 'w', encoding='utf-8') as outfile:
            json_string = json.dumps(postList, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(json_string)

    return postList

#5개씩 뽑아내는 함수
def preprocess_post(post):
    #작성일
    created_time = post["created_time"]
    created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S+0000')
    created_time = created_time + timedelta(hours=+9)
    created_time = created_time.strftime('%Y-%m-%d %H:%M:%S')
    #공유수
    if "shares" not in post:
        shares_count=0
    else:
        shares_count=post["shares"]["count"]
    #리액션 수
    if "reactions" not in post:
        reactions_count=0
    else:
        reactions_count=post["reactions"]["summary"]["total_count"]
    #댓글 수
    if "comments" not in post:
        comments_count=0
    else:
        comments_count=post["reactions"]["summary"]["total_count"]
    #메시지 수
    if "message" not in post:
        message_str=""
    else:
        message_str=post["message"]

    postVo={
        "created_time": created_time,
        "shares_count": shares_count,
        "reactions_count": reactions_count,
        "comments_count": comments_count,
        "message_str": message_str
    }
    return postVo


result=fb_get_post_list(pagename, from_date, to_date)
print(result)







