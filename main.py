import JeopardyDatabase
import JeopardyCrawler
import JeopardyCategories


JeopardyDatabase.populate(JeopardyCrawler.fetchQuestions(JeopardyCategories.categoriesByRound()))
