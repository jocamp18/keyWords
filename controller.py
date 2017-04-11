from mongo import Mongo
import sys

def count_words(phrase):
  db = Mongo()
  words = []
  for word in phrase.split():
    words.append(db.search(word))
  print(words)

if __name__ == "__main__":
  count_words(sys.argv[1])
