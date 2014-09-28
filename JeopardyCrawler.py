import urllib
import urllib3
import re
import BeautifulSoup
import threader 

collected_data = []

def nextText(elements, i):
   return next(i for i, x in enumerate(elements, i))

def cleanUp(element):
   return element.strip().replace(": (", "").replace(":","").encode('utf8', 'replace')

def textTuple(elements, i):
   i1 = nextText(elements, i)
   i2 = nextText(elements, i1+1)
   return cleanUp(elements[i1]), cleanUp(elements[i2])

def clueValueIndices(elements):
   return (i for i, x in enumerate(elements) if re.match("\$\d+", x) is not None)

def questionAndAnswers(elements):
   for i in clueValueIndices(elements):
      yield textTuple(elements, i+1)

def fetchQuestions(categories_by_round):
   http = urllib3.PoolManager()
   threads = []
   for the_round, categories in categories_by_round.iteritems(): 
      for category in categories:
         threads.append(threader.makeThread(fetchQuestionsPerCategory, (http, the_round, category)))
   threader.joinThreads(threads)
   return collected_data

def fetchQuestionsPerCategory(http, the_round, category):
   url = "http://j-archive.com/search.php?search=" + urllib.quote_plus(category) + "&submit=Search"
   webpage = http.request('GET', url).data
   soup = BeautifulSoup.BeautifulSoup(webpage)
   text = soup.findAll(text=True)
   for question_and_answer in questionAndAnswers(text):
      if all(question_and_answer):
         collected_data.append({   
            "round" : the_round,
            "category" : category,
            "question" : question_and_answer[0],
            "answer" : question_and_answer[1]
         })
