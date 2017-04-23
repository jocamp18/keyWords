from pymongo import MongoClient

class Mongo():
  def __init__(self):
    self.client = MongoClient('10.131.137.188', 27017)
    self.db = self.client["project13"]
    self.db.authenticate("user1", "keywords")
    self.indexes = self.db["indexes"]

  def insert(self, word, file_paths):
    self.indexes.insert_one({"_id": word, "file_paths": file_paths})

  def search(self, word):
    return self.indexes.find_one({"_id": word})
