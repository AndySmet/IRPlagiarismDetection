
import csv
import time
import random
from functools import reduce

import math



def isPrime(n):

    if (n <= 1):
        return False
    if (n <= 3):
        return True

    if (n % 2 == 0 or n % 3 == 0):
        return False

    for i in range(5, int(math.sqrt(n) + 1), 6):
        if (n % i == 0 or n % (i + 2) == 0):
            return False

    return True


def nextPrime(N):
    # Base case
    if (N <= 1):
        return 2
    prime = N
    while True:
        prime = prime + 1
        if isPrime(prime):
            return prime






def jaccard(A, B):
    union = A.union(B)
    intersection = A.intersection(B)
    return len(intersection)/len(union)

def getShingles(string, n):
    badchars = ",.?!;\n\"'"
    for c in badchars:
        string = string.replace(c,"")
    words = string.lower().split()
    shingles = []

    for i in range(len(words)-n+1):
        shingle = ""
        shingle = reduce(lambda x,y: x+y+" ", words[i:i+n],"")

        shingles.append(shingle[:-1])

    return shingles

def hash(a,b,c,articles):
    result={}
    for article in articles:
        hashValues={}
        for shingle in articles[article]:
            hashValues[shingle]=(a*shingle+b)%c
        result[article]={min(hashValues, key=hashValues.get)}
    return result

def minhash(articles, numberOfHash):
    m = max(i for v in articles.values() for i in v)
    c = nextPrime(m) #lengte van de hash is gekozen als het priemgetal groter dan het hoogste getal dat toegewezen is aan de shingles
    result={}
    for i in range(numberOfHash): #make for each article a column with 'numberOfHash' rows
        a = int(random.uniform(m/2,m))
        b = int(random.uniform(m/2, m))
        ithMinHash=hash(a,b,c,articles) #Hash function maps the 'numbers/shingles' to a new number from length 'c'
        if i == 0:
            result = ithMinHash
        else:
            for article in ithMinHash:
                result[article] = result[article].union(ithMinHash[article])
    return result

if __name__ == '__main__':

    timestart = time.time()
    with open('news_articles_small.csv', mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)
        articles = {rows[0]:rows[1] for rows in reader}

        jaccardMatrix=[]

        shinglesDict={}
        articlesDict={}
        for article in articles:
            articlesDict[article]=set()
            shingles = set(getShingles(articles[article],2))
            for s in shingles:
                if s not in shinglesDict:
                    shinglesDict[s] = len(shinglesDict)
                articlesDict[article].add(shinglesDict[s]) #articlesDict contains the numbers per shingle per article

        articlesDict = minhash(articlesDict, 10)
        for a in articlesDict:
            row = []

            for b in articlesDict:
                if a > b:
                    score=jaccard(articlesDict[a], articlesDict[b])
                    if score > 0.8:
                        print(a,b,score)
                    row.append(score)
            jaccardMatrix.append(row)

        print(time.time()-timestart)


