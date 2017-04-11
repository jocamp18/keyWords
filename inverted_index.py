from mrjob.job import MRJob
from mrjob.step import MRStep
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from mongo import Mongo
import os

ps = PorterStemmer()
stop_words = stopwords.words('english')
tokenizer = RegexpTokenizer(r'\w+')
db = Mongo()

def tokenize(line):
  stemmed_words = []
  words = tokenizer.tokenize(line)
  for w in words:
    if w not in stop_words:
      stemmed_words.append(ps.stem(w))
  return stemmed_words

class InvertedIndex(MRJob):
  
  def mapper(self, key, line):
    words = tokenize(line)
    file_name = os.environ['mapreduce_map_input_file']
    for word in words:
      yield word, file_name

  def reducer(self, word, values):
    values = list(values)
    result = dict.fromkeys(set(values), 0)
    for document_path in values:
      result[document_path] += 1
    result = list(result.items())
    db.insert(word, result)
    yield word, result
  
if __name__ == '__main__':
  InvertedIndex.run()