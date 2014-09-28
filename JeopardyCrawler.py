import urllib
import urllib3
import BeautifulSoup
import re
import threader 

collected_data = []

def fetchQuestions(categories_by_round):
   http = urllib3.PoolManager()
   threader.joinThreads(_threadPerCategory(http, categories_by_round))
   return collected_data

def _threadPerCategory(http, categories_by_round):
   for the_round, categories in categories_by_round.iteritems(): 
      for category in categories:
         yield threader.makeThread(_fetchQuestionsPerCategory, (http, the_round, category))

def _fetchQuestionsPerCategory(http, the_round, category):
   text = _text(_webpage(http, _url(category)))
   for question_and_answer in _questionAndAnswers(text):
      if all(question_and_answer):
         collected_data.append({   
            "round" : the_round,
            "category" : category,
            "question" : question_and_answer[0],
            "answer" : question_and_answer[1]
         })

def _text(webpage):
   return BeautifulSoup.BeautifulSoup(webpage).findAll(text=True)

def _webpage(http, url):
   return http.request('GET', url).data

def _url(category):
   return "http://j-archive.com/search.php?search=" + urllib.quote_plus(category) + "&submit=Search"

def _questionAndAnswers(elements):
   for i in _clueValueIndices(elements):
      yield _textTuple(elements, i + 1)

def _clueValueIndices(elements):
   return (i for i, x in enumerate(elements) if re.match("\$\d+", x) is not None)

def _textTuple(elements, i):
   i1 = _nextText(elements, i)
   i2 = _nextText(elements, i1 + 1)
   return _cleanUp(elements[i1]), _cleanUp(elements[i2])

def _nextText(elements, i):
   return next(i for i, x in enumerate(elements, i))

def _cleanUp(element):
   return element.strip().replace(": (", "").replace(":","").encode('utf8', 'replace')
