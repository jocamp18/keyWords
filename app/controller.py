#!/bin/env python

import sys
from mongo import Mongo
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from operator import itemgetter


def get_files(phrase, language):
  db = Mongo()

  #Initialize needed variables
  words = []
  i = 0
  dic = {}
  stop_words = []

  stop_words = stopwords.words(language)
  stemmer = SnowballStemmer(language)

  tokenizer = RegexpTokenizer(r'\w+')
  splited_words = tokenizer.tokenize(phrase)

  for word in splited_words:
    if word not in stop_words:
      word = stemmer.stem(word)
      files = db.search(word)
      if files is not None:
        files = files['file_paths']
        for file in files:
          if file[0] not in dic:
            dic[file[0]] = file[1]
          else:
            dic[file[0]] += file[1]
  sorted_list = sorted(dic.items(), key=itemgetter(1))
  sorted_list = list(reversed(sorted_list))
  address = []
  for file in sorted_list:
    path = file[0].split("/")
    file_name = path[-1]
    if language == "english":
      address.append("http://10.131.137.188/~en/" + file_name)
    else:
      address.append("http://10.131.137.188/~es/" + file_name)
  print(address)
  return address

if __name__ == "__main__":
  get_files(sys.argv[1], sys.argv[2])
