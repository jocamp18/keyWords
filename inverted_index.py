from mrjob.job import MRJob
from mrjob.step import MRStep
from nltk.stem import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re
from mongo import Mongo
import os
from operator import itemgetter

spanish_stemmer = SnowballStemmer('spanish')
english_stemmer = SnowballStemmer('porter')
spanish_stop_words = stopwords.words('spanish')
english_stop_words = stopwords.words('english')
tokenizer = RegexpTokenizer(r'\w+')
db = Mongo()

def tokenize(line, language):
  stemmed_words = []
  words = tokenizer.tokenize(line)
  if language == 'es':
    for w in words:
      if w not in spanish_stop_words:
        stemmed_words.append(spanish_stemmer.stem(w))
  else:
    for w in words:
      if w not in english_stop_words:
        stemmed_words.append(english_stemmer.stem(w))

  return stemmed_words


class InvertedIndex(MRJob):

  def mapper(self, key, line):
    line = re.sub(r'\d+', '', line)
    if line != "":
      file_name = os.environ['mapreduce_map_input_file']
      language = file_name.split('/')[-2]
      words = tokenize(line, language)
      for word in words:
        yield (word, file_name),1

  def combiner(self, pair, values):
    yield pair[0], (pair[1], sum(values))

  def reducer(self, word, values):
    values = list(values)
    file_names, frec = zip(*values)
    file_names = list(file_names)
    result = dict.fromkeys(set(file_names), 0)
    for file_name in values:
      result[file_name[0]] += file_name[1]
    result = list(result.items())
    sorted_result = sorted(result, key=itemgetter(1))
    if len(sorted_result) > 10:
      db.insert(word, sorted_result[:10])
    else:
      db.insert(word, sorted_result)
    yield word, result

if __name__ == '__main__':
  InvertedIndex.run()
