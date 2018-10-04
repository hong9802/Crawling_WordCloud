import re
from bs4 import BeautifulSoup
import requests
from konlpy.tag import Twitter
from collections import Counter
import time
import pytagcloud

j = 0
state = 0
def listparshing(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    hansunglist = soup.find("table", class_="bbs-list")
    sublist = hansunglist.find_all("td", class_="subject")
    i = 0
    try:
        while True:
            f = open("data.txt", "a")
            mainurl = sublist[i].find("a")
            mainurl = str(mainurl)
            front = mainurl.find("http")
            back = mainurl.find(">")
            mainurl = mainurl[front:back-1]
            new_url = urlmaker(mainurl)
            print(new_url)
            content = contentparshing(new_url)
            i+=1
            f.write(content)
            f.close()
            time.sleep(300)
    except IndexError as e:
        if(i == 0):
            state = 1
        print("INDEX ERROR")

def contentparshing(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    hansunglist = soup.find("table", class_="bbs-view")
    subject = hansunglist.find("th")
    subject = str(subject)
    cleaner = re.compile('<.*?>')
    cleantext = re.sub(cleaner, '', subject)
    print(cleantext)
    return cleantext

def urlmaker(string):
    while True:
        if(string.find("amp;") == -1):
            return string
        else:
            a = string.find("amp;")
            string1 = string[:a]
            string2 = string[a + 4:]
            string = string1 + string2

def imagemake():
    f = open("data.txt", "r")
    text = f.read()
    nlp = Twitter()
    nouns = nlp.nouns(text)
    words = Counter(nouns)
    tags = words.most_common(80)
    taglist = pytagcloud.make_tags(tags, maxsize=100)
    pytagcloud.create_tag_image(taglist, 'wordcloud.jpg', size=(640 , 480), fontname='Korean', rectangular=True)
    f.close()

while True:
    url = "http://hansung.ac.kr/web/www/cmty_01_01?p_p_id=EXT_BBS&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_pos=1&p_p_col_count=3&_EXT_BBS_struts_action=%2Fext%2Fbbs%2Fview&_EXT_BBS_sCategory=&_EXT_BBS_sKeyType=&_EXT_BBS_sKeyword=&_EXT_BBS_curPage=" + str(j)
    listparshing(url)
    if(state == 1):
        break
    else:
        j+=1
imagemake()