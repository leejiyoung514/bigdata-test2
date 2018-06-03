from collect import crawler
from analysis import analizer
from visualize import visualizer

pagename = "jtbcnews"
#pagename = "chosun"
from_date = "2017-01-01"
to_date = "2017-10-31"

if __name__ == '__main__':

    #수집 저장
    postList = crawler.fb_get_post_list(pagename, from_date, to_date)
    print(postList)

    #분석
    datastring = analizer.json_to_str("D:/spring/fb/%s.json" % pagename, "message_str")
    count_data=analizer.count_wordfreq(datastring)
    print(count_data)  #list 데이터를 가지고 그림을 그릴것이다.ㅋㅋ
    dictWord=dict(count_data.most_common(20)) #list 딕셔너리 형태로 형변환

    #그래프
    visualizer.show_graph_bar(dictWord, pagename)
    #워드크라우드
    visualizer.worldcloud(dictWord, pagename)

