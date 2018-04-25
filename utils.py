import json
import requests
from bs4 import BeautifulSoup
import time
import re



########### CLEANING UTILS #############

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

from nltk.stem.porter import PorterStemmer
porter = PorterStemmer()


def split_on_caps(s):
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', ' '.join(s.split()))

def clean(article, stem = False):
    tokens = word_tokenize(article)
    words = [word for word in tokens if word.isalpha()]
    
    # convert everything to lower case
    words = [w.lower() for w in words]
    
    words = [w for w in words if not w in stop_words]
    
    # split on caps
    words = [split_on_caps(w) for w in words]
    
    if stem:
        words = [porter.stem(word) for word in words]
        
    return " ".join(words).split()





########### SCRAPING UTILS #############
def urlify(query): # i googled how to replace certain characters
    return query.replace(" ", "%20").replace("(", "%28").replace(")", "%29").replace(".", "%2E").replace("-", "%2D")

def get_url(param_dict):
    url = "https://newsapi.org/v2/everything?"
    for k, v in param_dict.items():
        url += (k + "=" + v + "&")
    return url

def get_articles(param_dict, page_end = 100, page_start=1):
    url_root = get_url(param_dict)
    responses = []
    for page in range(page_start, page_end + 1):
        response = requests.get(url_root + "page="+str(page)).json()
        if len(response['articles']) == 0:
            break
        else:
            responses.append(response)
    return responses


def scrape_text_from_articles(articles):
    docs = []
    for i, article in enumerate(articles):
        if i % 50 == 0:
            print(str(i)+"/"+str(len(articles)), end="...")
        url = article['url']
        soup = BeautifulSoup(requests.get(url).text, "lxml")
        content = soup.find("div", {"class":"organism contentStream"})
        if content is None:
            content_slides = soup.find_all("div", {"class":"organism contentStream slide"})
            paragraphs = []
            for content_slide in content_slides:
                paragraphs += content_slide.find_all("p")
        else:
            paragraphs = content.find_all("p")

        entire_text = "".join([p.get_text() for p in paragraphs])
        docs.append(entire_text)
        time.sleep(.300)
    return docs


def get_docs_from_params(param_dict):
    responses = get_articles(param_dict)
    all_articles = []
    for response in responses:
        all_articles += response['articles']
        
    return scrape_text_from_articles(all_articles)


TOP_100_PLAYERS = ['lebron james',
 'kevin durant',
 'kawhi leonard',
 'stephen curry',
 'russell westbrook',
 'james harden',
 'giannis antetokounmpo',
 'anthony davis',
 'jimmy butler',
 'karl-anthony towns',
 'draymond green',
 'chris paul',
 'john wall',
 'klay thompson',
 'paul george',
 'demarcus cousins',
 'gordon hayward',
 'rudy gobert',
 'marc gasol',
 'kyle lowry',
 'paul millsap',
 'blake griffin',
 'mike conley',
 'damian lillard',
 'deandre jordan',
 'nikola jokic',
 'kyrie irving',
 'isaiah thomas',
 'al horford',
 'bradley beal',
 'demar derozan',
 'kevin love',
 'c.j. mccollum',
 'andre drummond',
 'carmelo anthony',
 'kristaps porzingis',
 'lamarcus aldridge',
 'kemba walker',
 'eric bledsoe',
 'khris middleton',
 'avery bradley',
 'dwight howard',
 'jrue holiday',
 'brook lopez',
 'andre iguodala',
 'harrison barnes',
 'otto porter',
 'goran dragic',
 'eric gordon',
 'danilo gallinari',
 'nicolas batum',
 'danny green',
 'andrew wiggins',
 'jae crowder',
 'george hill',
 'serge ibaka',
 'ricky rubio',
 'steven adams',
 'jeff teague',
 'hassan whiteside',
 'clint capela',
 'trevor ariza',
 'derrick favors',
 'myles turner',
 'patrick beverley',
 'gary harris',
 'devin booker',
 'joel embiid',
 'kentavious caldwell-pope',
 'taj gibson',
 'tristan thompson',
 'dirk nowitzki',
 'cody zeller',
 'lou williams',
 'jusuf nurkic',
 'robert covington',
 'wilson chandler',
 'malcolm brogdon',
 'tobias harris',
 'j.j. redick',
 'dwyane wade',
 'markieff morris',
 'marcus morris',
 'dennis schroder',
 'reggie jackson',
 'rodney hood',
 'dion waiters',
 'marcin gortat',
 'victor oladipo',
 'jamal murray',
 'evan fournier',
 'mason plumlee',
 'james johnson',
 'joe ingles',
 'thaddeus young',
 'julius randle',
 'j.r. smith',
 'patrick patterson',
 'ben simmons',
 'dennis smith']







##### how i got the top 100 names:
# ## get all NBA players, add them to the query
# player_url = "https://www.washingtonpost.com/graphics/2017/sports/nba-top-100-players-2017/?utm_term=.856ecec51f15"
# soup = BeautifulSoup(requests.get(player_url).content, "lxml")
# content = soup.find_all("h4", {"class":"player-name"})
# def get_name(item):
#     temp = str(item).split("<h4 class=\"player-name\">")[1]
#     first, second_temp = temp.split("<br/>")
#     second = second_temp.split("</h4>")[0]
#     return first.lower(), second.lower()

# names = [" ".join(list(get_name(item))) for item in soup.find_all("h4", {"class":"player-name"})]
