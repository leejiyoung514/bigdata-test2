import matplotlib.pyplot as plt
from matplotlib import font_manager
import pytagcloud
import webbrowser


# dict 형식의 단어들을 받아서 그래프를 출력하는 함수이다.
def show_graph_bar(dictWords, pagename):
    # 한글처리
    # 한글 폰트설정을 위해 font family 이름을 알아야 하는데, 폰트 파일만으로 알수없다.
    font_filename = "c:/Windows/fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_filename).get_name()
    print(font_name)
    plt.rc('font', family=font_name)  # 리소스에 넣는 작업

    # 라벨처리
    plt.xlabel("주요단어")
    plt.ylabel("빈도수")
    plt.grid(True)  # 그리드 그릴것인지

    # 데이터 대입- key value 따로 뽑아냅
    dict_keys = dictWords.keys()
    dict_values = dictWords.values()

    # 그래프 그리는 속성들 엑셀에서 그리는것과 같은
    plt.bar(range(len(dictWords)), dict_values, align='center')
    plt.xticks(range(len(dictWords)), list(dict_keys), rotation=70)

    save_filename = "d:/spring/fb/%s_bar_graph.png" % pagename
    plt.savefig(save_filename, dpi=400, bbox_inches='tight')

    plt.show()


def worldcloud(dictWords, pagename):
    print(type(dictWords))
    print(dictWords)
    taglist = pytagcloud.make_tags(dictWords.items(), maxsize=80)

    save_filename = "d:/spring/fb/%s_worldcloud.png" % pagename
    pytagcloud.create_tag_image(
        taglist,
        save_filename,
        size=(800, 600),
        fontname='korean',
        rectangular=False
    )

    webbrowser.open(save_filename)
