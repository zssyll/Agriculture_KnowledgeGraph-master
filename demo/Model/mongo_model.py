import sys
import os

import pymongo
from pymongo import MongoClient
from constants import constant_url

class Mongo():
	clent = None
	db = None
	collection = None
	def makeConnection(self):
		self.client = MongoClient(constant_url.MONGODB_IP_URL, constant_url.MONGODB_PORT)

	def getDatabase(self,dbName):
		self.db = self.client[dbName]
		return self.db

	def getCollection(self,collectionName):
		self.collection = self.db[collectionName]
		return self.collection

