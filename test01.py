import requests
from datetime import datetime, timedelta
import json

BASE_URL_FB_API="https://graph.facebook.com/v3.0"
ACCESS_TOKEN="EAACEdEose0cBANEp4OhiKCfvOkLX08Q1ZC6LHfVrEuo9teZBNgPaEJZA7VabYE4fAWtE3kI8vTIB8ZAPF0Sp6UajuFl5boAO1uIlOpu81ZCtx3rsQEYWZAVIJS8FgSPMpauJ6AuGyWXAzciS9t1DCZApwrVKH4VAa9LaBUlIbFIAWotSwQNxyl35hsTgPSH4AsTejezqoc68QZDZD"
LIMIT_REQUEST=20
pagename="jtbcnews"
from_date="2018-05-22"
to_date="2018-05-23"

#url을 주면
def get_json_result(url):
    try:
        response = requests.get(url)  #get으로 요청
        if response.status_code == 200:  # 정상일때만
           return response.json()  #요청한곳으로 데이터 리턴

    except Exception as e: #정상이 아니면 에러메세지 리턴
        return "%s: Error for request [%s]" %(datetime.now(), url)


#페이스북 페이지네임을 주면 페이지 id 값을 리턴해주는 애를 만들것임
def fb_name_to_id(pagename):

    #url="https://graph.facebook.com/v3.0/jtbcnews/?access_token=324342434"
    base=BASE_URL_FB_API
    node="/%s" % pagename
    params="/?access_token=%s" % ACCESS_TOKEN
    url=base+node+params

    #위의 메소드 사용하여 json 형태의 결과값 받기
    json_result=get_json_result(url)
    #특정값을 뽑을때 value 값을 뽑는거
    return (json_result["id"])
    #print(json_result)

#페이스북 포스트 리스트 가져오는 함수(페이지네임, 시작날짜, 끝날짜)를 주면 json형태가아니라 list형태로 데이터를 리턴해준다.
def fb_get_post_list(pagename, from_date, to_date):

    page_id=fb_name_to_id(pagename)
    base=BASE_URL_FB_API
    node='/%s/posts' % page_id
    fields='/?fields=id,message,link,name,type,shares,'+\
        'created_time,comments.limit(0).summary(true),'+\
        'reactions.limit(0).summary(true)'
    duration='&since=%s&until=%s' %(from_date, to_date)
    parameters='&limit=%s&access_token=%s' %(LIMIT_REQUEST, ACCESS_TOKEN)
    url=base+node+fields+duration+parameters

    postList=[]
    isNext=True
    while isNext:
        #json만든주소로 요청, 20개와 next가 있는데 필요한 것만 뽑을꺼야
        tmpPostList = get_json_result(url)
        for post in tmpPostList["data"]: #20개짜리 data를 1개 꺼내서 담는다
            postVo=preprocess_post(post)
            postList.append(postVo)

        paging=tmpPostList.get("paging").get("next")
        #paging=tmpPostList["paging"]["next"]
        if paging !=None: #아직있으면
            url=paging
        else:
            isNext=False
        # save results to file
        with open("d:/spring/fb/" + pagename + ".json", 'w', encoding='utf-8') as outfile:
            json_string = json.dumps(postList, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(json_string)

    return postList

#5개만 뽑아내는 함수
def preprocess_post(post):
    #작성일+9시간 해줘야 함
    created_time = post["created_time"]
    created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S+0000')
    created_time = created_time + timedelta(hours=+9)
    created_time = created_time.strftime('%Y-%m-%d %H:%M:%S')
    #공유수
    if "shares" not in post :
        shares_count=0
    else:
        shares_count=post["shares"]["count"]
    # 리액션 수
    if 'reactions' not in post:
        reactions_count = 0
    else:
        reactions_count = post["reactions"]['summary']['total_count']
    # 댓글 수
    if 'comments' not in post:
        comments_count = 0
    else:
        comments_count = post["comments"]['summary']['total_count']
    # 메시지 수
    if 'message' not in post:
        message_str = ""
    else:
        message_str = post["message"]
    postVo = {
        "created_time": created_time,
        "shares_count": shares_count,
        "reactions_count": reactions_count,
        "comments_count": comments_count,
        "message_str": message_str
    }
    return postVo

    #json 형태로 된 포스트들을 가져옴
    # jsonPosts=get_json_result(url) #포스트 정보를 딕션어리 형태로 리턴(date, paging)
    # return jsonPosts

result=fb_get_post_list(pagename, from_date, to_date)
print(result)


# result=fb_name_to_id("jtbcnews")
# print(result)

# url="http://192.168.1.14:8088/mysite4/api/gb/list/"
# result=get_json_result(url)
# print(result)

# #get 방식으로 요청한것임
# #응답을 받을 수 있는 객체 자료형이지만response는 내가 만든 변수
# response=requests.get(url)
# print(type(response))
#
# #주소가 없을 경우:
# if response.status_code==200: #성공일때만
#     print(response.json())
