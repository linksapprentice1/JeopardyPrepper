from threading import Thread
 
def makeThread(function, arguments):
   thread = Thread(target = function, args = arguments)
   thread.start()
   return thread

def joinThreads(threads):
   for thread in threads:
      thread.join()
