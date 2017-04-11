from pymongo import MongoClient

class Mongo():
  def __init__(self):
    self.client = MongoClient()
    self.db = self.client.keyword
    self.indexes = self.db.indexes

  def insert(self, word, file_paths):
    self.indexes.insert_one({"_id": word, "file_paths": file_paths})

  def search(self, word):
    return self.indexes.find_one({"_id": word})
