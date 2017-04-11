from mongo import Mongo
import sys

def count_words(phrase):
  db = Mongo()
  words = []
  i = 0
  dic = {}
  for word in phrase.split():
    word_aux = db.search(word)['file_paths']
    for file in word_aux:
      if file[0] not in dic:
        dic[file[0]] = file[1]
      else:
        dic[file[0]] += file[1]
  print(dic)

if __name__ == "__main__":
  count_words(sys.argv[1])
