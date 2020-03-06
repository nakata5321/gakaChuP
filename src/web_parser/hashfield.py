import json as js
import pandas as pd

class HashField:
    def __init__(self):
        self.__tagPopularity = pd.DataFrame(columns = ['Hashtag', 'Number of Posts', 'Cost', 'Potential Cost', 'Score'])
        self.__tagTree = {}
        self.__countTags = 0

    def saveTree(self, filename):
        with open(filename+'.json', 'w', encoding='utf8') as jfp:
            js.dump(self.__tagTree, jfp, indent=4)
        sortTable()
        self.__tagPopularity.to_csv(filename+'.csv', sep=' ', encoding='utf-8')

    def addHashTag(self, hashtag):
        if self.checkInTree(hashtag):
            self.__tagPopularity.loc[int(self.__tagTree[hashtag]['id'])][1] = int(self.__tagPopularity.loc[int(self.__tagTree[hashtag]['id'])][1])+1
            self.__tagTree[hashtag]['count'] += 1
        else:
            self.__tagTree[hashtag]={}
            self.__tagTree[hashtag]['id'] = self.__countTags
            self.__tagTree[hashtag]['count'] = 0
            self.__tagTree[hashtag]['rel'] = []
            self.__tagPopularity.loc[self.__countTags]=[hashtag,0,0,0]
            self.__countTags += 1

    def checkInTree(self,hashtag):
        if hashtag in self.__tagTree.keys():
            return True
        return False

    def addRelHashTags(self, hash, rel_hash_list):
        for rh in rel_hash_list:
            if rh not in self.__tagTree[hash]['rel']:
                self.__tagTree[hash]['rel'].append(rh)

    def getHashTree(self):
        return self.__tagTree

    def getHashTable(self):
        sortTable()
        return self.__tagPopularity

    def sortTableByCount(self):
        self.__tagPopularity = self.__tagPopularity.sort_values(by='Number of Posts')

    def sortTableByPrice(self):
        self.__tagPopularity = self.__tagPopularity.sort_values(by='Number of Posts')

    def sortTableByScore(self):
        self.__tagPopularity = self.__tagPopularity.sort_values(by='Score')

    def setHashScore(self,hashtag, score):
        self.__tagPopularity.loc[int(self.__tagTree[hashtag]['id'])][2] = score
